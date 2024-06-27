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

from os import PathLike
from typing import Union

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from .rapids_version import get_rapids_version

__all__ = [
    "RAPIDSMetadata",
    "RAPIDSPackage",
    "RAPIDSRepository",
    "RAPIDSVersion",
]


@dataclass
class RAPIDSPackage:
    (
        """Package published by a RAPIDS repository. Includes both Python packages """
        """and Conda packages."""
    )

    publishes_prereleases: bool = Field(
        default=True,
        description="""Whether or not the package publishes prereleases.""",
    )

    has_cuda_suffix: bool = Field(
        default=True,
        description="""Whether or not the package has a CUDA suffix.""",
    )


@dataclass
class RAPIDSRepository:
    """RAPIDS Git repository. Can publish more than one package."""

    packages: dict[str, RAPIDSPackage] = Field(
        default_factory=dict,
        description="""Dictionary of packages in this repository by name.""",
    )


@dataclass
class RAPIDSVersion:
    """Version of RAPIDS, which contains many Git repositories."""

    repositories: dict[str, RAPIDSRepository] = Field(
        default_factory=dict,
        description="""Dictionary of repositories in this version by name.""",
    )

    @property
    def all_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package in repository_data.packages
        }

    @property
    def prerelease_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package, package_data in repository_data.packages.items()
            if package_data.publishes_prereleases
        }

    @property
    def cuda_suffixed_packages(self) -> set[str]:
        return {
            package
            for repository_data in self.repositories.values()
            for package, package_data in repository_data.packages.items()
            if package_data.has_cuda_suffix
        }


@dataclass(
    config=ConfigDict(
        json_schema_extra={
            "$id": "https://raw.githubusercontent.com/rapidsai/rapids-metadata/main/schemas/rapids-metadata-v1.json",
        },
    )
)
class RAPIDSMetadata:
    """All RAPIDS metadata."""

    versions: dict[str, RAPIDSVersion] = Field(
        default_factory=dict,
        description=(
            """Dictionary of RAPIDS versions by <major>.<minor> """
            """version string."""
        ),
    )

    def get_current_version(
        self, directory: Union[str, PathLike[str]]
    ) -> RAPIDSVersion:
        from packaging.version import Version

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
