
def _is_regular_expression(re):
    return type(re) == list and re[0] == "Regular Expression"


def _get_regular_expression_type(re):
    return re[1]


def _get_regular_expression_arg1(re):
    return re[2]


def _get_regular_expression_arg2(re):
    return re[3]


def _is_empty_set(re):
    return _is_regular_expression(re) and re[1] == "EMPTY SET"


def _is_epsilon(re):
    return _is_regular_expression(re) and re[1] == "EPSILON"


def _is_symbol(re):
    return _is_regular_expression(re) and re[1] == "SYMBOL"


def _is_concat(re):
    return _is_regular_expression(re) and re[1] == "CONCAT"


def _is_or(re):
    return _is_regular_expression(re) and re[1] == "OR"


def _is_kleene_star(re):
    return _is_regular_expression(re) and re[1] == "KLEENE STAR"
