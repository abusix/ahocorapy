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
        next_state = current_state.follow(keyword[idx:idx + 1])
        while next_state is not None:
            current_state = next_state
            idx += 1
            next_state = current_state.follow(keyword[idx:idx + 1])
        while idx < len(keyword):
            new_state = State(self._state_count)
            current_state.add_transition_to(new_state, keyword[idx:idx + 1])
            current_state = new_state
            self._state_count += 1
            idx += 1
        current_state.mark_success(keyword)

    def search(self, text):
        if not self._finalized:
            raise ValueError('KeywordTree has not been finalized.' +
                             ' No search allowed. Call finalize() first.')
        for idx, _ in enumerate(text):
            current_state = self._zero_state
            index = idx
            next_state = current_state.follow(text[index:index + 1])
            while next_state is not None:
                current_state = next_state
                if current_state._success:
                    return (current_state._matched_keyword, idx)
                index += 1
                next_state = current_state.follow(text[index:index + 1])
        return None

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

    def add_transition_to(self, state, symbol):
        self._transitions[symbol] = state

    def follow(self, symbol):
        if symbol in self._transitions:
            return self._transitions[symbol]
        return None

    def mark_success(self, keyword):
        self._success = True
        self._matched_keyword = keyword

    def _has_transition_with_symbol(self, symbol):
        if symbol in self._transitions:
            return True
        return False

    def __str__(self):
        return "ahocorapy State with id %i" +\
               " and %i followers" % (self._id, len(self._transitions))


class Finalizer:

    def __init__(self, keyword_tree):
        self._keyword_tree = keyword_tree

    def finalize(self):
        zero_state = self._keyword_tree._zero_state
        zero_state._longest_strict_suffix = None
        self.search_longest_strict_suffixes(zero_state)
        zero_state._dict_suffix = None
        self.search_dict_suffix(zero_state)

    def search_longest_strict_suffixes(self, state):
        for symbol, child in state._transitions.iteritems():
            traversed = state
            found_suffix = False
            while not found_suffix:
                if traversed._longest_strict_suffix is None or\
                        traversed._has_transition_with_symbol(symbol):
                    child._longest_strict_suffix = traversed
                    found_suffix = True
                else:
                    traversed = traversed._longest_strict_suffix
            self.search_longest_strict_suffixes(child)

    def search_dict_suffix(self, state):
        for child in state._transitions.itervalues():
            if child._success:
                # No need. We only want one match. Increase performance
                continue
            traversed = child
            done = False
            while not done:
                if traversed._longest_strict_suffix is None:
                    child._dict_suffix = None
                    done = True
                elif traversed._success:
                    child._dict_suffix = traversed
                    done = True
                else:
                    traversed = traversed._longest_strict_suffix
            self.search_dict_suffix(child)
