from builtins import map
from builtins import range
from ahocorapy.keywordtree import KeywordTree

kwtree = KeywordTree()
with open('tests/data/domains.txt') as keyword_file:
    keyword_list = list(map(str.strip, keyword_file.readlines()))
    for keyword in keyword_list:
        kwtree.add(keyword)
    kwtree.finalize()
    for _ in range(0, 1000):
        kwtree.search('peterchen@linkpt.com')
