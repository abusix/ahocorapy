from __future__ import print_function

import time

from pickle import loads, dumps

from ahocorapy.keywordtree import KeywordTree


with open('tests/data/names.txt') as keyword_file:
    keyword_list = [keyword.strip() for keyword in keyword_file.readlines()]


def init_ahocorapy():
    kwtree = KeywordTree()
    for keyword in keyword_list:
        kwtree.add(keyword)
    kwtree.finalize()
    return kwtree


ahocorapy_tree = init_ahocorapy()

dump_start = time.time()
serialized = dumps(ahocorapy_tree)
dump_end = time.time()

load_start = time.time()
deserialized = loads(serialized)
load_end = time.time()

print('Serialization took: {0:.2f}s\nDeserialization took: {1:.2f}s'.format(
    dump_end-dump_start, load_end-load_start))
