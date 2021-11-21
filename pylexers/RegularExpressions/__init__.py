from string import printable

from RegularExpressions.util import (
    _build_or,
    _build_symbol,
    _build_concat,
    _build_kleene_star,
    _build_epsilon,
)

from RegularExpressions.util import _RegularExpression

"""
Basic Regular Expressions
"""


def Symbol(character: chr):
    return _build_symbol(character)


def Or(*regular_expressions: _RegularExpression) -> _RegularExpression:
    re = regular_expressions[0]
    for r in regular_expressions[1:]:
        re = _build_or(re, r)
    return re


def Concat(
    regular_expression_1: _RegularExpression, regular_expression_2: _RegularExpression
) -> _RegularExpression:
    return _build_concat(regular_expression_1, regular_expression_2)


def Star(regular_expression: _RegularExpression) -> _RegularExpression:
    return _build_kleene_star(regular_expression)


"""
Extended Regular Expressions
"""


def Sigma(alphabet: str = printable, exclude: str = "") -> _RegularExpression:
    for ex in exclude:
        alphabet = alphabet.replace(ex, "")

    re = _build_symbol(alphabet[0])
    for symbol in alphabet[1:]:
        re = _build_or(_build_symbol(symbol), re)
    return re


def String(string: str) -> _RegularExpression:
    def _build_string(s):
        if len(s) == 1:
            return _build_symbol(s)
        return _build_concat(_build_symbol(s[0]), _build_string(s[1:]))

    return _build_string(string)


def AtLeastOne(regular_expression: _RegularExpression) -> _RegularExpression:
    return _build_concat(regular_expression, _build_kleene_star(regular_expression))


def Optional(regular_expression: _RegularExpression) -> _RegularExpression:
    return _build_or(regular_expression, _build_epsilon())
