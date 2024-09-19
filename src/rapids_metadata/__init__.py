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

from copy import deepcopy

from .metadata import (
    RAPIDSMetadata,
    RAPIDSPackage,
    RAPIDSRepository,
    RAPIDSVersion,
)


__all__ = ["all_metadata"]


all_metadata: RAPIDSMetadata = RAPIDSMetadata()

all_metadata.versions["24.08"] = RAPIDSVersion(
    repositories={
        "_nvidia": RAPIDSRepository(
            packages={
                "cubinlinker": RAPIDSPackage(publishes_prereleases=False),
            }
        ),
        "cucim": RAPIDSRepository(
            packages={
                "cucim": RAPIDSPackage(),
            }
        ),
        "cudf": RAPIDSRepository(
            packages={
                "cudf": RAPIDSPackage(),
                "cudf-polars": RAPIDSPackage(),
                "cudf_kafka": RAPIDSPackage(),
                "dask-cudf": RAPIDSPackage(),
                "libcudf": RAPIDSPackage(),
            }
        ),
        "cugraph": RAPIDSRepository(
            packages={
                "cugraph": RAPIDSPackage(),
                "cugraph-dgl": RAPIDSPackage(),
                "cugraph-equivariant": RAPIDSPackage(),
                "cugraph-pyg": RAPIDSPackage(),
                "cugraph-service-client": RAPIDSPackage(has_cuda_suffix=False),
                "cugraph-service-server": RAPIDSPackage(),
                "nx-cugraph": RAPIDSPackage(),
                "pylibcugraph": RAPIDSPackage(),
            }
        ),
        "cugraph-ops": RAPIDSRepository(
            packages={
                "libcugraphops": RAPIDSPackage(),
                "pylibcugraphops": RAPIDSPackage(),
            }
        ),
        "cuml": RAPIDSRepository(
            packages={
                "cuml": RAPIDSPackage(),
                "libcuml": RAPIDSPackage(),
                "libcuml-tests": RAPIDSPackage(),
            }
        ),
        "cumlprims_mg": RAPIDSRepository(
            packages={
                "libcumlprims": RAPIDSPackage(),
            }
        ),
        "cuproj": RAPIDSRepository(
            packages={
                "cuproj": RAPIDSPackage(),
            }
        ),
        "cuspatial": RAPIDSRepository(
            packages={
                "cuspatial": RAPIDSPackage(),
                "libcuspatial": RAPIDSPackage(),
                "libcuspatial-tests": RAPIDSPackage(),
            }
        ),
        "cuxfilter": RAPIDSRepository(
            packages={
                "cuxfilter": RAPIDSPackage(),
            }
        ),
        "dask-cuda": RAPIDSRepository(
            packages={
                "dask-cuda": RAPIDSPackage(has_cuda_suffix=False),
            }
        ),
        "kvikio": RAPIDSRepository(
            packages={
                "libkvikio": RAPIDSPackage(),
                "kvikio": RAPIDSPackage(),
            }
        ),
        "ptxcompiler": RAPIDSRepository(
            packages={
                "ptxcompiler": RAPIDSPackage(publishes_prereleases=False),
            }
        ),
        "pynvjitlink": RAPIDSRepository(
            packages={
                "pynvjitlink": RAPIDSPackage(),
            }
        ),
        "raft": RAPIDSRepository(
            packages={
                "libraft": RAPIDSPackage(),
                "libraft-headers": RAPIDSPackage(),
                "pylibraft": RAPIDSPackage(),
                "raft-dask": RAPIDSPackage(),
            }
        ),
        "rapids-dask-dependency": RAPIDSRepository(
            packages={
                "rapids-dask-dependency": RAPIDSPackage(has_cuda_suffix=False),
            }
        ),
        "rmm": RAPIDSRepository(
            packages={
                "librmm": RAPIDSPackage(),
                "rmm": RAPIDSPackage(),
            }
        ),
        "ucxx": RAPIDSRepository(
            packages={
                "distributed-ucxx": RAPIDSPackage(),
                "libucxx": RAPIDSPackage(),
                "ucxx": RAPIDSPackage(),
            }
        ),
        "ucx-py": RAPIDSRepository(
            packages={
                "ucx-py": RAPIDSPackage(),
            }
        ),
        "wholegraph": RAPIDSRepository(
            packages={
                "pylibwholegraph": RAPIDSPackage(),
            }
        ),
    }
)

all_metadata.versions["24.10"] = deepcopy(all_metadata.versions["24.08"])

all_metadata.versions["24.12"] = deepcopy(all_metadata.versions["24.10"])
