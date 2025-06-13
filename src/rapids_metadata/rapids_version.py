# Copyright (c) 2024-2025, NVIDIA CORPORATION.
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

import os.path
from os import PathLike
from typing import Union


__all__ = ["get_rapids_version"]


def get_rapids_version(
    directory: Union[str, PathLike[str]],
    version_file: Union[str, PathLike[str]] = "VERSION",
) -> str:
    from packaging.version import InvalidVersion, Version

    while not os.path.samefile(directory, os.path.dirname(directory)):
        try:
            with open(os.path.join(directory, version_file)) as f:
                version = Version(f.read())
        except (FileNotFoundError, InvalidVersion):
            directory = os.path.dirname(directory)
        else:
            return f"{version.major:02}.{version.minor:02}"

    raise FileNotFoundError
