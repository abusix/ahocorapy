'''
Ahocorasick implementation entirely written in python.
Supports unicode.

Quite optimized, the code may not be as beautiful as you like,
since inlining and so on was necessary

This library is optimized for the cPython interpreter.
I will most likely run slower with pypy, etc.

Created on Jan 5, 2016

@author: Frederik Petersen (fp@abusix.com)
'''


class KeywordTree:

    def __init__(self):
        self._zero_state = {
            'id': 0, 'success': False, 'transitions': {}, 'parent': None}
        self._finalized = False
        self._states = [self._zero_state]

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
        if symbol in current_state['transitions']:
            next_state = self._states[current_state['transitions'][symbol]]
        while next_state is not None:
            current_state = next_state
            idx += 1
            next_state = None
            symbol = keyword[idx:idx + 1]
            if symbol in current_state['transitions']:
                next_state = self._states[current_state['transitions'][symbol]]
        while idx < len(keyword):
            new_state = {
                'id': len(self._states), 'success': False, 'transitions': {},
                'parent': current_state['id']}
            current_state['transitions'][
                keyword[idx:idx + 1]] = len(self._states)
            self._states.append(new_state)
            current_state = new_state
            idx += 1
        current_state['success'] = True
        current_state['matched_keyword'] = keyword

    def search(self, text):
        if not self._finalized:
            raise ValueError('KeywordTree has not been finalized.' +
                             ' No search allowed. Call finalize() first.')
        current_state = self._zero_state
        for idx, symbol in enumerate(text):
            if symbol in current_state['transitions']:
                current_state = self._states[
                    current_state['transitions'][symbol]]
                if current_state['success']:
                    keyword = current_state['matched_keyword']
                    return (keyword, idx + 1 - len(keyword))
            else:
                current_state = self._zero_state

    def finalize(self):
        if self._finalized:
            raise ValueError('KeywordTree has already been finalized.')
        finalizer = Finalizer(self)
        finalizer.finalize()
        self._finalized = True

    def __str__(self):
        return "ahocorapy KeywordTree with %i states." % self._state_count

    def __repr__(self):
        return self.dump()

    def dump(self):
        tree = {}
        tree['states'] = self._states
        tree['finalized'] = self._finalized
        return tree

    def load(self, tree):
        self._states = tree['states']
        self._zero_state = self._states[0]
        self._finalized = tree['finalized']


class Finalizer:

    def __init__(self, keyword_tree):
        self._keyword_tree = keyword_tree
        self._states = keyword_tree._states

    def finalize(self):
        zero_state = self._keyword_tree._zero_state
        zero_state['longest_strict_suffix'] = None
        self.search_longest_strict_suffixes_for_children(zero_state)
        shortcut = self.shortcut_suffix_search
        for state in self._states:
            if state['id'] > 0:
                shortcut(state)
        # Remove to save space
        for state in self._states:
            # Only needed during finalize
            del state['longest_strict_suffix']
            del state['parent']
            # Remove since we only need one result
            if state['success']:
                del state['transitions']

    def shortcut_suffix_search(self, state):
        traversing = self._states[state['longest_strict_suffix']]
        while traversing['id'] > 0:
            for symbol_in_suffix in traversing['transitions']:
                if symbol_in_suffix not in state['transitions']:
                    state['transitions'][symbol_in_suffix] =\
                        traversing['transitions'][symbol_in_suffix]
            traversing = self._states[traversing['longest_strict_suffix']]

    def search_longest_strict_suffixes_for_children(self, state):
        for symbol, childid in state['transitions'].iteritems():
            child = self._states[childid]
            self.search_longest_strict_suffix(child, symbol)
            self.search_longest_strict_suffixes_for_children(child)

    def search_longest_strict_suffix(self, state, symbol):
        if 'longest_strict_suffix' not in state:
            parent = self._states[state['parent']]
            if parent['id'] == 0:
                state['longest_strict_suffix'] = 0
            else:
                found_suffix = False
                if 'longest_strict_suffix' not in parent:
                    # Has not been done yet. Do early
                    self.search_longest_strict_suffix(parent, symbol)
                traversed = self._states[parent['longest_strict_suffix']]
                while not found_suffix:
                    if symbol in traversed['transitions']:
                        state['longest_strict_suffix'] = traversed[
                            'transitions'][symbol]
                        found_suffix = True
                    elif traversed['id'] == 0:
                        state['longest_strict_suffix'] = 0
                        found_suffix = True
                    else:
                        if 'longest_strict_suffix' not in traversed:
                            # Has not been done yet. Do early
                            self.search_longest_strict_suffix(
                                traversed, symbol)
                        traversed = self._states[
                            traversed['longest_strict_suffix']]
