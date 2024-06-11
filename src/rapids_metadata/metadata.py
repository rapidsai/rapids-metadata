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
from os import PathLike

from packaging.version import Version
from .rapids_version import get_rapids_version

__all__ = [
    "RAPIDSMetadata",
    "RAPIDSPackage",
    "RAPIDSRepository",
    "RAPIDSVersion",
]


@dataclass
class RAPIDSPackage:
    has_alpha_spec: bool = field(default=True)
    has_cuda_suffix: bool = field(default=True)


@dataclass
class RAPIDSRepository:
    packages: dict[str, RAPIDSPackage] = field(default_factory=dict)


@dataclass
class RAPIDSVersion:
    repositories: dict[str, RAPIDSRepository] = field(default_factory=dict)

    @property
    def all_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package in repository_data.packages
        }

    @property
    def alpha_spec_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package, package_data in repository_data.packages.items()
            if package_data.has_alpha_spec
        }

    @property
    def cuda_suffixed_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package, package_data in repository_data.packages.items()
            if package_data.has_cuda_suffix
        }


@dataclass
class RAPIDSMetadata:
    versions: dict[str, RAPIDSVersion] = field(default_factory=dict)

    def get_current_version(self, directory: PathLike) -> RAPIDSVersion:
        current_version = get_rapids_version(directory)
        try:
            return self.versions[current_version]
        except KeyError:
            max_version, max_version_data = max(
                self.versions.items(), key=lambda item: Version(item[0])
            )
            if Version(current_version) > Version(max_version):
                return max_version_data
            raise
