from RegularExpressions.builders import _build_empty_set, _build_epsilon, _build_concat, _build_or
from RegularExpressions.util import _get_regular_expression_arg1, _get_regular_expression_arg2,\
    _is_epsilon, _is_symbol, _is_concat, _is_or, _is_kleene_star, _is_empty_set


def nullable(re):
    if _is_epsilon(re) or _is_kleene_star(re):
        return _build_epsilon()
    elif _is_empty_set(re) or _is_symbol(re):
        return _build_empty_set()
    elif _is_concat(re):
        a = nullable(_get_regular_expression_arg1(re))
        b = nullable(_get_regular_expression_arg2(re))
        if _is_epsilon(a) and _is_epsilon(b):
            return _build_epsilon()
        return _build_empty_set()
    elif _is_or(re):
        a = nullable(_get_regular_expression_arg1(re))
        b = nullable(_get_regular_expression_arg2(re))
        if _is_epsilon(a) or _is_epsilon(b):
            return _build_epsilon()
        return _build_empty_set()


def derivative(re, symbol):
    if _is_empty_set(re) or _is_epsilon(re):
        return _build_empty_set()
    elif _is_symbol(re):
        if _get_regular_expression_arg1(re) == symbol:
            return _build_epsilon()
        else:
            return _build_empty_set()
    elif _is_concat(re):
        r = _get_regular_expression_arg1(re)
        s = _get_regular_expression_arg2(re)
        dr = derivative(r, symbol)
        ds = derivative(s, symbol)
        return simplify_regular_expression(_build_or(_build_concat(dr, s), _build_concat(nullable(r), ds)))
    elif _is_or(re):
        r = _get_regular_expression_arg1(re)
        s = _get_regular_expression_arg2(re)
        dr = derivative(r, symbol)
        ds = derivative(s, symbol)
        return simplify_regular_expression(_build_or(dr, ds))
    elif _is_kleene_star(re):
        dr = derivative(_get_regular_expression_arg1(re), symbol)
        return simplify_regular_expression(_build_concat(dr, re))
    else:
        raise SyntaxError("Encountered unknown regular expession")


def simplify_regular_expression(re):
    if _is_concat(re):
        r = simplify_regular_expression(_get_regular_expression_arg1(re))
        s = simplify_regular_expression(_get_regular_expression_arg2(re))
        if _is_empty_set(r) or _is_empty_set(s):
            return _build_empty_set()
        if _is_epsilon(r):
            return s
        if _is_epsilon(s):
            return r
    elif _is_or(re):
        r = simplify_regular_expression(_get_regular_expression_arg1(re))
        s = simplify_regular_expression(_get_regular_expression_arg2(re))
        if _is_empty_set(r):
            return s
        elif _is_empty_set(s):
            return r
    return re
