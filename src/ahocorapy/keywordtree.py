'''
Simple ahocorasick implementation entirely written in python.
Supports unicode.

TODO: optimize!

Created on Jan 5, 2016

@author: frederik
'''


class KeywordTree:

    def __init__(self):
        self._zero_state = State(0)
        self._state_count = 1

    def add(self, keyword):
        if len(keyword) <= 0:
            return
        current_state = self._zero_state
        idx = 0
        while current_state.follow(keyword[idx:idx + 1]) is not None:
            current_state = current_state.follow(keyword[idx:idx + 1])
            idx += 1
        while idx < len(keyword):
            new_state = State(self._state_count)
            current_state.add_transition_to(new_state, keyword[idx:idx + 1])
            current_state = new_state
            self._state_count += 1
            idx += 1
        current_state.mark_success(keyword)

    def search(self, text):
        for idx, _ in enumerate(text):
            current_state = self._zero_state
            index = idx
            while current_state.follow(text[index:index + 1]) is not None:
                current_state = current_state.follow(text[index:index + 1])
                if current_state._success:
                    return (current_state._matched_keyword, idx)
                index += 1
        return None

    def __str__(self):
        return "ahocorapy KeywordTree with %i states." % self._state_count


class State:

    def __init__(self, identifier):
        self._success = False
        self._id = identifier
        self._depth = 0
        self._transitions = {}

    def add_transition_to(self, state, symbol):
        self._transitions[symbol] = state

    def follow(self, symbol):
        if symbol in self._transitions:
            return self._transitions[symbol]
        return None

    def mark_success(self, keyword):
        self._success = True
        self._matched_keyword = keyword

    def __str__(self):
        return "ahocorapy State with id %i" +\
               " and %i followers" % (self._id, len(self._transitions))
