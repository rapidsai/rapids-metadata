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
import dataclasses
import json
import os
import sys
from typing import Any, Union

from . import all_metadata
from .metadata import (
    RAPIDSMetadata,
    RAPIDSPackage,
    RAPIDSRepository,
    RAPIDSVersion,
)
from .rapids_version import get_rapids_version


__all__ = [
    "main",
]


class _RAPIDSMetadataEncoder(json.JSONEncoder):
    def default(
        self, o: Union[RAPIDSMetadata, RAPIDSPackage, RAPIDSRepository, RAPIDSVersion]
    ) -> dict[str, Any]:
        return dataclasses.asdict(o)


def main(argv: Union[list[str], None] = None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--all-versions", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("-o", "--output")

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
            metadata,
            f,
            cls=_RAPIDSMetadataEncoder,
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
