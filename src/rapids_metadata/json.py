# Copyright (c) 2024, NVIDIA CORPORATION.
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
import sys
from typing import Union

from pydantic import TypeAdapter

from . import all_metadata
from .metadata import RAPIDSMetadata
from .rapids_version import get_rapids_version


__all__ = [
    "main",
]


def main(argv: Union[list[str], None] = None):
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
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="<output file>",
        help="Write to a file instead of stdout",
    )

    parsed = parser.parse_args(argv)
    metadata = (
        all_metadata
        if parsed.all_versions
        else RAPIDSMetadata(
            versions={
                get_rapids_version(os.getcwd()): all_metadata.get_current_version(
                    os.getcwd()
                )
            }
        )
    )

    def write_file(f):
        json.dump(
            TypeAdapter(RAPIDSMetadata).dump_python(metadata),
            f,
            sort_keys=True,
            separators=(",", ": ") if parsed.pretty else (",", ":"),
            indent="  " if parsed.pretty else None,
        )
        if parsed.pretty:
            f.write("\n")

    if parsed.output:
        with open(parsed.output, "w") as f:
            write_file(f)
    else:
        write_file(sys.stdout)


if __name__ == "__main__":
    main()
