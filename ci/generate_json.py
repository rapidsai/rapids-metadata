#!/usr/bin/env python3
# Copyright (c) 2024, NVIDIA CORPORATION.

import os.path
import sys

repo_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(os.path.join(repo_root, "src"))

from rapids_metadata import json as rapids_json  # noqa: E402

if __name__ == "__main__":
    rapids_json.main(
        [
            "--output",
            os.path.join(repo_root, "rapids-metadata.json"),
            "--pretty",
            "--all-versions",
        ]
    )
