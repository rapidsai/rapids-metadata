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
import os.path
import re
from textwrap import dedent
from typing import Generator, Union
from unittest.mock import patch

import pytest
from pydantic import TypeAdapter
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
        (
            RAPIDSPackage(),
            {
                "publishes_prereleases": True,
                "has_cuda_suffix": True,
                "has_conda_package": True,
                "has_wheel_package": True,
            },
        ),
        (
            RAPIDSPackage(has_conda_package=False),
            {
                "publishes_prereleases": True,
                "has_cuda_suffix": True,
                "has_conda_package": False,
                "has_wheel_package": True,
            },
        ),
        (
            RAPIDSPackage(has_wheel_package=False),
            {
                "publishes_prereleases": True,
                "has_cuda_suffix": True,
                "has_conda_package": True,
                "has_wheel_package": False,
            },
        ),
        (
            RAPIDSRepository(
                packages={
                    "package1": RAPIDSPackage(),
                    "package2": RAPIDSPackage(
                        publishes_prereleases=False, has_cuda_suffix=False
                    ),
                }
            ),
            {
                "packages": {
                    "package1": {
                        "publishes_prereleases": True,
                        "has_cuda_suffix": True,
                        "has_conda_package": True,
                        "has_wheel_package": True,
                    },
                    "package2": {
                        "publishes_prereleases": False,
                        "has_cuda_suffix": False,
                        "has_conda_package": True,
                        "has_wheel_package": True,
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
                                "publishes_prereleases": True,
                                "has_cuda_suffix": True,
                                "has_conda_package": True,
                                "has_wheel_package": True,
                            },
                        },
                    },
                    "_nvidia": {
                        "packages": {
                            "proprietary-package": {
                                "publishes_prereleases": True,
                                "has_cuda_suffix": True,
                                "has_conda_package": True,
                                "has_wheel_package": True,
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
    assert TypeAdapter(type(unencoded)).dump_python(unencoded) == encoded


@pytest.mark.parametrize(
    ["version", "args", "expected_json"],
    [
        (
            "24.08.00",
            [],
            "{"
            '"versions":{'
            '"24.08":{'
            '"repositories":{'
            '"repo1":{'
            '"packages":{'
            '"package":{'
            '"has_conda_package":true,'
            '"has_cuda_suffix":true,'
            '"has_wheel_package":true,'
            '"publishes_prereleases":true'
            "}"
            "}"
            "}"
            "}"
            "}"
            "}"
            "}",
        ),
        (
            "24.10.00",
            [],
            "{"
            '"versions":{'
            '"24.10":{'
            '"repositories":{'
            '"repo2":{'
            '"packages":{'
            '"package":{'
            '"has_conda_package":true,'
            '"has_cuda_suffix":true,'
            '"has_wheel_package":true,'
            '"publishes_prereleases":true'
            "}"
            "}"
            "}"
            "}"
            "}"
            "}"
            "}",
        ),
        (
            "24.12.00",
            [],
            "{"
            '"versions":{'
            '"24.12":{'
            '"repositories":{'
            '"repo2":{'
            '"packages":{'
            '"package":{'
            '"has_conda_package":true,'
            '"has_cuda_suffix":true,'
            '"has_wheel_package":true,'
            '"publishes_prereleases":true'
            "}"
            "}"
            "}"
            "}"
            "}"
            "}"
            "}",
        ),
        (
            None,
            ["--all-versions"],
            "{"
            '"versions":{'
            '"24.08":{'
            '"repositories":{'
            '"repo1":{'
            '"packages":{'
            '"package":{'
            '"has_conda_package":true,'
            '"has_cuda_suffix":true,'
            '"has_wheel_package":true,'
            '"publishes_prereleases":true'
            "}"
            "}"
            "}"
            "}"
            "},"
            '"24.10":{'
            '"repositories":{'
            '"repo2":{'
            '"packages":{'
            '"package":{'
            '"has_conda_package":true,'
            '"has_cuda_suffix":true,'
            '"has_wheel_package":true,'
            '"publishes_prereleases":true'
            "}"
            "}"
            "}"
            "}"
            "}"
            "}"
            "}",
        ),
        (
            "24.08.00",
            ["--pretty"],
            dedent(
                """\
                {
                  "versions": {
                    "24.08": {
                      "repositories": {
                        "repo1": {
                          "packages": {
                            "package": {
                              "has_conda_package": true,
                              "has_cuda_suffix": true,
                              "has_wheel_package": true,
                              "publishes_prereleases": true
                            }
                          }
                        }
                      }
                    }
                  }
                }
                """
            ),
        ),
        (
            None,
            ["--schema"],
            re.compile(
                r'"\$id":"https://raw.githubusercontent.com/rapidsai/rapids-metadata/main/schemas/rapids-metadata-v1.json"'
            ),
        ),
    ],
)
def test_main(
    capsys: pytest.CaptureFixture[str],
    tmp_path: str,
    version: Union[str, None],
    args: list[str],
    expected_json: Union[str, re.Pattern],
):
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

    def check_output(output: str):
        if isinstance(expected_json, re.Pattern):
            assert expected_json.search(output)
        else:
            assert output == expected_json

    with set_cwd(tmp_path), patch("sys.argv", ["rapids-metadata-json", *args]), patch(
        "rapids_metadata.json.all_metadata", mock_metadata
    ):
        rapids_json.main()
    captured = capsys.readouterr()
    check_output(captured.out)

    with set_cwd(tmp_path), patch("rapids_metadata.json.all_metadata", mock_metadata):
        rapids_json.main(args)
    captured = capsys.readouterr()
    check_output(captured.out)

    with set_cwd(tmp_path), patch(
        "sys.argv", ["rapids-metadata-json", *args, "-o", "rapids-metadata.json"]
    ), patch("rapids_metadata.json.all_metadata", mock_metadata):
        rapids_json.main()
        with open("rapids-metadata.json") as f:
            written_json = f.read()
    captured = capsys.readouterr()
    assert captured.out == ""
    check_output(written_json)
