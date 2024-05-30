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

from .metadata import Metadata
from .rapids_version import get_rapids_version


__all__ = ["get_metadata", "metadata"]

def get_metadata(directory: PathLike=None) -> Metadata:
    return metadata[get_rapids_version(directory)]

metadata: dict[str, Metadata] = {}

metadata["24.08"] = Metadata()
metadata["24.08"].packages.update({
    "cubinlinker",
    "cucim",
    "cudf",
    "cugraph",
    "cugraph-dgl",
    "cugraph-equivariant",
    "cugraph-pyg",
    "cuml",
    "cuproj",
    "cuspatial",
    "cuxfilter",
    "dask-cuda",
    "dask-cudf",
    "distributed-ucxx",
    "libcuml",
    "libcuml-tests",
    "libcumlprims",
    "libraft",
    "libraft-headers",
    "librmm",
    "libucx",
    "nx-cugraph",
    "ptxcompiler",
    "pylibcugraph",
    "pylibcugraphops",
    "pylibraft",
    "pylibwholegraph",
    "pynvjitlink",
    "raft-dask",
    "rapids-dask-dependency",
    "rmm",
    "ucx-py",
    "ucxx",
})
metadata["24.08"].non_cuda_suffixed_packages.update({
    "dask-cuda",
})
