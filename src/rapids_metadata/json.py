# Copyright (c) 2024-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os
import re
import sys
from typing import Any, TextIO

from pydantic import TypeAdapter

from . import all_metadata
from .metadata import RAPIDSMetadata
from .rapids_version import get_rapids_version

__all__ = [
    "main",
]


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.description = "Output RAPIDS metadata as a JSON document."
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help="Output all versions, ignoring local VERSION file",
    )
    parser.add_argument(
        "--version",
        help="Output metadata for this RAPIDS YY.MM version, ignoring local VERSION file",
    )
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Output a JSON schema for the data instead of the data itself",
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="<output file>",
        help="Write to a file instead of stdout",
    )

    parsed = parser.parse_args(argv)
    if parsed.all_versions and parsed.version is not None:
        parser.error("--all-versions and --version cannot be used together")
    if (
        parsed.version is not None
        and re.fullmatch(r"[0-9]{2}\.[0-9]{2}", parsed.version) is None
    ):
        parser.error("--version must use YY.MM format")

    def write_file(data: dict[str, Any], f: TextIO):
        json.dump(
            data,
            f,
            sort_keys=True,
            separators=(",", ": ") if parsed.pretty else (",", ":"),
            indent="  " if parsed.pretty else None,
        )
        if parsed.pretty:
            f.write("\n")

    type_adapter = TypeAdapter(RAPIDSMetadata)
    if parsed.schema:
        data = type_adapter.json_schema()
    else:
        if parsed.all_versions:
            metadata = all_metadata
        else:
            version = parsed.version or get_rapids_version(os.getcwd())
            try:
                version_data = all_metadata.get_version(version)
            except KeyError:
                parser.error(f"no metadata compatible with RAPIDS {version}")
            metadata = RAPIDSMetadata(versions={version: version_data})
        data = type_adapter.dump_python(metadata)

    if parsed.output:
        with open(parsed.output, "w") as f:
            write_file(data, f)
    else:
        write_file(data, sys.stdout)


if __name__ == "__main__":
    main()
