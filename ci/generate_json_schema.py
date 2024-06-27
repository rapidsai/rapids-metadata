#!/usr/bin/env python3
# Copyright (c) 2024, NVIDIA CORPORATION.

import os.path
import sys

repo_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(os.path.join(repo_root, "src"))

import rapids_metadata.json as rapids_json  # noqa: E402

if __name__ == "__main__":
    rapids_json.main(
        [
            "--output",
            os.path.join(repo_root, "schemas/rapids-metadata-v1.json"),
            "--pretty",
            "--schema",
        ]
    )
