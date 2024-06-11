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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-versions", action="store_true")

    parsed = parser.parse_args()
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
    json.dump(metadata, sys.stdout, cls=_RAPIDSMetadataEncoder)


if __name__ == "__main__":
    main()
