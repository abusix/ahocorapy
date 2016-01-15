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

from array import array


class KeywordTree:

    def __init__(self, case_insensitive=False):
        self._zero_state = {
            'id': 0, 'success': False, 'transitions': array('i', [-1] * 5), 'parent': None}
        self._finalized = False
        self._states = [self._zero_state]
        self._symbols = {}
        self._symbol_list = []
        self._case_insensitive = case_insensitive

    def add(self, keyword):
        if self._finalized:
            raise ValueError('KeywordTree has been finalized.' +
                             ' No more keyword additions allowed')
        original_keyword = keyword
        if self._case_insensitive:
            keyword = keyword.lower()
        if len(keyword) <= 0:
            return
        current_state = self._zero_state
        idx = 0
        next_state = None
        symbol = keyword[idx:idx + 1]
        if symbol not in self._symbols:
            self._symbols[symbol] = len(self._symbols)
            self._symbol_list.append(symbol)
        symbol_id = self._symbols[symbol]
        if len(current_state['transitions']) > symbol_id\
                and current_state['transitions'][symbol_id] >= 0:
            next_state = self._states[current_state['transitions'][symbol_id]]
        while next_state is not None:
            current_state = next_state
            idx += 1
            next_state = None
            symbol = keyword[idx:idx + 1]
            if symbol not in self._symbols:
                self._symbols[symbol] = len(self._symbols)
                self._symbol_list.append(symbol)
            symbol_id = self._symbols[symbol]
            if len(current_state['transitions']) > symbol_id\
                    and current_state['transitions'][symbol_id] >= 0:
                next_state = self._states[
                    current_state['transitions'][symbol_id]]
        while idx < len(keyword):
            new_state = {
                'id': len(self._states), 'success': False,
                'transitions': array('i', [-1] * 5),
                'parent': current_state['id']}
            symbol = keyword[idx:idx + 1]
            if symbol not in self._symbols:
                self._symbols[symbol] = len(self._symbols)
                self._symbol_list.append(symbol)
            symbol_id = self._symbols[symbol]
            while symbol_id >= len(current_state['transitions']):
                current_state['transitions'].fromlist([-1] * 5)
            current_state['transitions'][symbol_id] = len(self._states)
            self._states.append(new_state)
            current_state = new_state
            idx += 1
        current_state['success'] = True
        current_state['matched_keyword'] = original_keyword

    def search(self, text):
        if not self._finalized:
            raise ValueError('KeywordTree has not been finalized.' +
                             ' No search allowed. Call finalize() first.')
        if self._case_insensitive:
            text = text.lower()
        current_state = self._zero_state
        for idx, symbol in enumerate(text):
            try:
                symbol_id = self._symbols[symbol]
            except KeyError:
                # Not known in keyword alphabet. Go back to zero
                current_state = self._zero_state
                continue
            if len(current_state['transitions']) > symbol_id and\
                    current_state['transitions'][symbol_id] >= 0:
                current_state = self._states[
                    current_state['transitions'][symbol_id]]
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
        return "ahocorapy KeywordTree with %i states." % len(self._states)

    def __repr__(self):
        return self.dump()

    def dump(self):
        tree = {}
        tree['states'] = []
        for state in self._states:
            serializable_state = state.copy()
            if 'transitions' in state:
                serializable_state['transitions'] = state[
                    'transitions'].tolist()
            tree['states'].append(serializable_state)
        tree['finalized'] = self._finalized
        tree['symbols'] = self._symbols
        tree['symbol_list'] = self._symbol_list
        tree['case_insensitive'] = self._case_insensitive
        return tree

    def load(self, tree):
        self._states = []
        for serializable_state in tree['states']:
            state = serializable_state.copy()
            if 'transitions' in serializable_state:
                arr = array('i')
                arr.fromlist(serializable_state['transitions'])
                state['transitions'] = arr
            self._states.append(state)
        self._zero_state = self._states[0]
        self._finalized = tree['finalized']
        self._symbol_list = tree['symbol_list']
        self._symbols = tree['symbols']
        self._case_insensitive = tree['case_insensitive']


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
            for symbol_id, state_id in enumerate(traversing['transitions']):
                if state_id is not None:
                    if len(state['transitions']) <= symbol_id or\
                            state['transitions'][symbol_id] < 0:
                        while symbol_id >= len(state['transitions']):
                            state['transitions'].fromlist([-1] * 5)
                        state['transitions'][symbol_id] = state_id
            traversing = self._states[traversing['longest_strict_suffix']]

    def search_longest_strict_suffixes_for_children(self, state):
        for symbol_id, childid in enumerate(state['transitions']):
            if childid >= 0:
                child = self._states[childid]
                self.search_longest_strict_suffix(child, symbol_id)
                self.search_longest_strict_suffixes_for_children(child)

    def search_longest_strict_suffix(self, state, symbol_id):
        if 'longest_strict_suffix' not in state:
            parent = self._states[state['parent']]
            if parent['id'] == 0:
                state['longest_strict_suffix'] = 0
            else:
                found_suffix = False
                if 'longest_strict_suffix' not in parent:
                    # Has not been done yet. Do early
                    self.search_longest_strict_suffix(parent, symbol_id)
                traversed = self._states[parent['longest_strict_suffix']]
                while not found_suffix:
                    if len(traversed['transitions']) > symbol_id\
                            and traversed['transitions'][symbol_id] >= 0:
                        state['longest_strict_suffix'] = traversed[
                            'transitions'][symbol_id]
                        found_suffix = True
                    elif traversed['id'] == 0:
                        state['longest_strict_suffix'] = 0
                        found_suffix = True
                    else:
                        if 'longest_strict_suffix' not in traversed:
                            # Has not been done yet. Do early
                            self.search_longest_strict_suffix(
                                traversed, symbol_id)
                        traversed = self._states[
                            traversed['longest_strict_suffix']]
