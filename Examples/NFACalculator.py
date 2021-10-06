from BaseLexer import build_token_func
from DerivativeLexer import DerivativeLexer
from PyLexer import AtLeastOneRegularExpression, KleeneStarRegularExpression, StringRegularExpression, \
    SigmaRegularExpression, SymbolRegularExpression, ConcatRegularExpression, OrRegularExpression, \
    NFALexer

source_program = "12 + 5 - 750"
numbers = "0123456789"
alphabet = numbers + ".+- "

number_re = AtLeastOneRegularExpression(SigmaRegularExpression(numbers))
regular_expressions = [
    number_re,
    ConcatRegularExpression(number_re, ConcatRegularExpression(SymbolRegularExpression("."), number_re)),
    StringRegularExpression("ans"),
    SymbolRegularExpression("+"),
    SymbolRegularExpression("-"),
    SymbolRegularExpression("*"),
    SymbolRegularExpression("/"),
    StringRegularExpression("//"),
    SymbolRegularExpression(" "),
]

tokenizing_functions = [
    build_token_func("INT", int),
    build_token_func("DOUBLE", float),
    build_token_func("ANS"),
    build_token_func("PLUS"),
    build_token_func("MINUS"),
    build_token_func("STAR"),
    build_token_func("SLASH"),
    build_token_func("2-SLASH"),
    build_token_func("IGNORE"),
]


def process_tokens(lexer, ans):
    last_number = None
    operation = None
    for token in lexer:
        if token[0] == "INT" or token[0] == "DOUBLE":
            if operation:
                last_number = operation(last_number, token[2])
                operation = None
            else:
                last_number = token[2]
        if token[0] == "PLUS":
            operation = lambda a, b: a + b
        if token[0] == "MINUS":
            operation = lambda a, b: a - b
        if token[0] == "STAR":
            operation = lambda a, b: a * b
        if token[0] == "SLASH":
            operation = lambda a, b: a / b
        if token[0] == "2-SLASH":
            operation = lambda a, b: a // b
        if token[0] == "ANS":
            last_number = ans
    return last_number


if __name__ == '__main__':
    lexer = NFALexer(regular_expressions, tokenizing_functions)
    user_input = ""
    ans = 0
    while user_input != "quit":
        user_input = input("> ")
        lexer.set_source_program(user_input)
        ans = process_tokens(lexer, ans)
        print(ans)
