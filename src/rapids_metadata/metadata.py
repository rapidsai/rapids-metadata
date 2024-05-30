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

from typing import Union


class Metadata:
    def __init__(self, inherit: Union["Metadata", None]=None):
        self._packages: set[str] = set()
        self._non_alpha_spec_packages: set[str] = set()
        self._non_cuda_suffixed_packages: set[str] = set()

        if inherit:
            self._packages.update(inherit.packages)
            self._non_alpha_spec_packages.update(inherit.non_alpha_spec_packages)
            self._non_cuda_suffixed_packages.update(inherit.non_cuda_suffixed_packages)

    @property
    def packages(self) -> set[str]:
        return self._packages

    @property
    def non_alpha_spec_packages(self) -> set[str]:
        return self._non_alpha_spec_packages

    @property
    def non_cuda_suffixed_packages(self) -> set[str]:
        return self._non_cuda_suffixed_packages

    @property
    def alpha_spec_packages(self) -> frozenset[str]:
        return frozenset(self.packages - self.non_alpha_spec_packages)

    @property
    def cuda_suffixed_packages(self) -> frozenset[str]:
        return frozenset(self.packages - self.non_cuda_suffixed_packages)
