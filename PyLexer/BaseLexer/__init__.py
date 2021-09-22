
class Lexer:
    def __init__(self, regular_expressions: list, tokenize_functions: list):
        self.regular_expressions = [r.re for r in regular_expressions]
        self.tokenize_functions = tokenize_functions
        self.source_program = ""

    def set_source_program(self, source_program):
        self.source_program = source_program

    def find_records(self):
        return []

    def get_successful_id(self, states):
        return -1

    def is_failure_state(self, derivatives):
        return True

    def __iter__(self, **kwargs):
        self.i = 0
        return self

    def __next__(self):
        if len(self.source_program) <= self.i:
            raise StopIteration
        records = self.find_records()
        for record in records[::-1]:
            if not self.is_failure_state(record[2]):
                lexeme = self.source_program[record[0]: record[1]]
                token_function_id = self.get_successful_id(record[2])
                self.i = record[1]
                return self.tokenize_functions[token_function_id](lexeme)
        raise StopIteration


def build_token_func(identifier, process_lexeme_func=None):
    if process_lexeme_func:
        return lambda lexeme: [identifier, lexeme, process_lexeme_func(lexeme)]
    return lambda lexeme: [identifier, lexeme, None]
