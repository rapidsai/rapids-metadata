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

import urllib.request

import pydantic

from .metadata import RAPIDSMetadata


__all__ = ["fetch_latest"]

_GITHUB_METADATA_URL = "https://raw.githubusercontent.com/rapidsai/rapids-metadata/main/rapids-metadata.json"


def _fetch_from_url(url: str) -> RAPIDSMetadata:
    with urllib.request.urlopen(url) as f:
        return pydantic.TypeAdapter(RAPIDSMetadata).validate_json(f.read())


def fetch_latest() -> RAPIDSMetadata:
    return _fetch_from_url(_GITHUB_METADATA_URL)
