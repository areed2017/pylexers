from PyLexer import AtLeastOne, Sigma, Symbol, NFALexer

source_program = "12 + 5 - 750"
numbers = "0123456789"
alphabet = numbers + "+- "

regular_expressions = [
    AtLeastOne(Sigma(numbers)),
    Symbol("+"),
    Symbol("-"),
    Symbol(" "),
]

tokenizing_functions = [
    lambda lexeme: ["INT", lexeme, int(lexeme)],
    lambda lexeme: ["DOUBLE", lexeme, float(lexeme)],
    lambda lexeme: ["PLUS", lexeme, None],
    lambda lexeme: ["MINUS", lexeme, None],
    lambda lexeme: ["IGNORE", lexeme, None]
]


lexer = NFALexer(regular_expressions, tokenizing_functions)
for token in lexer.set_source_program(source_program):
    print(token)
