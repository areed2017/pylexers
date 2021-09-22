from string import printable

from RegularExpressions.builders import _build_or, _build_symbol, _build_concat, _build_kleene_star


class _RegularExpression:
    def __init__(self, re):
        self.re = re


"""
Basic Regular Expressions
"""


class SymbolRegularExpression(_RegularExpression):
    def __init__(self, character: chr):
        super().__init__(_build_symbol(character))


class OrRegularExpression(_RegularExpression):
    def __init__(self, regular_expression_1: _RegularExpression, regular_expression_2: _RegularExpression):
        super().__init__(_build_or(regular_expression_1.re, regular_expression_2.re))


class ConcatRegularExpression(_RegularExpression):
    def __init__(self, regular_expression_1: _RegularExpression, regular_expression_2: _RegularExpression):
        super().__init__(_build_concat(regular_expression_1.re, regular_expression_2.re))


class KleeneStarRegularExpression(_RegularExpression):
    def __init__(self, regular_expression: _RegularExpression):
        super().__init__(_build_kleene_star(regular_expression.re))


"""
Extended Regular Expressions
"""


class SigmaRegularExpression(_RegularExpression):
    @staticmethod
    def build_re(alphabet: str, exclude: str) -> list:
        for ex in exclude:
            alphabet = alphabet.replace(ex, "")

        re = _build_symbol(alphabet[0])
        for symbol in alphabet[1:]:
            re = _build_or(_build_symbol(symbol), re)
        return re

    def __init__(self, alphabet=printable, exclude=""):
        super().__init__(self.build_re(alphabet, exclude))


class StringRegularExpression(_RegularExpression):
    @staticmethod
    def build_re(string: str) -> list:
        re = _build_symbol(string[0])
        for symbol in string[1:]:
            re = _build_concat(re, _build_symbol(symbol))
        return re

    def __init__(self, string: str):
        super().__init__(self.build_re(string))


class AtLeastOneRegularExpression(_RegularExpression):
    def __init__(self, regular_expression: _RegularExpression):
        super().__init__(_build_concat(regular_expression.re, _build_kleene_star(regular_expression.re)))


