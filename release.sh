#!/bin/bash

set -e

python setup.py sdist bdist_wheel
twine upload dist/*
rm -r dist/
