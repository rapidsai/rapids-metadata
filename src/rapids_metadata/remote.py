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

import os
import time
import urllib.error
import urllib.request
from typing import Optional

import pydantic

from .metadata import RAPIDSMetadata

__all__ = ["fetch_latest"]

_GITHUB_METADATA_URL = "https://raw.githubusercontent.com/rapidsai/rapids-metadata/main/rapids-metadata.json"
_GITHUB_API_METADATA_URL = "https://api.github.com/repos/rapidsai/rapids-metadata/contents/rapids-metadata.json"
_GITHUB_API_VERSION = "2026-03-10"
_MAX_ATTEMPTS = 3
_RETRYABLE_HTTP_STATUS_CODES = {408, 429, 500, 502, 503, 504}


def _fetch_from_url(
    url: str, *, headers: Optional[dict[str, str]] = None
) -> RAPIDSMetadata:
    request = urllib.request.Request(url, headers=headers or {})
    for attempt in range(_MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(request) as f:
                return pydantic.TypeAdapter(RAPIDSMetadata).validate_json(f.read())
        except urllib.error.HTTPError as error:
            if (
                attempt == _MAX_ATTEMPTS - 1
                or error.code not in _RETRYABLE_HTTP_STATUS_CODES
            ):
                raise
            default_delay = (60 if error.code == 429 else 1) * 2**attempt
            delay = max(0, int(error.headers.get("Retry-After", default_delay)))
        except urllib.error.URLError:
            if attempt == _MAX_ATTEMPTS - 1:
                raise
            delay = 2**attempt
        time.sleep(delay)

    raise AssertionError("unreachable")


def fetch_latest() -> RAPIDSMetadata:
    if token := os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"):
        return _fetch_from_url(
            _GITHUB_API_METADATA_URL,
            headers={
                "Accept": "application/vnd.github.raw+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": _GITHUB_API_VERSION,
            },
        )
    return _fetch_from_url(_GITHUB_METADATA_URL)
