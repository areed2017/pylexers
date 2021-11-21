from pylexers import DerivativeLexer, AtLeastOne, Sigma, _Symbol, _Star, Concat, String

source_program = "12. + 5 - 750.5"
numbers = "0123456789"
alphabet = numbers + "+- "

regular_expressions = [
    AtLeastOne(Sigma(numbers)),
    Concat(AtLeastOne(Sigma(numbers)), Concat(_Symbol("."), _Star(Sigma(numbers)))),
    _Symbol("+"),
    _Symbol("-"),
    _Symbol(" "),
]

tokenizing_functions = [
    lambda lexeme: ["INT", lexeme, int(lexeme)],
    lambda lexeme: ["DOUBLE", lexeme, float(lexeme)],
    lambda lexeme: ["PLUS", lexeme, None],
    lambda lexeme: ["MINUS", lexeme, None],
    lambda lexeme: ["IGNORE", lexeme, None]
]


lexer = DerivativeLexer(regular_expressions, tokenizing_functions)
for token in lexer.set_source_program(source_program):
    print(token)
