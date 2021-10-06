from BaseLexer import Lexer
from DFALexer.DFA import DFA
from RegularExpressions.util import _RegularExpression, _is_epsilon, _is_empty_set


class DFALexer(Lexer):
    def __init__(
        self, regular_expressions: list[_RegularExpression], tokenize_functions: list
    ):
        super().__init__(regular_expressions, tokenize_functions)
        self.dfa_list = [DFA(re) for re in regular_expressions]

    def get_successful_id(self, derivatives: list[_RegularExpression]):
        for index in range(len(derivatives)):
            if _is_epsilon(derivatives[index].nullable()):
                return index
        return True

    def is_failure_state(self, derivatives: list[_RegularExpression]):
        for derivative_ in derivatives:
            if not _is_empty_set(derivative_.simplify()):
                return False
        return True

    def find_records(self):
        i = self.i
        j = self.i
        records = []
        derivatives: list[_RegularExpression] = self.regular_expressions.copy()
        while len(self.source_program) > j:
            symbol = self.source_program[j]
            for i_ in range(len(derivatives)):
                derivatives[i_] = self.dfa_list[i_].transition(derivatives[i_], symbol)
            j = j + 1
            records += [[i, j, derivatives.copy()]]
            if self.is_failure_state(derivatives):
                break
        return records
