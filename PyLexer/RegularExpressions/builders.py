
def _build_regular_expression(type, re):
    return ['Regular Expression', type] + re


def _build_empty_set():
    return _build_regular_expression("EMPTY SET", [])


def _build_epsilon():
    return _build_regular_expression("EPSILON", [])


def _build_symbol(symbol):
    return _build_regular_expression("SYMBOL", [symbol])


def _build_concat(re_1, re_2):
    return _build_regular_expression("CONCAT", [re_1, re_2])


def _build_or(re_1, re_2):
    return _build_regular_expression("OR", [re_1, re_2])


def _build_kleene_star(re):
    return _build_regular_expression("KLEENE STAR", [re])

