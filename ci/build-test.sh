#!/bin/bash
# Copyright (c) 2024, NVIDIA CORPORATION.
# Builds and tests Python package

set -ue

pip install build

python -m build .

for PKG in dist/*; do
  echo "$PKG"
  pip install --force-reinstall "$PKG[test]"
  pytest
done
