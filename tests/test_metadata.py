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

from unittest.mock import Mock, patch

import pytest
from packaging.version import InvalidVersion
from rapids_metadata import metadata as md


class TestRAPIDSVersion:
    @pytest.fixture
    def metadata(self):
        return md.RAPIDSVersion(repositories={
            "repo1": md.RAPIDSRepository(packages={
                "package1": md.RAPIDSPackage(has_alpha_spec=True, has_cuda_suffix=True),
                "package2": md.RAPIDSPackage(has_alpha_spec=True, has_cuda_suffix=False),
            }),
            "repo2": md.RAPIDSRepository(packages={
                "package3": md.RAPIDSPackage(has_alpha_spec=False, has_cuda_suffix=True),
                "package4": md.RAPIDSPackage(has_alpha_spec=False, has_cuda_suffix=False),
            }),
        })

    def test_all_packages(self, metadata):
        assert metadata.all_packages == {"package1", "package2", "package3", "package4"}

    def test_alpha_spec_packages(self, metadata):
        assert metadata.alpha_spec_packages == {"package1", "package2"}

    def test_cuda_suffixed_packages(self, metadata):
        assert metadata.cuda_suffixed_packages == {"package1", "package3"}


class TestRAPIDSMetadata:
    @pytest.fixture
    def metadata(self):
        return md.RAPIDSMetadata(versions={
            "24.06": md.RAPIDSVersion(repositories={
                "repo1": md.RAPIDSRepository(),
            }),
            "24.08": md.RAPIDSVersion(repositories={
                "repo2": md.RAPIDSRepository(),
            }),
        })

    @pytest.mark.parametrize(
        ["current_version", "expected_version"],
        [
            ("24.05", KeyError),
            ("24.06", "24.06"),
            ("24.07", KeyError),
            ("24.08", "24.08"),
            ("24.09", "24.08"),
            ("aaa", InvalidVersion),
        ],
    )
    def test_get_current_version(self, current_version, expected_version, metadata):
        if isinstance(expected_version, type) and issubclass(expected_version, BaseException):
            with patch("rapids_metadata.metadata.get_rapids_version", Mock(return_value=current_version)):
                with pytest.raises(expected_version):
                    metadata.get_current_version(".")
        else:
            with patch("rapids_metadata.metadata.get_rapids_version", Mock(return_value=current_version)):
                current_version = metadata.get_current_version(".")
            assert current_version == metadata.versions[expected_version]
            for v, m in metadata.versions.items():
                if v != expected_version:
                    assert m != current_version
