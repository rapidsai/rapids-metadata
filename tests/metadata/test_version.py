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

import pytest
from rapids_metadata import metadata as md


@pytest.fixture
def metadata():
    return md.RAPIDSVersion(
        repositories={
            "repo1": md.RAPIDSRepository(
                packages={
                    "package1": md.RAPIDSPackage(
                        has_alpha_spec=True, has_cuda_suffix=True
                    ),
                    "package2": md.RAPIDSPackage(
                        has_alpha_spec=True, has_cuda_suffix=False
                    ),
                }
            ),
            "repo2": md.RAPIDSRepository(
                packages={
                    "package3": md.RAPIDSPackage(
                        has_alpha_spec=False, has_cuda_suffix=True
                    ),
                    "package4": md.RAPIDSPackage(
                        has_alpha_spec=False, has_cuda_suffix=False
                    ),
                }
            ),
        }
    )


def test_all_packages(metadata):
    assert metadata.all_packages == {"package1", "package2", "package3", "package4"}


def test_alpha_spec_packages(metadata):
    assert metadata.alpha_spec_packages == {"package1", "package2"}


def test_cuda_suffixed_packages(metadata):
    assert metadata.cuda_suffixed_packages == {"package1", "package3"}
