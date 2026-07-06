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

import math
import os
import time
import urllib.error
import urllib.request
from collections.abc import Mapping
from typing import Optional

import pydantic

from .metadata import RAPIDSMetadata

__all__ = ["fetch_latest"]

_GITHUB_METADATA_URL = "https://raw.githubusercontent.com/rapidsai/rapids-metadata/main/rapids-metadata.json"
_GITHUB_API_METADATA_URL = "https://api.github.com/repos/rapidsai/rapids-metadata/contents/rapids-metadata.json"
_GITHUB_API_VERSION = "2026-03-10"
_MAX_ATTEMPTS = 3
_RETRYABLE_HTTP_STATUS_CODES = {408, 429, 500, 502, 503, 504}
_RATE_LIMIT_RETRY_SECONDS = 60.0


def _header_as_float(error: urllib.error.HTTPError, name: str) -> Optional[float]:
    try:
        value = float(error.headers[name])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def _retry_delay(error: urllib.error.HTTPError, attempt: int) -> float:
    if (retry_after := _header_as_float(error, "Retry-After")) is not None:
        return max(0.0, retry_after)

    if (
        error.headers.get("X-RateLimit-Remaining") == "0"
        and (reset_at := _header_as_float(error, "X-RateLimit-Reset")) is not None
    ):
        return max(0.0, reset_at - time.time()) + 1.0

    if error.code in {403, 429}:
        return _RATE_LIMIT_RETRY_SECONDS * 2**attempt
    return float(2**attempt)


def _is_retryable(error: urllib.error.HTTPError) -> bool:
    return error.code in _RETRYABLE_HTTP_STATUS_CODES or (
        error.code == 403
        and (
            "Retry-After" in error.headers
            or error.headers.get("X-RateLimit-Remaining") == "0"
        )
    )


def _fetch_from_url(
    url: str, *, headers: Optional[Mapping[str, str]] = None
) -> RAPIDSMetadata:
    request = urllib.request.Request(url, headers=dict(headers or {}))
    for attempt in range(_MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(request) as f:
                return pydantic.TypeAdapter(RAPIDSMetadata).validate_json(f.read())
        except urllib.error.HTTPError as error:
            if attempt == _MAX_ATTEMPTS - 1 or not _is_retryable(error):
                raise
            time.sleep(_retry_delay(error, attempt))
        except urllib.error.URLError:
            if attempt == _MAX_ATTEMPTS - 1:
                raise
            time.sleep(2**attempt)

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
