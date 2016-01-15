import re

from ahocorapy.keywordtree import KeywordTree

# from guppy import hpy
# h = hpy()

kwtree = KeywordTree()
with open('tests/data/domains.txt') as keyword_file:
    keyword_list = map(re.escape, map(str.strip, keyword_file.readlines()))
    for keyword in keyword_list:
        kwtree.add(keyword)
    kwtree.finalize()
    # print h.heap()
    for _ in range(0, 1000):
        kwtree.search(re.escape('peterchen@linkpt.com'))
