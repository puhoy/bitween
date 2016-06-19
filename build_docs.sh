#!/bin/bash

cd docs
sphinx-apidoc -f -o . ../bitween
make html
