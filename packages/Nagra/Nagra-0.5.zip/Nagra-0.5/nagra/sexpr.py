"""
The `AST` (abstract syntax tree) implement parsing and evaluation
of [s-expressions](https://en.wikipedia.org/wiki/S-expression).

Example:

``` python-console
>>> from nagra.sexpr import AST
>>> AST.parse('(+ 1 1)')
<nagra.sexpr.AST object at 0x7f1bcc5b2fd0>
>>> ast = AST.parse('(+ 1 1)')
>>> ast.eval()
2
```

The `eval` method accepts an `env` parameter, a dictionary used to
evaluate non-litteral tokens:

``` python-console
>>> ast = AST.parse('(+ 1 x)')
>>> ast.eval()
Traceback (most recent call last):
   ...
ValueError: Unexpected token: "x"
>>> ast.eval({'x': 2})
3
```

"""

import shlex

from nagra.exceptions import EvalTypeError


DEFAULT_FLAVOR = "postgresql"
__all__ = ["AST"]


def list_to_dict(*items):
    it = iter(items)
    return dict(zip(it, it))


class KWargs:
    def __init__(self, *items):
        self.value = list_to_dict(*items)

    def __repr__(self):
        return f'<KWargs "{self.value}">'


class Alias:
    """
    Simple wrapper that combine a value and an alias name
    """

    def __init__(self, value, name):
        self.value = value
        self.name = name


def tokenize(expr):
    lexer = shlex.shlex(expr)
    lexer.wordchars += ".!=<>:{}-|"
    prev_tk = None
    for i in lexer:
        tk = Token.from_value(i, prev_tk)
        prev_tk = tk
        yield tk


def scan(tokens, end_tk=")"):
    res = []
    for tk in tokens:
        if tk.value == end_tk:
            return res
        elif tk.value == "(":
            res.append(scan(tokens))
        else:
            res.append(tk)

    tail = next(tokens, None)
    if tail:
        raise ValueError(f'Unexpected token: "{tail.value}"')
    return res


class AST:
    builtins = {
        # Boolean
        "!=": "{} != {}".format,
        "<": "{} < {}".format,
        "<=": "{} <= {}".format,
        "=": "{} = {}".format,
        ">": "{} > {}".format,
        ">=": "{} >= {}".format,
        "and": lambda *x: " AND ".join(x),
        "or": lambda *x: "(%s)" % (" OR ".join(x)),
        "not": "NOT {}".format,
        "is": "{} is {}".format,
        "isnot": "NOT {} IS {}".format,
        # Arithmetic
        "+": lambda *xs: " + ".join(map(str, xs)),
        "-": (lambda *xs: " - ".join(map(str, xs)) if len(xs) > 1 else f"-{xs[0]}"),
        "*": lambda *xs: " * ".join(map(str, xs)),
        "/": lambda *xs: " / ".join(map(str, xs)),
        # dates and time
        "strftime": "strftime({}, {})".format,
        "extract": "EXTRACT({} FROM {})".format,
        # Strings
        "length": "LENGTH({})".format,
        "like": "{} LIKE {}".format,
        "lower": "LOWER({})".format,
        "upper": "UPPER({})".format,
        "match": "{} MATCH {}".format,
        "ilike": "{} ILIKE {}".format,
        "||": lambda *xs: " || ".join(map(str, xs)),
        "substr": "substr({}, {}, {})".format,
        # Others
        "in": lambda x, *ys: f"{x} in (%s)" % ", ".join(map(str, ys)),
    }

    literals = {
        "true": lambda: "true",
        "false": lambda: "false",
        "null": lambda: "NULL",
    }

    aggregates = {
        "min": "min({})".format,
        "max": "max({})".format,
        "sum": "sum({})".format,
        "avg": "avg({})".format,
        "every": "every({})".format,
        "count": lambda x="*": f"count({x})",
        # Sqlite specific
        "group_concat": lambda *xs: ("group_concat(%s)")
        % (", ".join("{}" for _ in xs)).format(*xs),
        # Pg specific
        "string_agg": "string_agg({}, {})".format,
        "array_agg": "array_agg({})".format,
        "json_agg": "json_agg({})".format,
        "bool_or": "bool_or({})".format,
        "bool_and": "bool_and({})".format,
        "json_object_agg": "json_object_agg({}, {})".format,
    }

    def __init__(self, tokens):
        # Auto-wrap sublist into AST
        self.tokens = [tk if isinstance(tk, Token) else AST(tk) for tk in tokens]

    @classmethod
    def parse(cls, expr):
        res = tokenize(expr)
        tokens = scan(res)[0]
        if isinstance(tokens, Token):
            tokens = [tokens]
        return AST(tokens)

    def chain(self):
        for tk in self.tokens:
            if isinstance(tk, Token):
                yield tk
            else:
                yield from tk.chain()

    def _eval(self, env, flavor, top=False):
        head, tail = self.tokens[0], self.tokens[1:]
        args = [tk._eval(env, flavor) for tk in tail]
        res = head._eval(env, flavor, *args)
        return res if top else "({})".format(res)

    def eval(self, env, flavor=DEFAULT_FLAVOR):
        return self._eval(env, flavor, top=True)

    def relations(self):
        for tk in self.chain():
            if tk.is_relation():
                yield tk.value

    def _eval_type(self, env):
        head, tail = self.tokens[0], self.tokens[1:]
        args = [tk._eval_type(env) for tk in tail]
        res = head._eval_type(env, *args)
        return res

    def eval_type(self, env):
        return self._eval_type(env)

    def get_args(self):
        """
        Return token that should be treated as query arguments
        """
        args = list((tk.get_arg() for tk in self.chain()))
        return [a for a in args if a]

    def is_aggregate(self):
        for tk in self.chain():
            if tk.is_aggregate():
                return True
        return False


class Token:
    def __init__(self, value):
        self.value = value

    def is_relation(self):
        return False

    @staticmethod
    def from_value(value, prev_tk):
        # Handle exceptions
        if value == "(":
            return LParen(value)

        # Dot prefix force Vartoken
        if value.startswith("."):
            return VarToken(value.lstrip("."))

        # Literals take precedence over everything else
        if value in AST.literals:
            return LiteralToken(value)

        # First item should be an operator
        if isinstance(prev_tk, LParen):
            if value in AST.builtins:
                return BuiltinToken(value)
            if value in AST.literals:
                return LiteralToken(value)
            if value in AST.aggregates:
                return AggToken(value)

        if (value[0], value[-1]) == ("{", "}"):
            return ParamToken(value)
        try:
            if "." in value:
                value = float(value)
                return FloatToken(value)
            else:
                value = int(value)
                return IntToken(value)
        except ValueError:
            pass
        return StrToken(value) if value[0] in "\"'" else VarToken(value)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"<{cls} {self.value}>"

    def get_arg(self):
        return None

    def _eval(self, env, flavor, *args):
        return None


class LParen(Token):
    "Left Parenthesis"


class ParamToken(Token):
    "Parameterized Token"

    def __init__(self, value):
        # Remove braces
        self.value = value[1:-1]

    def _eval(self, env, flavor, *args):
        placeholder = "%s" if flavor == "postgresql" else "?"
        return placeholder


class LitToken(Token):
    "Litteral Token"

    def _eval_type(self, env):
        return self._type

    def _eval(self, env, flavor, *args):
        return self.value


class FloatToken(LitToken):
    "Float Token"
    _type = float


class IntToken(LitToken):
    "Integer Token"
    _type = int


class StrToken(LitToken):
    "String Token"

    def __init__(self, value):
        # Remove quotes
        self.value = value[1:-1]

    def _eval_type(self, env):
        return str

    def _eval(self, env, flavor, *args):
        return f"'{self.value}'"


class VarToken(Token):
    def __init__(self, value):
        self.join_alias = None
        super().__init__(value)

    def is_relation(self):
        return "." in self.value

    def _eval(self, env, flavor, *args):
        if self.is_relation():
            self.join_alias = env.add_ref(self.value.split("."))
            return self.join_alias
        return '"{}"."{}"'.format(env.table.name, self.value)

    def _eval_type(self, env):
        # TODO handle paramtoken here?
        if self.is_relation():
            *head, tail = self.value.split(".")
            ftable, _, _ = env.table.join_on(tuple(head), env=env)
            col = ftable.columns[tail]
            return col.python_type()
        elif col := env.table.columns.get(self.value):
            return col.python_type()
        elif self.value == env.table.primary_key:
            # implicit type for pk is integer
            return int
        else:
            raise EvalTypeError(f"Unable to eval type of '{self.value}'")


class OpToken(Token):
    ops = AST.builtins | AST.literals

    def _eval(self, env, flavor, *args):
        op = self.ops[self.value]
        return op(*args)

    # FIXME shoud return different _eval_type based on op ?!


class BuiltinToken(OpToken):
    num_like = "+-*/"
    bool_like = (
        "!=",
        "<",
        ">",
        ">=",
        "<=",
        "=",
        "and",
        "or",
        "not",
        "is",
        "isnot",
        "like",
        "ilike",
    )

    def _eval_type(self, env, *operands):
        # FIXME, probably too basic
        if self.value in self.num_like:
            if any(op == float for op in operands):
                return float
            return int
        elif self.value in self.bool_like:
            return bool
        else:
            return str


class LiteralToken(OpToken):
    def _eval_type(self, env, *operands):
        if self.value == "null":
            return None
        return bool


class AggToken(OpToken):
    ops = AST.aggregates

    num_like = ["sum", "avg"]
    bool_like = ["every"]

    def _eval_type(self, env, *operands):
        if self.value == "count":
            return int
        if self.value in self.num_like:
            assert operands[0] in (float, int)
            return operands[0]
        if self.value in self.bool_like:
            assert operands[0] == bool
            return bool
        else:
            return operands[0]
