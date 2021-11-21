from pylexers.NFALexer.NFA import NFA
from pylexers.RegularExpressions.util import (
    _get_regular_expression_arg1,
    _get_regular_expression_arg2,
    _is_epsilon,
    _is_symbol,
    _is_concat,
    _is_or,
    _is_kleene_star,
)


def _nfa_from_re_epsilon():
    return NFA()


def _nfa_from_re_symbol(re):
    final_state = NFA()
    initial_state = NFA(final_states={final_state})
    initial_state.add_transition(final_state, _get_regular_expression_arg1(re))
    return initial_state


def _nfa_from_re_concat(re):
    machine_1 = _regular_expression_to_nfa(_get_regular_expression_arg1(re))
    machine_2 = _regular_expression_to_nfa(_get_regular_expression_arg2(re))
    accepting_state = NFA()
    initial_state = NFA(final_states={accepting_state})

    initial_state.add_transition(machine_1, "EPSILON")
    for final_state in machine_1.final_states:
        final_state.add_transition(machine_2, "EPSILON")
    for final_state in machine_2.final_states:
        final_state.add_transition(accepting_state, "EPSILON")
    return initial_state


def _nfa_from_re_or(re):
    machine_1 = _regular_expression_to_nfa(_get_regular_expression_arg1(re))
    machine_2 = _regular_expression_to_nfa(_get_regular_expression_arg2(re))
    accepting_state = NFA()
    initial_state = NFA(final_states={accepting_state})

    initial_state.add_transition(machine_1, "EPSILON")
    initial_state.add_transition(machine_2, "EPSILON")
    for final_state in machine_1.final_states.union(machine_2.final_states):
        final_state.add_transition(accepting_state, "EPSILON")
    return initial_state


def _nfa_from_re_kleene_star(re):
    machine = _regular_expression_to_nfa(_get_regular_expression_arg1(re))
    accepting_state = NFA()
    initial_state = NFA(final_states={accepting_state})

    initial_state.add_transition(machine, "EPSILON")
    initial_state.add_transition(accepting_state, "EPSILON")
    for final_state in machine.final_states:
        final_state.add_transition(machine, "EPSILON")
        final_state.add_transition(accepting_state, "EPSILON")
    return initial_state


def _regular_expression_to_nfa(re):
    if _is_epsilon(re):
        return _nfa_from_re_epsilon()
    elif _is_symbol(re):
        return _nfa_from_re_symbol(re)
    elif _is_concat(re):
        return _nfa_from_re_concat(re)
    elif _is_or(re):
        return _nfa_from_re_or(re)
    elif _is_kleene_star(re):
        return _nfa_from_re_kleene_star(re)
    else:
        raise SyntaxError("Encountered unknown regular expession")
