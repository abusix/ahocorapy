from builtins import map
from io import open
from timeit import timeit

import ahocorasick
from py_aho_corasick import py_aho_corasick

from ahocorapy.keywordtree import KeywordTree



SEARCH_ITERATIONS = 100


with open('tests/data/names.txt') as keyword_file:
    keyword_list = list(map(str.strip, keyword_file.readlines()))

with open('tests/data/textblob.txt') as keyword_file:
    textblob = keyword_file.read()

print('-' * 10 + 'ahocorapy' + '-' * 10)


def init_ahocorapy():
    kwtree = KeywordTree()
    for keyword in keyword_list:
        kwtree.add(keyword)
    kwtree.finalize()
    return kwtree


def search_ahocorapy(ahocorapy_tree, textblob):
    keyword, _ = ahocorapy_tree.search(textblob)
    return keyword


ahocorapy_tree = init_ahocorapy()
result = search_ahocorapy(ahocorapy_tree, textblob)
assert result == 'Dawn Higgins'

print('setup_ahocorapy: ' +
      str(timeit(stmt='init_ahocorapy()', number=1, globals=globals())))
print('search_ahocorapy: ' + str(timeit(stmt='search_ahocorapy(ahocorapy_tree, textblob)',
                                        number=SEARCH_ITERATIONS, globals=globals())))

print('-' * 10 + 'pyahocorasick' + '-' * 10)


def init_ahocorasick():
    A = ahocorasick.Automaton()
    for keyword in keyword_list:
        A.add_word(keyword, keyword)
    A.make_automaton()
    return A


def search_ahocorasick(ahocorasick_tree, textblob):
    result = ''
    for _, keyword in ahocorasick_tree.iter(textblob):
        result += keyword
    return keyword


ahocorasick_tree = init_ahocorasick()
result = search_ahocorasick(ahocorasick_tree, textblob)
assert result == 'Dawn Higgins'

print('setup_pyahocorasick: ' +
      str(timeit(stmt='init_ahocorasick()', number=1, globals=globals())))
print('search_pyahocorasick: ' + str(timeit(stmt='search_ahocorasick(ahocorasick_tree, textblob)',
                                            number=SEARCH_ITERATIONS, globals=globals())))


print('-' * 10 + 'py_aho_corasick' + '-' * 10)


def init_py_aho_corasick():
    return py_aho_corasick.Automaton(keyword_list)


def search_py_aho_corasick(py_aho_corasick_tree, textblob):
    result = ''
    for match in py_aho_corasick_tree.get_keywords_found(textblob):
        result += match[1]
    return result


py_aho_corasick_tree = init_py_aho_corasick()
result = search_py_aho_corasick(py_aho_corasick_tree, textblob)
assert result == 'dawn higgins'

print('setup_py_aho_corasick: ' +
      str(timeit(stmt='init_py_aho_corasick()', number=1, globals=globals())))

print('search_py_aho_corasick: ' + str(timeit(stmt='search_py_aho_corasick(py_aho_corasick_tree, textblob)',
                                              number=SEARCH_ITERATIONS, globals=globals())))
