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

from . import rapids_metadata
from .metadata import (
    RAPIDSMetadata,
    RAPIDSPackage,
    RAPIDSRepository,
    RAPIDSVersion,
)
from .rapids_version import get_rapids_version


__all__ = [
    "RAPIDSMetadataEncoder",
    "main",
]


class RAPIDSMetadataEncoder(json.JSONEncoder):
    def default(self, o):
        def recurse(o):
            if o is None:
                return None
            for t in [bool, int, float, str]:
                if isinstance(o, t):
                    return o
            if isinstance(o, dict):
                return {key: recurse(value) for key, value in o.items()}
            return self.default(o)

        for c in [RAPIDSMetadata, RAPIDSPackage, RAPIDSRepository]:
            if isinstance(o, c):
                return {
                    field.name: recurse(getattr(o, field.name))
                    for field in dataclasses.fields(o)
                }
        if isinstance(o, RAPIDSVersion):
            return {
                "repositories": {
                    str(repository): recurse(repository_data)
                    for repository, repository_data in o.repositories.items()
                },
                **{
                    field.name: recurse(getattr(o, field.name))
                    for field in dataclasses.fields(o)
                    if field.name != "repositories"
                },
            }
        return super().default(o)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-versions", action="store_true")

    parsed = parser.parse_args()
    metadata = (
        rapids_metadata
        if parsed.all_versions
        else RAPIDSMetadata(
            versions={
                get_rapids_version(os.getcwd()): rapids_metadata.get_current_version(
                    os.getcwd()
                )
            }
        )
    )
    json.dump(metadata, sys.stdout, cls=RAPIDSMetadataEncoder)


if __name__ == "__main__":
    main()