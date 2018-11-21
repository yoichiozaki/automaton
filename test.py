# -*- coding: utf-8 -*-

import unittest
from Automaton import DeterministicFiniteAutomaton as DFA
from Automaton import NonDeterministicFiniteAutomaton as NFA


class DFAIsLengthEven(DFA):
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


class DFAEndsUpWith00(DFA):
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


class DFAStartsWithOneAndDividableWith5(DFA):
    """
    test whether the DFA can accept the input which starts with 1 and is a multiple of 5 when viewed as a binary number
    """
    tests = (("101", True),
             ("1010", True),
             ("1111", True),
             ("0", False),
             ("100", False),
             ("111", False))

    def __init__(self):
        s, q0, q1, q2, q3, q4, d = range(7)
        states = {s, q0, q1, q2, q3, q4, d}
        alphabet = {"0", "1"}
        transitions = {
            s: {"0": d, "1": q1},
            q0: {"0": q0, "1": q1},
            q1: {"0": q2, "1": q3},
            q2: {"0": q4, "1": q0},
            q3: {"0": q1, "1": q2},
            q4: {"0": q3, "1": q4},
            d: {"0": d, "1": d},
        }
        initial_state = s
        final_states = {q0}
        super().__init__(states, alphabet, transitions, initial_state, final_states)


class NFAEndsUpWith0xxx(NFA):
    """
    test whether the NFA can accept the input which ends up with a pattern '0xxx'
    """
    tests = (("00000000", True),
             ("000110", True),
             ("1110", False),
             ("01", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d, e = range(5)
        states = {a, b, c, d, e}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"0": {c}, "1": {c}},
            c: {"0": {d}, "1": {d}},
            d: {"0": {e}, "1": {e}},
            e: {},
        }
        initial_state = a
        final_states = {e}
        super().__init__(states, alphabet, transitions, initial_state, final_states)


class NFAHas010(NFA):
    """
    test whether the NFA can accept the input which has a pattern '010'
    """
    tests = (("010", True),
             ("000110", False),
             ("111111001010", True),
             ("111101", False),
             ("1110100110", True))

    def __init__(self):
        a, b, c, d = range(4)
        states = {a, b, c, d}
        alphabet = {"0", "1"}
        transitions = {
            a: {"0": {a, b}, "1": {a}},
            b: {"1": {c}},
            c: {"0": {d}},
            d: {"0": {d}, "1": {d}},
        }
        initial_state = a
        final_states = {d}
        super().__init__(states, alphabet, transitions, initial_state, final_states)


class AutomatonTest(unittest.TestCase):
    automata = [
        DFAIsLengthEven,
        DFAEndsUpWith00,
        DFAStartsWithOneAndDividableWith5,
        NFAEndsUpWith0xxx,
        NFAHas010,
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
