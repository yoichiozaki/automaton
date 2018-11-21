# -*- coding: utf-8 -*-
class Automaton(object):
    """
    the base class of automaton
    """

    def __init__(self, states, alphabet, transitions, initial_state, final_state):
        self.states = frozenset(states)
        self.alphabet = frozenset(alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = frozenset(final_state)

    def __eq__(self, other):
        return self.states == other.states and \
               self.alphabet == other.alphabet and \
               self.transitions == other.transitions and \
               self.initial_state == other.initial_state and \
               self.final_states == other.final_states

    def __repr__(self):
        str_transitions = "\n\t\t\t"
        for key, val in self.transitions.items():
            str_transitions += str(key).replace("\n", "") \
                               + " : " + str(val).replace("\n", "") \
                               + "\n\t\t\t"
        ans = """Automaton
        states          : %s
        alphabet        : %s
        transitions     : %s
        initial_state   : %s
        final_states    : %s
        """ % (str(self.states).replace("\n", ""),
               str(self.alphabet).replace("\n", ""),
               str_transitions,
               str(self.initial_state).replace("\n", ""),
               str(self.final_states).replace("\n", ""))
        ans = ans.replace("frozenset()", "frozenset({})")
        ans = ans.replace("frozenset({", "{")
        ans = ans.replace("})", "}")
        return ans


class DeterministicFiniteAutomaton(Automaton):
    """
    Deterministic Finite Automaton
    """

    def run(self, inputs):
        """
        check whether the input is the language of this DFA.
        :param inputs:
        :return:
        """
        state = self.initial_state
        for character in inputs:
            if character not in self.alphabet:
                print("ERROR: %s not in alphabet" % character)
                return False
            else:
                state = self.transitions[state][character]
        return state in self.final_states


class NonDeterministicFiniteAutomaton(Automaton):
    """
    Non Deterministic Finite Automaton
    """

    def run(self, inputs):
        """
        check whether the input is the language of this NFA.
        :param inputs:
        :return:
        """
        states = {self.initial_state}
        for character in inputs:
            if character not in self.alphabet:
                print("ERROR: %s not in alphabet" % character)
                return False
            else:
                states = self.next_states(states, character)
        return len(states.intersection(self.final_states)) != 0

    def next_states(self, states, character):
        """
        return set of next states.
        :param states:
        :param character:
        :return: next_state:
        """
        next_states = set()
        for state in states:
            next_states = next_states.union(self.transitions[state].get(character, frozenset()))
        return frozenset(next_states)
