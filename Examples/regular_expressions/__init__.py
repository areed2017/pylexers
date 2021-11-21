import dataclasses
from typing import Optional

from pylexers import String, NFALexer, _Symbol, Sigma
from SymbolTable import SymbolTable
from parse_tree import build_regular_expression

regular_expressions = [
    String("\d"),
    String("\D"),
    String("\s"),
    String("\S"),
    String("\w"),
    String("\W"),
    _Symbol("*"),
    _Symbol("|"),
    _Symbol("("),
    _Symbol(")"),
    Sigma(exclude="*"),
]

tokenizing_functions = [
    lambda lexeme: "DIGIT",
    lambda lexeme: "NON-DIGIT",
    lambda lexeme: "WHITE-SPACE",
    lambda lexeme: "NON-WHITE-SPACE",
    lambda lexeme: "ALPHA-NUMERIC",
    lambda lexeme: "NON-ALPHA-NUMERIC",
    lambda lexeme: "STAR",
    lambda lexeme: "OR",
    lambda lexeme: "OPEN-PAREN",
    lambda lexeme: "CLOSE-PAREN",
    lambda lexeme: ["SYMBOL", lexeme],
]


lexer = NFALexer(regular_expressions, tokenizing_functions)


@dataclasses.dataclass
class Match:
    span: tuple[int, int]
    match: str


class CompiledRegularExpression:
    def __init__(self, pattern: str):
        lex = lexer.set_source_program(pattern)
        self.regular_expression = build_regular_expression(lex, SymbolTable())

    def match(self, string) -> Optional[Match]:
        for i in range(len(string) + 1):
            for j in range(len(string) + 1, i, -1):
                s = string[i: j]
                if self.regular_expression.matches(s):
                    return Match(span=(i, j), match=s)
        return None


def compile(pattern: str) -> CompiledRegularExpression:
    return CompiledRegularExpression(pattern)


if __name__ == '__main__':
    import time
    import re

    start = time.time()
    r = compile("ab*")
    for _ in range(100):
        r = compile("ab*")
    end = time.time()
    print(f"My Compile Time: {end - start} Seconds")

    start = time.time()
    for _ in range(100):
        r.match("abbbb")
    end = time.time()
    print(f"My Parse Time: {end - start} Seconds")

    start = time.time()
    r = re.compile("ab*")
    for _ in range(100):
        r = re.compile("ab*")
    end = time.time()
    print(f"Python RE Compile Time: {end - start} Seconds")

    start = time.time()
    for _ in range(100):
        r.match("abbbb")
    end = time.time()
    print(f"Python RE Parse Time: {end - start} Seconds")

