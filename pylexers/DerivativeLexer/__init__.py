from pylexers.BaseLexer import Lexer
from pylexers.RegularExpressions.util import _is_epsilon, _RegularExpression, _is_empty_set


class DerivativeLexer(Lexer):
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
            derivatives = [re.derivative(symbol) for re in derivatives]
            j = j + 1
            records += [[i, j, derivatives.copy()]]
            if self.is_failure_state(derivatives):
                break
        return records
