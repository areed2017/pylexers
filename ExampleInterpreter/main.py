import string

from BaseLexer import Lexer
from PyLexer import AtLeastOne, Concat, Sigma, Symbol, Star, DerivativeLexer, Or, DFALexer, NFALexer
from PySymbolTable import SymbolTable

example_file = """
set('i', 100)
display(i)
"""

numbers = string.digits
letters = string.ascii_lowercase + string.ascii_uppercase

regular_expressions = [
    Or(Symbol(" "), Symbol("\n")),
    AtLeastOne(Sigma(letters)),
    Concat(Symbol("'"), Concat(Star(Sigma("i")), Symbol("'"))),
    AtLeastOne(Sigma(numbers)),
    Concat(AtLeastOne(Sigma(numbers)), Concat(Symbol("."), Star(Sigma(numbers)))),
    Symbol(","),
    Symbol("+"),
    Symbol("-"),
    Symbol("*"),
    Symbol("/"),
    Symbol("<"),
    Symbol("<="),
    Symbol(">"),
    Symbol(">="),
    Symbol("("),
    Symbol(")"),
]

tokenizing_functions = [
    lambda lexeme: None,
    lambda lexeme: ["ID", lexeme, lexeme],
    lambda lexeme: ["STRING", lexeme, str(lexeme)],
    lambda lexeme: ["INT", lexeme, int(lexeme)],
    lambda lexeme: ["DOUBLE", lexeme, float(lexeme)],
    lambda lexeme: None,
    lambda lexeme: ["PLUS", lexeme, None],
    lambda lexeme: ["MINUS", lexeme, None],
    lambda lexeme: ["TIMES", lexeme, None],
    lambda lexeme: ["DIVIDE", lexeme, None],
    lambda lexeme: ["LESS_THAN", lexeme, None],
    lambda lexeme: ["LESS_THAN_EQ", lexeme, None],
    lambda lexeme: ["GREATER_THAN", lexeme, None],
    lambda lexeme: ["GREATER_THAN_EQ", lexeme, None],
    lambda lexeme: ["OPEN_PAREN", lexeme, None],
    lambda lexeme: ["CLOSE_PAREN", lexeme, None],
]

# Syntax Tree


def value(lexer: Lexer, symbol_table: SymbolTable):
    token = lexer.peek()
    if token[0] in ["INT", "DOUBLE"]:
        return ['VALUE', next(lexer)[2]]
    if token[0] == "STRING":
        return ['VALUE', next(lexer)[2][1:-1]]
    return None


def identifier(lexer: Lexer, symbol_table: SymbolTable):
    token = lexer.peek()
    if token[0] == "ID":
        token = next(lexer)
        return ["ID", token[2], lambda: symbol_table.get_identifier(token[2])]
    return None


def arg_list(lexer: Lexer, symbol_table: SymbolTable):
    arg_list_ = []
    if next(lexer)[0] != "OPEN_PAREN":
        raise SyntaxError("Expected open parenthesis")
    try:
        while True:
            token = lexer.peek()
            if token[0] == "CLOSE_PAREN":
                next(lexer)
                return arg_list_
            arg_list_ += [
                value(lexer, symbol_table) or \
                identifier(lexer, symbol_table)
            ]

    except StopIteration:
        raise SyntaxError("Unexpected EOF")


def call_function(lexer: Lexer, symbol_table: SymbolTable):
    peek_1 = lexer.peek(1)
    peek_2 = lexer.peek(2)
    if peek_1 and peek_2 and peek_1[0] == "ID" and peek_2[0] == "OPEN_PAREN":
        token = next(lexer)
        function_ = symbol_table.get_identifier(token[2])
        args = arg_list(lexer, symbol_table)
        return ['FUNCTION_CALL', function_, args]
    return None


def statement(lexer: Lexer, symbol_table: SymbolTable):
    return call_function(lexer, symbol_table)


def statement_list(lexer: Lexer, symbol_table: SymbolTable):
    if stmt := statement(lexer, symbol_table):
        return [stmt] + statement_list(lexer, symbol_table)
    return []


def execute_(statement):
    if statement[0] == "VALUE":
        return statement[1]
    if statement[0] == "ID":
        return statement[-1]()
    if statement[0] == "FUNCTION_CALL":
        args = [execute_(arg) for arg in statement[2]]
        return statement[1](*args)


def execute(statement_list):
    for statement in statement_list:
        if statement:
            execute_(statement)


class ExampleSymbolTable(SymbolTable):

    def __init__(self, parent=None):
        self.parent = parent
        self.identifiers = dict()

        def _set(id, value):
            self.add_identifier(id, value, type(value))

        def _display(*values):
            print(*values)

        self.add_identifier('set', _set, "func")
        self.add_identifier('display', _display, "func")


lexer = DerivativeLexer(regular_expressions, tokenizing_functions)
symbol_table = ExampleSymbolTable()
stmt_list = statement_list(lexer.set_source_program(example_file), symbol_table)
execute(stmt_list)
