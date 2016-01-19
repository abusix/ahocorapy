#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ahocorapy.keywordtree import KeywordTree
from ahocorapy.visualizer import Visualizer


class TestAhocorapyVisualizer(unittest.TestCase):

    def test_visualizer(self):
        # Needs working pygraphviz on system
        kwtree = KeywordTree(case_insensitive=True)
        kwtree.add('malaga')
        kwtree.add('lacrosse')
        kwtree.add('mallorca')
        kwtree.add('mallorca bella')
        kwtree.finalize()

        result = kwtree.search('My favorite islands are malaga and sylt.')
        self.assertEqual(('malaga', 24), result)

        result = kwtree.search(
            'idontlikewhitespaceswhereismalacrossequestionmark')
        self.assertEqual(('lacrosse', 29), result)

        result = kwtree.search('crossing on mallorca bella')
        self.assertEqual(('mallorca', 12), result)

        visualizer = Visualizer()
        visualizer.draw('readme_example.png', kwtree)


if __name__ == '__main__':
    unittest.main()
