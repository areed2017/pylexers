import random
import time
import matplotlib.pyplot as plt
from pylexers import AtLeastOne, Sigma, Symbol, DFALexer, Star, Concat, NFALexer, DerivativeLexer

numbers = "0123456789"
alphabet = numbers + "+- "


regular_expressions = []
tokenizing_functions = []
dfa_timing = []
nfa_timing = []
derivative_timing = []


def average_time(regular_expressions, tokenizing_functions, lexer):
    data = []
    for _ in range(10):
        start = time.time()
        lexer(regular_expressions, tokenizing_functions)
        end = time.time()
        data += [end - start]
    return sum(data) / len(data)


for i in range(40):
    print(f"Construction Cycle {i}")
    regular_expressions += [Concat(AtLeastOne(Sigma(numbers)), Concat(Symbol("."), Star(Sigma(numbers))))]
    tokenizing_functions += [lambda lexeme: ["DOUBLE", lexeme, float(lexeme)]]

    dfa_timing += [average_time(regular_expressions, tokenizing_functions, DFALexer)]
    nfa_timing += [average_time(regular_expressions, tokenizing_functions, NFALexer)]
    derivative_timing += [average_time(regular_expressions, tokenizing_functions, DerivativeLexer)]


# plt.title("Lexer Construction Time")
# plt.plot(dfa_timing)
# plt.plot(nfa_timing)
# plt.plot(derivative_timing)
# plt.legend(["DFA", "NFA", "Derivative"])
# plt.show()

"""Parsing"""

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
    lambda lexeme: ["PLUS", lexeme, None],
    lambda lexeme: ["MINUS", lexeme, None],
    lambda lexeme: ["IGNORE", lexeme, None]
]


def average_time(regular_expressions, tokenizing_functions, lexer):
    data = []
    for _ in range(10):
        lex = lexer(regular_expressions, tokenizing_functions)
        start = time.time()
        for _ in lex.set_source_program(source_program):
            pass
        end = time.time()
        data += [end - start]
    return sum(data) / len(data)


for _ in range(10):
    number = str(random.randint(0, 1000))
    source_program += random.choice([number, " ", "+"])


for i in range(1):
    print(f"Parsing Cycle {i}")
    number = str(random.randint(0, 1000))
    source_program += random.choice([number, " ", "+"])

    dfa_timing += [average_time(regular_expressions, tokenizing_functions, DFALexer)]
    nfa_timing += [average_time(regular_expressions, tokenizing_functions, NFALexer)]
    derivative_timing += [average_time(regular_expressions, tokenizing_functions, DerivativeLexer)]



# plt.title("Lexer Construction Time")
# plt.plot(dfa_timing[10:])
# plt.plot(nfa_timing[10:])
# plt.plot(derivative_timing[10:])
# plt.legend(["DFA", "NFA", "Derivative"])
# plt.show()
