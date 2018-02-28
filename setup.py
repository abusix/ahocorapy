#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open('%s/VERSION' % here) as f:
    __version__ = f.readline().strip()

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='abusix',
    author_email='fp@abusix.com',
    description='ahocorapy - Pure python ahocorasick implementation',
    long_description=long_description,
    name='ahocorapy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['future'],
    url='https://github.com/abusix/ahocorapy',
    project_urls={
        'Source': 'https://github.com/abusix/ahocorapy',
        'Company': 'https://www.abusix.com/'
    },
    keywords = ['keyword', 'search', 'purepython', 'aho-corasick', 'ahocorasick', 'abusix'],
    license='MIT',
    version=__version__
)
