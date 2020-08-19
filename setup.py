#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

from setuptools import setup, find_packages


with open('%s/VERSION' % here) as f:
    __version__ = f.readline().strip()

setup(
    author='abusix',
    author_email='fp@abusix.com',
    description='ahocorapy - Pure python ahocorasick implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='ahocorapy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['future'],
    python_requires='>=2.7',
    url='https://github.com/abusix/ahocorapy',
    project_urls={
        'Source': 'https://github.com/abusix/ahocorapy',
        'Company': 'https://www.abusix.com/'
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords = ['keyword', 'search', 'purepython', 'aho-corasick', 'ahocorasick', 'abusix'],
    license='MIT',
    version=__version__
)
