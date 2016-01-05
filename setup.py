#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open('%s/VERSION' % here) as f:
    __version__ = f.readline().strip()

setup(
    author='abusix',
    author_email='info@abusix.com',
    description='ahocorapy - Simple ahocorasick implementation',
    long_description='ahocorapy- A simple ahocorasick library, implemented entirely' +
    ' in python. No regexes etc supported. With unicode support',
    name='ahocorapy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    url='http://www.abusix.com/',
    version=__version__
)
