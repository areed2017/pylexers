import dataclasses
import typing

from pylexers.BaseLexer import Lexer
from pylexers.SymbolTable import SymbolTable
from pylexers.RegularExpressions import _RegularExpression, Sigma, Concat, Or, _Star, _Symbol


@dataclasses.dataclass
class _Group:
    re: _RegularExpression


def get_last_re(symbol_table: SymbolTable) -> typing.Optional[_RegularExpression]:
    if symbol_table.does_identifier_exist("LAST_RE"):
        re = symbol_table.get_identifier("LAST_RE")
        return re.re if isinstance(re, _Group) else re
    return None


def _build_regular_expression(lexer: Lexer, symbol_table: SymbolTable) -> _RegularExpression:
    next_token = lexer.peek()
    if next_token is None:
        return get_last_re(symbol_table)

    re = None
    if next_token == "OPEN-PAREN":
        next(lexer)
        re = _Group(re=build_regular_expression(lexer, symbol_table.create_sub_scope()))
    elif next_token == "CLOSE-PAREN":
        next(lexer)
        return symbol_table.get_identifier("LAST_RE")
    elif next_token == "DIGIT":
        next(lexer)
        re = _Group(re=Sigma("0123456789"))
    elif next_token == "NON-DIGIT":
        next(lexer)
        re = _Group(re=Sigma(exclude="0123456789"))
    elif next_token == "WHITE-SPACE":
        next(lexer)
        re = _Group(re=Sigma(" \t\n\r\f\v"))
    elif next_token == "NON-WHITE-SPACE":
        next(lexer)
        re = _Group(re=Sigma(exclude=" \t\n\r\f\v"))
    elif next_token == "ALPHA-NUMERIC":
        next(lexer)
        re = _Group(re=Sigma("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
    elif next_token == "NON-ALPHA-NUMERIC":
        next(lexer)
        re = _Group(re=Sigma(exclude="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
    elif next_token == "OR":
        next(lexer)
        next_re = build_regular_expression(lexer, symbol_table)
        try:
            re = get_last_re(symbol_table)
        except RuntimeError:
            raise SyntaxError("Or found without leading regular expression")
        re = Or(re, next_re)
    elif next_token == "STAR":
        next(lexer)
        try:
            re = symbol_table.get_identifier("LAST_RE")
            if isinstance(re, _Group):
                re = _Star(re.re)
            elif re.type == "OR":
                re = Or(re.re1, _Star(re.re2))
            elif re.type == "CONCAT":
                re = Concat(re.re1, _Star(re.re2))
            else:
                re = _Star(re)
            symbol_table.remove_identifier("LAST_RE")
        except RuntimeError:
            raise SyntaxError("Kleene _Star found without leading regular expression")
    elif next_token[0] == "SYMBOL":
        next(lexer)
        re = _Symbol(next_token[1])

    if symbol_table.does_identifier_exist("LAST_RE"):
        re = Concat(get_last_re(symbol_table), re)
    symbol_table.reset_identifier("LAST_RE", re, "RE")
    return _build_regular_expression(lexer, symbol_table)


def build_regular_expression(lexer: Lexer, symbol_table: SymbolTable) -> _RegularExpression:
    re = _build_regular_expression(lexer, symbol_table)
    return re.re if isinstance(re, _Group) else re