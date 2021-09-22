from BaseLexer import Lexer
from DerivativeLexer.derivative import derivative, nullable
from RegularExpressions.util import _is_epsilon


class DerivativeLexer(Lexer):

    def get_successful_id(self, derivatives):
        for index in range(len(derivatives)):
            if _is_epsilon(nullable(derivatives[index])):
                return index
        return True

    def is_failure_state(self, derivatives):
        for derivative_ in derivatives:
            if _is_epsilon(nullable(derivative_)):
                return False
        return True

    def find_records(self):
        i = self.i
        j = self.i
        records = []
        derivatives = self.regular_expressions.copy()
        while len(self.source_program) > j:
            symbol = self.source_program[j]
            derivatives = [derivative(re, symbol) for re in derivatives]
            j = j + 1
            records += [[i, j, derivatives.copy()]]
            if self.is_failure_state(derivatives):
                break
        return records
