#!/bin/bash

rm -r build/ dist/ 2>/dev/null
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
