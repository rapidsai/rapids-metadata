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

from . import metadata as md


__all__ = ["rapids_metadata"]


rapids_metadata: md.RAPIDSMetadata = md.RAPIDSMetadata()

rapids_metadata.versions["24.08"] = md.RAPIDSVersion(repositories={
    repository: md.RAPIDSRepository(packages={package: md.RAPIDSPackage(**overrides) for package, overrides in packages.items()}) for repository, packages in {
        md.PseudoRepository.NVIDIA: {
            "cubinlinker": {},
        },
        "cucim": {
            "cucim": {},
        },
        "cudf": {
            "cudf": {},
            "dask-cudf": {},
        },
        "cugraph": {
            "cugraph": {},
            "cugraph-dgl": {},
            "cugraph-equivariant": {},
            "cugraph-pyg": {},
            "nx-cugraph": {},
            "pylibcugraph": {},
        },
        "cugraph-ops": {
            "pylibcugraphops": {},
        },
        "cuml": {
            "cuml": {},
            "libcuml": {},
            "libcuml-tests": {},
        },
        "cumlprims_mg": {
            "libcumlprims": {},
        },
        "cuproj": {
            "cuproj": {},
        },
        "cuspatial": {
            "cuspatial": {},
        },
        "cuxfilter": {
            "cuxfilter": {},
        },
        "dask-cuda": {
            "dask-cuda": {
                "has_cuda_suffix": False,
            },
        },
        "ptxcompiler": {
            "ptxcompiler": {},
        },
        "pynvjitlink": {
            "pynvjitlink": {},
        },
        "raft": {
            "libraft": {},
            "libraft-headers": {},
            "pylibraft": {},
            "raft-dask": {},
        },
        "rapids-dask-dependency": {
            "rapids-dask-dependency": {},
        },
        "rmm": {
            "librmm": {},
            "rmm": {},
        },
        "ucxx": {
            "distributed-ucxx": {},
            "libucxx": {},
            "ucxx": {},
        },
        "ucx-py": {
            "ucx-py": {},
        },
        "wholegraph": {
            "pylibwholegraph": {},
        },
    }.items()
})
