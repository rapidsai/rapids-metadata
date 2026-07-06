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

import io
import urllib.error
from unittest.mock import call, patch

import pytest
import rapids_metadata.remote as rapids_remote
from pydantic import TypeAdapter
from pytest_httpserver import HTTPServer
from rapids_metadata import all_metadata
from rapids_metadata.metadata import RAPIDSMetadata


def test_fetch_from_url(httpserver: HTTPServer):
    httpserver.expect_request("/rapids-metadata.json").respond_with_json(
        TypeAdapter(RAPIDSMetadata).dump_python(all_metadata)
    )
    assert (
        rapids_remote._fetch_from_url(httpserver.url_for("/rapids-metadata.json"))
        == all_metadata
    )


def test_fetch_latest_without_token(monkeypatch):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with patch("rapids_metadata.remote._fetch_from_url") as patch_fetch_from_url:
        rapids_remote.fetch_latest()
    patch_fetch_from_url.assert_called_once_with(rapids_remote._GITHUB_METADATA_URL)


@pytest.mark.parametrize(
    ("environment", "expected_token"),
    [
        ({"GITHUB_TOKEN": "github-token"}, "github-token"),
        (
            {"GH_TOKEN": "gh-token", "GITHUB_TOKEN": "github-token"},
            "gh-token",
        ),
    ],
)
def test_fetch_latest_with_token(monkeypatch, environment, expected_token):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    with patch("rapids_metadata.remote._fetch_from_url") as patch_fetch_from_url:
        rapids_remote.fetch_latest()

    patch_fetch_from_url.assert_called_once_with(
        rapids_remote._GITHUB_API_METADATA_URL,
        headers={
            "Accept": "application/vnd.github.raw+json",
            "Authorization": f"Bearer {expected_token}",
            "X-GitHub-Api-Version": rapids_remote._GITHUB_API_VERSION,
        },
    )


def _metadata_response():
    return io.BytesIO(TypeAdapter(RAPIDSMetadata).dump_json(all_metadata))


def _http_error(status, headers=None):
    return urllib.error.HTTPError(
        rapids_remote._GITHUB_METADATA_URL,
        status,
        "request failed",
        headers or {},
        None,
    )


@patch("rapids_metadata.remote.time.sleep")
@patch("rapids_metadata.remote.urllib.request.urlopen")
def test_fetch_retries_429(patch_urlopen, patch_sleep):
    patch_urlopen.side_effect = [
        _http_error(429, {"Retry-After": "7"}),
        _metadata_response(),
    ]

    assert rapids_remote._fetch_from_url("https://example.com") == all_metadata
    assert patch_urlopen.call_count == 2
    patch_sleep.assert_called_once_with(7)


@pytest.mark.parametrize(
    "error",
    [_http_error(503), urllib.error.URLError("connection reset")],
)
@patch("rapids_metadata.remote.time.sleep")
@patch("rapids_metadata.remote.urllib.request.urlopen")
def test_fetch_retries_transient_error(patch_urlopen, patch_sleep, error):
    patch_urlopen.side_effect = [error, _metadata_response()]

    assert rapids_remote._fetch_from_url("https://example.com") == all_metadata
    patch_sleep.assert_called_once_with(1)


@patch("rapids_metadata.remote.time.sleep")
@patch("rapids_metadata.remote.urllib.request.urlopen")
def test_fetch_stops_after_max_attempts(patch_urlopen, patch_sleep):
    errors = [
        _http_error(429, {"Retry-After": "0"})
        for _ in range(rapids_remote._MAX_ATTEMPTS)
    ]
    patch_urlopen.side_effect = errors

    with pytest.raises(urllib.error.HTTPError) as raised:
        rapids_remote._fetch_from_url("https://example.com")

    assert raised.value is errors[-1]
    assert patch_urlopen.call_count == rapids_remote._MAX_ATTEMPTS
    assert patch_sleep.call_args_list == [call(0), call(0)]


@patch("rapids_metadata.remote.time.sleep")
@patch("rapids_metadata.remote.urllib.request.urlopen")
def test_fetch_does_not_retry_nonretryable_error(patch_urlopen, patch_sleep):
    error = _http_error(404)
    patch_urlopen.side_effect = error

    with pytest.raises(urllib.error.HTTPError) as raised:
        rapids_remote._fetch_from_url("https://example.com")

    assert raised.value is error
    patch_urlopen.assert_called_once()
    patch_sleep.assert_not_called()
