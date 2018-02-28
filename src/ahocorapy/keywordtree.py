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

from builtins import object
from array import array
import json


class KeywordTree(object):

    def __init__(self, case_insensitive=False,
                 over_allocation=2):
        '''
        @param case_insensitive: If true, case will be ignored when searching.
                                 Setting this to true will have a positive
                                 impact on performance.
                                 Defaults to false.
        @param over_allocation: Determines how big initial transition arrays
                                are and how much space is allocated in addition
                                to what is essential when array needs to be
                                resized. Default value 2 seemed to be sweet
                                spot for memory as well as cpu.
        '''
        self._zero_state = {
            'id': 0, 'success': False,
            'transitions': array('i', [-1] * over_allocation), 'parent': None}
        self._finalized = False
        self._states = [self._zero_state]
        self._symbols = {}
        self._symbol_list = []
        self._case_insensitive = case_insensitive
        self._over_allocation = over_allocation
    
    def add(self, keyword):
        '''
        Add a keyword to the tree.
        Can only be used before finalize() has been called.
        Keyword should be str or unicode.
        '''
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
        symbol = keyword[idx]
        if symbol not in self._symbols:
            self._symbols[symbol] = len(self._symbols)
            self._symbol_list.append(symbol)
        symbol_id = self._symbols[symbol]
        if len(current_state['transitions']) > symbol_id\
                and current_state['transitions'][symbol_id] >= 0:
            next_state = self._states[current_state['transitions'][symbol_id]]
        while next_state is not None:
            idx += 1
            if next_state['success'] or idx>=len(keyword):
                # There is a keyword which is a prefix of the added keyword
                # return here for performance
                return
            current_state = next_state
            next_state = None
            symbol = keyword[idx]
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
                'transitions': array('i', [-1] * self._over_allocation),
                'parent': current_state['id']}
            symbol = keyword[idx]
            if symbol not in self._symbols:
                self._symbols[symbol] = len(self._symbols)
                self._symbol_list.append(symbol)
            symbol_id = self._symbols[symbol]
            trans_len = len(current_state['transitions'])
            if symbol_id >= trans_len:
                current_state['transitions'].fromlist(
                    [-1] * (symbol_id -
                            trans_len + 1 +
                            self._over_allocation))
            current_state['transitions'][symbol_id] = len(self._states)
            self._states.append(new_state)
            current_state = new_state
            idx += 1
        current_state['success'] = True
        current_state['matched_keyword'] = original_keyword

    def search(self, text):
        '''
        Search a text for any occurence of a keyword.
        Returns when one keyword has been found.
        Can only be called after finalized() has been called.
        O(n) with n = len(text)
        @return: 2-Tuple with keyword and startindex in text.
                 Or None if no keyword was found in the text.
        '''
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
                if len(current_state['transitions']) > symbol_id and\
                    current_state['transitions'][symbol_id] >= 0:
                    current_state = self._states[
                        current_state['transitions'][symbol_id]]
                    if current_state['success']:
                        keyword = current_state['matched_keyword']
                        return (keyword, idx + 1 - len(keyword))

    def finalize(self):
        '''
        Needs to be called after all keywords have been added and
        before any searching is performed.
        '''
        if self._finalized:
            raise ValueError('KeywordTree has already been finalized.')   
        finalizer = Finalizer(self)
        finalizer.finalize()
        self._finalized = True

    def __str__(self):
        return "ahocorapy KeywordTree with %i states." % len(self._states)

    def __repr__(self):
        return json.dumps(self.dump())

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
        tree['over_allocation'] = self._over_allocation
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
        self._over_allocation = tree['over_allocation']


class Finalizer(object):

    def __init__(self, keyword_tree):
        self._keyword_tree = keyword_tree
        self._states = keyword_tree._states

    def finalize(self):
        zero_state = self._keyword_tree._zero_state
        zero_state['longest_strict_suffix'] = 0
        self.search_longest_strict_suffixes_for_children(zero_state)
        # Remove to save space
        for state in self._states:
            # Only needed during finalize
            del state['longest_strict_suffix']
            del state['parent']
            # Remove since we only need one result
            if state['success']:
                del state['transitions']

    def search_longest_strict_suffixes_for_children(self, state):
        processed = set()
        to_process = [state]
        while to_process:
            state_to_process = to_process.pop()
            processed.add(state_to_process['id'])
            for symbol_id, childid in enumerate(state_to_process['transitions']):
                if childid >= 0 and childid not in processed:
                    child = self._states[childid]
                    self.search_longest_strict_suffix(child, symbol_id)
                    to_process.append(child)

    def search_longest_strict_suffix(self, state, symbol_id):
        if 'longest_strict_suffix' not in state:
            parent = self._states[state['parent']]
            found_suffix = False
            if 'longest_strict_suffix' not in parent:
                # Has not been done yet. Do early
                self.search_longest_strict_suffix(parent, [ingoing_symbol_id for ingoing_symbol_id, ingoing_state_id in enumerate(parent['transitions']) if ingoing_state_id == state['id']][0])
            traversed = self._states[parent['longest_strict_suffix']]
            while not found_suffix:
                if len(traversed['transitions']) > symbol_id\
                        and traversed['transitions'][symbol_id] >= 0\
                        and traversed['transitions'][symbol_id] != state['id']:
                    state['longest_strict_suffix'] = traversed[
                        'transitions'][symbol_id]
                    found_suffix = True
                elif traversed['id'] == 0:
                    state['longest_strict_suffix'] = 0
                    found_suffix = True
                else:
                    if 'longest_strict_suffix' not in traversed:
                        # Has not been done yet. Do early
                        self.search_longest_strict_suffix(traversed, symbol_id)

                    traversed = self._states[
                        traversed['longest_strict_suffix']]
            if state['longest_strict_suffix'] > 0:
                suffix_trans = self._states[state['longest_strict_suffix']]['transitions']
                suffix_trans_len = len(suffix_trans)
                if suffix_trans_len > len(state['transitions']):
                    state['transitions'].fromlist(
                                    [-1] * (suffix_trans_len +
                                            self._keyword_tree._over_allocation))
                for symbol_id, state_id in enumerate(suffix_trans):
                    if state_id >= 0 and state['transitions'][symbol_id] < 0:
                            state['transitions'][symbol_id] = state_id
