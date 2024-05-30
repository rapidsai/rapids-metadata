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

import pytest
from rapids_metadata import rapids_version


@contextlib.contextmanager
def set_cwd(cwd: os.PathLike):
    old_cwd = os.getcwd()
    os.chdir(cwd)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@pytest.mark.parametrize(
    ["dirname", "version"],
    [
        (".", FileNotFoundError),
        ("dir1", "24.08"),
        ("dir1/dir2", "24.06"),
        ("dir1/dir2/dir3", "24.06"),
    ],
)
def test_get_rapids_version(tmp_path, dirname, version):
    os.makedirs(os.path.join(tmp_path, "dir1/dir2/dir3"))
    with open(os.path.join(tmp_path, "dir1/VERSION"), "w") as f:
        f.write("24.08\n")
    with open(os.path.join(tmp_path, "dir1/dir2/VERSION"), "w") as f:
        f.write("24.06.00a1\n")

    abs_dir = os.path.join(tmp_path, dirname)
    if isinstance(version, type) and issubclass(version, BaseException):
        with pytest.raises(version):
            rapids_version.get_rapids_version(abs_dir)
        with set_cwd(abs_dir):
            with pytest.raises(version):
                rapids_version.get_rapids_version()
    else:
        assert rapids_version.get_rapids_version(abs_dir) == version
        with set_cwd(abs_dir):
            assert rapids_version.get_rapids_version() == version
