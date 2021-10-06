from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class _RegularExpression:
    type: str
    re1: Union["_RegularExpression", str]
    re2: Optional["_RegularExpression"]

    def is_nullable(self):
        return _is_epsilon(self.nullable())

    def nullable(self) -> "_RegularExpression":
        if _is_epsilon(self) or _is_kleene_star(self):
            return _build_epsilon()
        elif _is_empty_set(self) or _is_symbol(self):
            return _build_empty_set()
        elif _is_concat(self):
            a = self.re1.nullable()
            b = self.re2.nullable()
            if _is_epsilon(a) and _is_epsilon(b):
                return _build_epsilon()
            return _build_empty_set()
        elif _is_or(self):
            a = self.re1.nullable()
            b = self.re2.nullable()
            if _is_epsilon(a) or _is_epsilon(b):
                return _build_epsilon()
            return _build_empty_set()

    def simplify(self) -> "_RegularExpression":
        if _is_concat(self):
            r = self.re1.simplify()
            s = self.re2.simplify()
            if _is_empty_set(r) or _is_empty_set(s):
                return _build_empty_set()
            if _is_epsilon(r):
                return s
            if _is_epsilon(s):
                return r
        elif _is_or(self):
            r = self.re1.simplify()
            s = self.re2.simplify()
            if _is_empty_set(r):
                return s
            elif _is_empty_set(s):
                return r
        return self

    def derivative(self, symbol) -> "_RegularExpression":
        if _is_empty_set(self) or _is_epsilon(self):
            return _build_empty_set()
        elif _is_symbol(self):
            if self.re1 == symbol:
                return _build_epsilon()
            else:
                return _build_empty_set()
        elif _is_concat(self):
            dr = self.re1.derivative(symbol)
            ds = self.re2.derivative(symbol)
            return _build_or(
                _build_concat(dr, self.re2), _build_concat(self.re1.nullable(), ds)
            ).simplify()
        elif _is_or(self):
            dr = self.re1.derivative(symbol)
            ds = self.re2.derivative(symbol)
            return _build_or(dr, ds).simplify()
        elif _is_kleene_star(self):
            dr = self.re1.derivative(symbol)
            return _build_concat(dr, self).simplify()
        else:
            raise SyntaxError("Encountered unknown regular expession")

    def matches(self, string):
        re = self
        for c in string:
            re = re.derivative(c).simplify()
        return re.is_nullable()

    def get_alphabet(self) -> str:
        if self.re1 and self.re2:
            return self.re1.get_alphabet() + self.re2.get_alphabet()
        elif isinstance(self.re1, _RegularExpression):
            return self.re1.get_alphabet()
        else:
            return self.re1 or ""


def _build_regular_expression(type, re1=None, re2=None) -> _RegularExpression:
    return _RegularExpression(type, re1, re2)


def _build_empty_set() -> _RegularExpression:
    return _build_regular_expression("EMPTY SET")


def _build_epsilon() -> _RegularExpression:
    return _build_regular_expression("EPSILON")


def _build_symbol(symbol) -> _RegularExpression:
    return _build_regular_expression("SYMBOL", symbol)


def _build_concat(re_1, re_2) -> _RegularExpression:
    return _build_regular_expression("CONCAT", re_1, re_2)


def _build_or(re_1, re_2) -> _RegularExpression:
    return _build_regular_expression("OR", re_1, re_2)


def _build_kleene_star(re) -> _RegularExpression:
    return _build_regular_expression("KLEENE STAR", re)


def _is_regular_expression(re: _RegularExpression) -> bool:
    return isinstance(re, _RegularExpression)


def _get_regular_expression_type(re: _RegularExpression) -> str:
    return re.type


def _get_regular_expression_arg1(re: _RegularExpression) -> _RegularExpression:
    return re.re1 or _build_empty_set()


def _get_regular_expression_arg2(re: _RegularExpression) -> _RegularExpression:
    return re.re2 or _build_empty_set()


def _is_empty_set(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "EMPTY SET"


def _is_epsilon(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "EPSILON"


def _is_symbol(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "SYMBOL"


def _is_concat(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "CONCAT"


def _is_or(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "OR"


def _is_kleene_star(re: _RegularExpression) -> bool:
    return _is_regular_expression(re) and re.type == "KLEENE STAR"
