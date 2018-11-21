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

    def run(self, input_string):
        """
        check whether the input is the language of this DFA.
        :param input_string:
        :return:
        """
        state = self.initial_state
        for character in input_string:
            if character not in self.alphabet:
                print("ERROR: %s not in alphabet" % character)
                return False
            else:
                state = self.transitions[state][character]
        return state in self.final_states

    def flipped_dfa(self):
        """
        return a DFA whose language is flipped over
        :return:
        """
        final_states = set([x for x in self.states if x not in self.final_states])
        return DeterministicFiniteAutomaton(self.states,
                                            self.alphabet,
                                            self.transitions,
                                            self.initial_state,
                                            final_states)

    def minimized(self):
        """
        return the DFA with the minimized number of states
        :return:
        """
        marked = set()
        unmarked = set()
        checked = set()
        for p in self.states:
            for q in self.states:
                if frozenset({p, q}) in checked or p == q:
                    continue
                if (p in self.final_states and q not in self.final_states) or \
                        (q in self.final_states and p not in self.final_states):
                    marked.add(frozenset({p, q}))
                else:
                    unmarked.add(frozenset({p, q}))
                checked.add(frozenset({p, q}))
                checked.add(frozenset({q, p}))

        flag = True
        while flag:
            flag = False
            for p, q in unmarked:
                for s in self.alphabet:
                    if frozenset({self.transitions[p][s], self.transitions[q][s]}) in marked:
                        flag = True
                        marked.add(frozenset({p, q}))
                        unmarked.remove(frozenset({p, q}))
                        break
                if flag:
                    break

        states_dict = {}
        for p in self.states:
            states_dict[p] = {p}
        for p in self.states:
            for q in self.states:
                if frozenset({p, q}) in unmarked:
                    states_dict[p].add(q)
                    states_dict[q].add(p)

        states = set()
        initial_state = None
        final_states = set()
        transitions = {}
        for p in self.states:
            state = frozenset(states_dict[p])
            if state in states:
                continue
            states.add(state)
            transitions[state] = {}
            for s in self.alphabet:
                transitions[state][s] = states_dict[self.transitions[next(iter(state))][s]]
            if self.initial_state in state:
                initial_state = state
            if len(self.final_states.intersection(state)) != 0:
                final_states.add(state)
        alphabet = self.alphabet
        return DeterministicFiniteAutomaton(states, alphabet, transitions, initial_state, final_states)


class NonDeterministicFiniteAutomaton(Automaton):
    """
    Non Deterministic Finite Automaton
    """

    def run(self, input_string):
        """
        check whether the input is the language of this NFA.
        :param input_string:
        :return:
        """
        states = {self.initial_state}
        for character in input_string:
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

    def convert_to_dfa(self):
        """
        convert self to equivalent DFA.
        :return:
        """
        states = {frozenset({self.initial_state})}
        transitions = {}
        to_search = {frozenset({self.initial_state})}
        searched = set()
        while len(to_search) != 0:
            searching = to_search.pop()
            searched.add(searching)
            for char in self.alphabet:
                reachable_states = self.next_states(searching, char)
                states.add(reachable_states)
                if reachable_states not in searched:
                    to_search.add(reachable_states)
                if not transitions.get(searching):
                    transitions[searching] = {}
                transitions[searching][char] = frozenset(reachable_states)

        final_states = set([x for x in states if len(self.final_states.intersection(x)) != 0])
        initial_state = frozenset({self.initial_state})
        alphabet = self.alphabet
        return DeterministicFiniteAutomaton(states, alphabet, transitions, initial_state, final_states)


class NFAWithEpsTransition(Automaton):
    """
    NFA with epsilon transition
    """

    def reachable_states_with_one_eps_from(self, state):
        """
        return a set of states which are reachable from input 'state' with one epsilon transition.
        :param state:
        :return:
        """
        return frozenset(self.transitions[state].get(-1, {}))

    def reachable_states_with_multi_eps_from(self, state):
        """
        return a set of states which are reachable from input 'state' with multi epsilon transitions.
        :param state:
        :return:
        """
        ans = frozenset([state])
        reachable_states = self.reachable_states_with_one_eps_from(state)
        while not reachable_states.issubset(ans):
            ans = ans.union(reachable_states)
            new_reachable_states = frozenset()
            for reachable_state in reachable_states:
                new_reachable_states \
                    = new_reachable_states.union(self.reachable_states_with_one_eps_from(reachable_state))
            reachable_states = new_reachable_states
        return ans

    def next_states(self, states, character):
        """
        return a set of states which is the next state from 'states' when read 'character'
        :param states:
        :param character:
        :return:
        """
        next_states = frozenset()
        for state in states:
            for reachable_state in self.transitions[state].get(character, frozenset()):
                next_states = next_states.union(self.reachable_states_with_multi_eps_from(reachable_state))
        return frozenset(next_states)

    def run(self, input_string):
        """
        check whether the eps-NFA can accept the input.
        :param input_string:
        :return:
        """
        states = self.reachable_states_with_multi_eps_from(self.initial_state)
        for character in input_string:
            if character not in self.alphabet:
                print("ERROR: %s not in alphabet" % character)
                return False
            else:
                states = self.next_states(states, character)
        return len(states.intersection(self.final_states)) != 0

    def convert_to_dfa(self):
        """
        convert self to equivalent DFA.
        :return:
        """
        states = {self.reachable_states_with_multi_eps_from(self.initial_state)}
        transitions = {}
        to_search = {self.reachable_states_with_multi_eps_from(self.initial_state)}
        searched = set()
        while len(to_search) != 0:
            searching = to_search.pop()
            searched.add(searching)
            for character in self.alphabet:
                reachable_states = self.next_states(searching, character)
                states.add(reachable_states)
                if reachable_states not in searched:
                    to_search.add(reachable_states)
                if not transitions.get(searching):
                    transitions[searching] = {}
                transitions[searching][character] = frozenset(reachable_states)

        final_states = set([x for x in states if len(self.final_states.intersection(x)) != 0])
        initial_state = self.reachable_states_with_multi_eps_from(self.initial_state)
        alphabet = self.alphabet
        return DeterministicFiniteAutomaton(states, alphabet, transitions, initial_state, final_states)


    @staticmethod
    def connect_serially(automata):
        """
        connect multiple automatata serially.
        :param automata:
        :return:
        """
        alphabet = set()
        states = set()
        transitions = {}
        for i, automaton in enumerate(automata):
            alphabet = alphabet.union(automaton.alphabet)
            states = states.union(set([(i, state) for state in automaton.states]))
            for final_state in automaton.final_states:
                transitions[(i, final_state)] = {}
            for state, trans_dict in automaton.transitions.items():
                transitions[(i, state)] = {}
                for character, states_transit_to in trans_dict.items():
                    transitions[(i, state)][character] = frozenset([(i, state) for state in states_transit_to])

            if i == 0:
                continue
            for pre_final_state in automata[i-1].final_state:
                transitions[(i - 1, pre_final_state)][-1] = frozenset([(i, automaton.init_state)])

        initial_state = (0, automata[0].initial_state)
        final_states = set([(len(automata) - 1, f) for f in automata[-1].final_states])
        return NFAWithEpsTransition(states, alphabet, transitions, initial_state, final_states)

    @staticmethod
    def connect_parallel(automata):
        """
        connect multiple automata parallel.
        :param automata:
        :return:
        """
        initial_state = 1
        alphabet = set()
        states = {(initial_state, -1)}
        transitions = {}
        final_states = set()
        for i, automaton in enumerate(automata):
            alphabet = alphabet.union(automaton.alphabet)
            states = states.union(set([(i, state) for state in automaton.states]))
            for state, trans_dict in automaton.transitions.items():
                transitions[(i, state)] = {}
                for character, states_transit_to in trans_dict.items():
                    transitions[(i, state)][character] = frozenset([(i, state) for state in states_transit_to])
            final_states = final_states.union(set([(i, final_state) for final_state in automaton.final_states]))
        transitions[initial_state] = {}
        transitions[initial_state][-1] = frozenset([(i, automaton.init_state) for i, automaton in enumerate(automata)])
        return NFAWithEpsTransition(states, alphabet, transitions, initial_state, final_states)