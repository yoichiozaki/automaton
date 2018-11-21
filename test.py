# -*- coding: utf-8 -*-

import unittest
from Automaton import DeterministicFiniteAutomaton as DFA
from Automaton import NonDeterministicFiniteAutomaton as NFA


class IsLengthEven(DFA):
    """
    test whether the DFA can accept the input which length is even.
    """

    tests = (("0111", True),
             ("1", False),
             ("", True),
             ("0011011", False))

    def __init__(self):
        a, b = range(2)
        states = {a, b}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": b, "1": b},
            b: {"0": a, "1": a},
        }
        initial_state = a
        final_states = {a}
        super().__init__(states, alphabet, transitions, initial_state, final_states)


class EndsUpWith00(DFA):
    """
    test whether the DFA can accept the input which ends up with 00.
    """
    tests = (("00100", True),
             ("11", False),
             ("1101000110100100", True))

    def __init__(self):
        a, b, c = range(3)
        states = {a, b, c}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": b, "1": a},
            b: {"0": c, "1": a},
            c: {"0": c, "1": a},
        }
        initial_state = a
        final_states = {c}
        super().__init__(states, alphabet, transitions, initial_state, final_states)


class AutomatonTest(unittest.TestCase):
    automata = [
        IsLengthEven,
        EndsUpWith00
    ]

    def test_automaton(self):
        for automaton in self.automata:
            print(str(automaton).center(70, "-"))
            instance = automaton()
            print(instance)
            for inputs, expected in instance.tests:
                result = instance.run(inputs)
                print("%s: %s" % (str(result).ljust(5), inputs))
                self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
