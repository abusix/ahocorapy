#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ahocorapy.keywordtree import KeywordTree
from ahocorapy_visualizer.visualizer import Visualizer


class TestAhocorapyVisualizer(unittest.TestCase):

    def test_visualizer(self):
        # Needs working pygraphviz on system
        kwtree = KeywordTree(case_insensitive=True)
        kwtree.add('malaga')
        kwtree.add('lacrosse')
        kwtree.add('mallorca')
        kwtree.add('mallorca bella')
        kwtree.add('orca')
        kwtree.finalize()

        visualizer = Visualizer()
        visualizer.draw('readme_example.png', kwtree)


if __name__ == '__main__':
    unittest.main()
