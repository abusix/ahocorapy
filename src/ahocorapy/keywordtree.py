'''
Simple ahocorasick implementation entirely written in python.
Supports unicode.

Slightly optimized.

TODO: optimize moar!

Created on Jan 5, 2016

@author: frederik
'''


class KeywordTree:

    def __init__(self):
        self._zero_state = State(0)
        self._state_count = 1
        self._finalized = False

    def add(self, keyword):
        if self._finalized:
            raise ValueError('KeywordTree has been finalized.' +
                             ' No more keyword additions allowed')
        if len(keyword) <= 0:
            return
        current_state = self._zero_state
        idx = 0
        next_state = None
        symbol = keyword[idx:idx + 1]
        if symbol in current_state._transitions:
            next_state = current_state._transitions[symbol]
        while next_state is not None:
            current_state = next_state
            idx += 1
            next_state = None
            symbol = keyword[idx:idx + 1]
            if symbol in current_state._transitions:
                next_state = current_state._transitions[symbol]
        while idx < len(keyword):
            new_state = State(self._state_count)
            current_state._transitions[keyword[idx:idx + 1]] = new_state
            current_state = new_state
            self._state_count += 1
            idx += 1
        current_state._success = True
        current_state._matched_keyword = keyword

    def search(self, text):
        if not self._finalized:
            raise ValueError('KeywordTree has not been finalized.' +
                             ' No search allowed. Call finalize() first.')
        current_state = self._zero_state
        for idx, symbol in enumerate(text):
            next_state = None
            if symbol in current_state._transitions:
                next_state = current_state._transitions[symbol]
            else:
                traversing = current_state
                while next_state is None and\
                        traversing._longest_strict_suffix is not None:
                    next_state = None
                    if symbol in traversing._transitions:
                        next_state = traversing._transitions[symbol]
                    traversing = traversing._longest_strict_suffix
                if next_state is None:
                    next_state = self._zero_state
            current_state = next_state
            if current_state._success:
                keyword = current_state._matched_keyword
                return (keyword, idx + 1 - len(keyword))

    def finalize(self):
        if self._finalized:
            raise ValueError('KeywordTree has already been finalized.')
        finalizer = Finalizer(self)
        finalizer.finalize()
        self._finalized = True

    def __str__(self):
        return "ahocorapy KeywordTree with %i states." % self._state_count


class State:

    def __init__(self, identifier):
        self._success = False
        self._id = identifier
        self._transitions = {}

    def __str__(self):
        return "ahocorapy State with id %i" % self._id +\
               " and %i followers" % len(self._transitions)


class Finalizer:

    def __init__(self, keyword_tree):
        self._keyword_tree = keyword_tree

    def finalize(self):
        zero_state = self._keyword_tree._zero_state
        zero_state._longest_strict_suffix = None
        self.search_longest_strict_suffixes_for_children(zero_state)

    def search_longest_strict_suffixes_for_children(self, state):
        for symbol, child in state._transitions.iteritems():
            traversed = state
            found_suffix = False
            while not found_suffix:
                if traversed._longest_strict_suffix is None or\
                        symbol in traversed._transitions:
                    child._longest_strict_suffix = traversed
                    found_suffix = True
                else:
                    traversed = traversed._longest_strict_suffix
            self.search_longest_strict_suffixes_for_children(child)
