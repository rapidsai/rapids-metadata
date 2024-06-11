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

import contextlib
import json
import os.path
from typing import Generator
from unittest.mock import patch

import pytest
from rapids_metadata import json as rapids_json
from rapids_metadata.metadata import (
    RAPIDSMetadata,
    RAPIDSPackage,
    RAPIDSRepository,
    RAPIDSVersion,
)


@contextlib.contextmanager
def set_cwd(cwd: os.PathLike) -> Generator:
    old_cwd = os.getcwd()
    os.chdir(cwd)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@pytest.mark.parametrize(
    ["unencoded", "encoded"],
    [
        (RAPIDSPackage(), {"has_alpha_spec": True, "has_cuda_suffix": True}),
        (
            RAPIDSRepository(
                packages={
                    "package1": RAPIDSPackage(),
                    "package2": RAPIDSPackage(
                        has_alpha_spec=False, has_cuda_suffix=False
                    ),
                }
            ),
            {
                "packages": {
                    "package1": {
                        "has_alpha_spec": True,
                        "has_cuda_suffix": True,
                    },
                    "package2": {
                        "has_alpha_spec": False,
                        "has_cuda_suffix": False,
                    },
                },
            },
        ),
        (
            RAPIDSVersion(
                repositories={
                    "repo1": RAPIDSRepository(),
                    "repo2": RAPIDSRepository(
                        packages={
                            "package": RAPIDSPackage(),
                        }
                    ),
                    "_nvidia": RAPIDSRepository(
                        packages={
                            "proprietary-package": RAPIDSPackage(),
                        }
                    ),
                }
            ),
            {
                "repositories": {
                    "repo1": {
                        "packages": {},
                    },
                    "repo2": {
                        "packages": {
                            "package": {
                                "has_alpha_spec": True,
                                "has_cuda_suffix": True,
                            },
                        },
                    },
                    "_nvidia": {
                        "packages": {
                            "proprietary-package": {
                                "has_alpha_spec": True,
                                "has_cuda_suffix": True,
                            },
                        },
                    },
                },
            },
        ),
        (
            RAPIDSMetadata(
                versions={
                    "24.06": RAPIDSVersion(),
                    "24.08": RAPIDSVersion(
                        repositories={
                            "repo": RAPIDSRepository(),
                        },
                    ),
                }
            ),
            {
                "versions": {
                    "24.06": {
                        "repositories": {},
                    },
                    "24.08": {
                        "repositories": {
                            "repo": {
                                "packages": {},
                            },
                        },
                    },
                },
            },
        ),
    ],
)
def test_metadata_encoder(unencoded, encoded):
    assert rapids_json._RAPIDSMetadataEncoder().default(unencoded) == encoded


@pytest.mark.parametrize(
    ["version", "args", "expected_json"],
    [
        (
            "24.08.00",
            [],
            {
                "versions": {
                    "24.08": {
                        "repositories": {
                            "repo1": {
                                "packages": {
                                    "package": {
                                        "has_cuda_suffix": True,
                                        "has_alpha_spec": True,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        ),
        (
            "24.10.00",
            [],
            {
                "versions": {
                    "24.10": {
                        "repositories": {
                            "repo2": {
                                "packages": {
                                    "package": {
                                        "has_cuda_suffix": True,
                                        "has_alpha_spec": True,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        ),
        (
            "24.12.00",
            [],
            {
                "versions": {
                    "24.12": {
                        "repositories": {
                            "repo2": {
                                "packages": {
                                    "package": {
                                        "has_cuda_suffix": True,
                                        "has_alpha_spec": True,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        ),
        (
            None,
            ["--all-versions"],
            {
                "versions": {
                    "24.08": {
                        "repositories": {
                            "repo1": {
                                "packages": {
                                    "package": {
                                        "has_cuda_suffix": True,
                                        "has_alpha_spec": True,
                                    },
                                },
                            },
                        },
                    },
                    "24.10": {
                        "repositories": {
                            "repo2": {
                                "packages": {
                                    "package": {
                                        "has_cuda_suffix": True,
                                        "has_alpha_spec": True,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        ),
    ],
)
def test_main(capsys, tmp_path, version, args, expected_json):
    mock_metadata = RAPIDSMetadata(
        versions={
            "24.08": RAPIDSVersion(
                repositories={
                    "repo1": RAPIDSRepository(
                        packages={
                            "package": RAPIDSPackage(),
                        },
                    ),
                },
            ),
            "24.10": RAPIDSVersion(
                repositories={
                    "repo2": RAPIDSRepository(
                        packages={
                            "package": RAPIDSPackage(),
                        },
                    ),
                },
            ),
        },
    )
    if version is not None:
        with open(os.path.join(tmp_path, "VERSION"), "w") as f:
            f.write(f"{version}\n")
    with set_cwd(tmp_path), patch("sys.argv", ["rapids-metadata-json", *args]), patch(
        "rapids_metadata.json.all_metadata", mock_metadata
    ):
        rapids_json.main()
    captured = capsys.readouterr()
    assert json.loads(captured.out) == expected_json
