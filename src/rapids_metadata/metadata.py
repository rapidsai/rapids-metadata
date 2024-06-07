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

from dataclasses import dataclass, field
from enum import Enum
from os import PathLike
from typing import Union

from .rapids_version import get_rapids_version

__all__ = ["PseudoRepository", "RAPIDSMetadata", "RAPIDSPackage", "RAPIDSRepository", "RAPIDSVersion"]


class PseudoRepository(Enum):
    NVIDIA = "nvidia"

    def __str__(self):
        return f"_{self.value}"


@dataclass
class RAPIDSPackage:
    has_alpha_spec: bool = field(default=True)
    has_cuda_suffix: bool = field(default=True)


@dataclass
class RAPIDSRepository:
    packages: dict[str, RAPIDSPackage] = field(default_factory=dict)


@dataclass
class RAPIDSVersion:
    repositories: dict[Union[str, PseudoRepository], RAPIDSRepository] = field(default_factory=dict)

    @property
    def all_packages(self) -> set[str]:
        return {package for repository_data in self.repositories.values() for package in repository_data.packages}

    @property
    def alpha_spec_packages(self) -> set[str]:
        return {package for repository_data in self.repositories.values() for package, package_data in repository_data.packages.items() if package_data.has_alpha_spec}

    @property
    def cuda_suffixed_packages(self) -> set[str]:
        return {package for repository_data in self.repositories.values() for package, package_data in repository_data.packages.items() if package_data.has_cuda_suffix}


@dataclass
class RAPIDSMetadata:
    versions: dict[str, RAPIDSVersion] = field(default_factory=dict)

    def get_current_version(self, directory: PathLike=None) -> RAPIDSVersion:
        return self.versions[get_rapids_version(directory)]
