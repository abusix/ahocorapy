#!/bin/bash

set -e

python setup.py sdist
twine upload dist/*
rm -r dist/
