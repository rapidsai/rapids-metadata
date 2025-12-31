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

from unittest.mock import patch

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


def test_fetch_latest():
    with patch("rapids_metadata.remote._fetch_from_url") as patch_fetch_from_url:
        return_value = rapids_remote.fetch_latest()
    patch_fetch_from_url.assert_called_once_with(rapids_remote._GITHUB_METADATA_URL)
    assert return_value == patch_fetch_from_url()
