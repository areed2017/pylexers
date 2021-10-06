from RegularExpressions import _RegularExpression
from RegularExpressions.util import _build_empty_set


class DFA:
    def __init__(self, regular_expression: _RegularExpression):
        alphabet = regular_expression.get_alphabet()
        self.states: dict[_RegularExpression, dict] = dict()
        queue = {regular_expression}
        while len(queue) > 0:
            current = queue.pop()
            if current in self.states:
                continue
            self.states[current] = dict()
            for symbol in alphabet:
                self.states[current][symbol] = current.derivative(symbol).simplify()
                queue.add(self.states[current][symbol])

        if _build_empty_set() not in self.states.keys():
            self.states[_build_empty_set()] = dict()

    def transition(self, state: _RegularExpression, symbol: chr):
        if state not in self.states:
            raise ValueError("Unknown State given to DFA")
        if symbol not in self.states[state]:
            return _build_empty_set()
        return self.states[state][symbol]
