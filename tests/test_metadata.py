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

from rapids_metadata.metadata import Metadata


def test_inherit():
    parent = Metadata()
    parent.packages.update({"package-1", "package-2"})
    parent.non_alpha_spec_packages.update({"package-1"})
    parent.non_cuda_suffixed_packages.update({"package-2"})

    metadata = Metadata(parent)
    assert metadata.packages == {"package-1", "package-2"}
    assert metadata.non_alpha_spec_packages == {"package-1"}
    assert metadata.non_cuda_suffixed_packages == {"package-2"}
    assert parent.packages == {"package-1", "package-2"}
    assert parent.non_alpha_spec_packages == {"package-1"}
    assert parent.non_cuda_suffixed_packages == {"package-2"}

    metadata.packages.update({"package-3"})
    metadata.non_alpha_spec_packages.update({"package-3"})
    metadata.non_cuda_suffixed_packages.update({"package-3"})
    assert metadata.packages == {"package-1", "package-2", "package-3"}
    assert metadata.non_alpha_spec_packages == {"package-1", "package-3"}
    assert metadata.non_cuda_suffixed_packages == {"package-2", "package-3"}
    assert parent.packages == {"package-1", "package-2"}
    assert parent.non_alpha_spec_packages == {"package-1"}
    assert parent.non_cuda_suffixed_packages == {"package-2"}


def test_alpha_spec_packages():
    metadata = Metadata()
    metadata.packages.update({"package-1", "package-2"})
    metadata.non_alpha_spec_packages.update({"package-1"})
    assert metadata.alpha_spec_packages == {"package-2"}


def test_cuda_suffixed_packages():
    metadata = Metadata()
    metadata.packages.update({"package-1", "package-2"})
    metadata.non_cuda_suffixed_packages.update({"package-1"})
    assert metadata.cuda_suffixed_packages == {"package-2"}
