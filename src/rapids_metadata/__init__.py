# Copyright (c) 2024-2025, NVIDIA CORPORATION.
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
                "libcucim": RAPIDSPackage(has_wheel_package=False),
            }
        ),
        "cudf": RAPIDSRepository(
            packages={
                "cudf": RAPIDSPackage(),
                "cudf-polars": RAPIDSPackage(),
                "cudf_kafka": RAPIDSPackage(),
                "custreamz": RAPIDSPackage(has_wheel_package=False),
                "dask-cudf": RAPIDSPackage(),
                "libcudf": RAPIDSPackage(),
                "libcudf_kafka": RAPIDSPackage(has_wheel_package=False),
            }
        ),
        "cugraph": RAPIDSRepository(
            packages={
                "cugraph": RAPIDSPackage(),
                "cugraph-dgl": RAPIDSPackage(),
                "cugraph-equivariant": RAPIDSPackage(),
                "cugraph-pyg": RAPIDSPackage(),
                "cugraph-service-client": RAPIDSPackage(
                    has_cuda_suffix=False, has_wheel_package=False
                ),
                "cugraph-service-server": RAPIDSPackage(has_wheel_package=False),
                "libcugraph": RAPIDSPackage(has_wheel_package=False),
                "libcugraph_etl": RAPIDSPackage(has_wheel_package=False),
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
                "cuml-cpu": RAPIDSPackage(has_wheel_package=False),
                "libcuml": RAPIDSPackage(has_wheel_package=False),
                "libcuml-tests": RAPIDSPackage(has_wheel_package=False),
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
                "libcuspatial-tests": RAPIDSPackage(has_wheel_package=False),
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
                "libraft-headers-only": RAPIDSPackage(has_wheel_package=False),
                "libraft-static": RAPIDSPackage(has_wheel_package=False),
                "pylibraft": RAPIDSPackage(),
                "raft-ann-bench": RAPIDSPackage(has_wheel_package=False),
                "raft-ann-bench-cpu": RAPIDSPackage(has_wheel_package=False),
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
                "libwholegraph": RAPIDSPackage(has_wheel_package=False),
            }
        ),
    }
)

all_metadata.versions["24.10"] = deepcopy(all_metadata.versions["24.08"])
all_metadata.versions["24.10"].repositories["cudf"].packages["pylibcudf"] = (
    RAPIDSPackage()
)
all_metadata.versions["24.10"].repositories["cuvs"] = RAPIDSRepository(
    packages={
        "cuvs": RAPIDSPackage(),
        "libcuvs": RAPIDSPackage(has_wheel_package=False),
    }
)

all_metadata.versions["24.12"] = deepcopy(all_metadata.versions["24.10"])

# fmt: off
del all_metadata.versions["24.12"].repositories["cugraph"].packages["cugraph-dgl"]
del all_metadata.versions["24.12"].repositories["cugraph"].packages["cugraph-equivariant"]
del all_metadata.versions["24.12"].repositories["cugraph"].packages["cugraph-pyg"]
del all_metadata.versions["24.12"].repositories["cugraph"].packages["nx-cugraph"]
del all_metadata.versions["24.12"].repositories["wholegraph"]
del all_metadata.versions["24.12"].repositories["raft"].packages["raft-ann-bench"]
del all_metadata.versions["24.12"].repositories["raft"].packages["raft-ann-bench-cpu"]
# fmt: on

all_metadata.versions["24.12"].repositories["cugraph-gnn"] = RAPIDSRepository(
    packages={
        "cugraph-dgl": RAPIDSPackage(),
        "cugraph-pyg": RAPIDSPackage(),
        "pylibwholegraph": RAPIDSPackage(),
        "libwholegraph": RAPIDSPackage(has_wheel_package=False),
    }
)

all_metadata.versions["24.12"].repositories["nx-cugraph"] = RAPIDSRepository(
    packages={
        "nx-cugraph": RAPIDSPackage(),
    }
)

all_metadata.versions["24.12"].repositories["cuvs"].packages["cuvs-bench"] = (
    RAPIDSPackage(has_wheel_package=False)
)
all_metadata.versions["24.12"].repositories["cuvs"].packages["cuvs-bench-cpu"] = (
    RAPIDSPackage(has_wheel_package=False)
)
all_metadata.versions["24.12"].repositories["cuvs"].packages["libcuvs-static"] = (
    RAPIDSPackage(has_wheel_package=False)
)

all_metadata.versions["25.02"] = deepcopy(all_metadata.versions["24.12"])
all_metadata.versions["25.02"].repositories["cugraph-docs"] = RAPIDSRepository(
    packages={}
)
