#!/bin/bash

set -exuo pipefail

# Commands from README.md
rm -rf .test_venv
python3 -m venv .test_venv
.test_venv/bin/python3 -m pip install --upgrade pip
.test_venv/bin/pip install -e .
.test_venv/bin/ruff check .
.test_venv/bin/py.test
