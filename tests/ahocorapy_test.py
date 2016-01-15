#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ahocorapy.keywordtree import KeywordTree

import msgpack
import gzip
import os


class TestAhocorapy(unittest.TestCase):

    def test_empty_tree(self):
        kwtree = KeywordTree()
        kwtree.finalize()

        result = kwtree.search('zef')
        self.assertIsNone(result)

    def test_empty_input(self):
        kwtree = KeywordTree()
        kwtree.add('bla')
        kwtree.finalize()

        result = kwtree.search('')
        self.assertIsNone(result)

    def test_empty_keyword(self):
        kwtree = KeywordTree()
        kwtree.add('')
        kwtree.finalize()

        result = kwtree.search('')
        self.assertIsNone(result)

    def test_suffix_stuff(self):
        kwtree = KeywordTree()
        kwtree.add('blaaaaa')
        kwtree.add('blue')
        kwtree.add('aaaamen')
        kwtree.finalize()

        result = kwtree.search('shfohdfaaaaaamenbla')
        self.assertEqual(('aaaamen', 9), result)

    def test_simple(self):
        kwtree = KeywordTree()
        kwtree.add('bla')
        kwtree.add('blue')
        kwtree.finalize()

        result = kwtree.search('bl')
        self.assertIsNone(result)

        result = kwtree.search('')
        self.assertIsNone(result)

        result = kwtree.search('zef')
        self.assertIsNone(result)

        result = kwtree.search('blaaaa')
        self.assertEqual(('bla', 0), result)

        result = kwtree.search('red green blue grey')
        self.assertEqual(('blue', 10), result)

    def test_domains(self):
        kwtree = KeywordTree()
        kwtree.add('searchenginemarketingfordummies.com')
        kwtree.add('linkpt.com')
        kwtree.add('fnbpeterstown.com')
        kwtree.finalize()

        result = kwtree.search('peterchen@linkpt.com')
        self.assertEqual(('linkpt.com', 10), result)

    def test_unicode(self):
        kwtree = KeywordTree()
        kwtree.add('bla')
        kwtree.add('blue')
        kwtree.add(u'颜到')
        kwtree.finalize()

        result = kwtree.search(u'春华变苍颜到处群魔乱')
        self.assertEqual((u'颜到', 4), result)

        result = kwtree.search(u'三年过')
        self.assertIsNone(result)

    def test_case_sensitivity(self):
        kwtree = KeywordTree()
        kwtree.add('bla')
        kwtree.add('blue')
        kwtree.add('blISs')
        kwtree.finalize()

        result = kwtree.search('bLa')
        self.assertIsNone(result)

        result = kwtree.search('BLISS')
        self.assertIsNone(result)

        result = kwtree.search('bliss')
        self.assertIsNone(result)

        result = kwtree.search('blISs')
        self.assertEqual(('blISs', 0), result)

    def test_case_insensitivity_mode(self):
        kwtree = KeywordTree(case_insensitive=True)
        kwtree.add('bla')
        kwtree.add('blue')
        kwtree.add('blISs')
        kwtree.finalize()

        result = kwtree.search('bLa')
        self.assertEqual(('bla', 0), result)

        result = kwtree.search('BLISS')
        self.assertEqual(('blISs', 0), result)

    def test_dump_and_load(self):
        kwtree = KeywordTree(case_insensitive=True)
        kwtree.add('bla')
        kwtree.add('blue')
        kwtree.add('blISs')
        kwtree.finalize()

        filename = 'kwtree_unittest.msgpack.gz'

        dumped = kwtree.dump()
        with gzip.open(filename, 'wb') as output_file:
            msgpack.dump(dumped, output_file)

        with gzip.open(filename, 'rb') as input_file:
            loadedTree = msgpack.load(input_file)
        kwtree2 = KeywordTree()
        kwtree2.load(loadedTree)

        result = kwtree2.search('bLa')
        self.assertEqual(('bla', 0), result)

        result = kwtree2.search('BLISS')
        self.assertEqual(('blISs', 0), result)

        try:
            os.remove(filename)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
