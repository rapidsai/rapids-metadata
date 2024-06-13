#!/bin/bash
# Copyright (c) 2024, NVIDIA CORPORATION.

set -euo pipefail

readonly repo_root=$(dirname "$0")/..
cd "$repo_root"

PYTHONPATH="$repo_root/src" python3 -m rapids_metadata.json --all-versions > rapids-metadata.json
