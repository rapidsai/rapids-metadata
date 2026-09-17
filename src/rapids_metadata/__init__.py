# Copyright (c) 2024-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
            github_url=None,
            packages={
                "cubinlinker": RAPIDSPackage(publishes_prereleases=False),
            },
        ),
        "cucim": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cucim",
            packages={
                "cucim": RAPIDSPackage(),
                "libcucim": RAPIDSPackage(has_wheel_package=False),
            },
        ),
        "cudf": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cudf",
            packages={
                "cudf": RAPIDSPackage(),
                "cudf-polars": RAPIDSPackage(),
                "cudf_kafka": RAPIDSPackage(
                    has_wheel_package=False, has_cuda_suffix=False
                ),
                "custreamz": RAPIDSPackage(has_wheel_package=False),
                "dask-cudf": RAPIDSPackage(),
                "libcudf": RAPIDSPackage(),
                "libcudf_kafka": RAPIDSPackage(
                    has_wheel_package=False, has_cuda_suffix=False
                ),
            },
        ),
        "cugraph": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cugraph",
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
            },
        ),
        "cugraph-ops": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cugraph-ops",
            packages={
                "libcugraphops": RAPIDSPackage(),
                "pylibcugraphops": RAPIDSPackage(),
            },
        ),
        "cuml": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cuml",
            packages={
                "cuml": RAPIDSPackage(),
                "cuml-cpu": RAPIDSPackage(has_wheel_package=False),
                "libcuml": RAPIDSPackage(has_wheel_package=False),
                "libcuml-tests": RAPIDSPackage(has_wheel_package=False),
            },
        ),
        "cumlprims_mg": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cumlprims_mg",
            packages={
                "libcumlprims": RAPIDSPackage(has_wheel_package=False),
            },
        ),
        "cuspatial": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cuspatial",
            packages={
                "cuspatial": RAPIDSPackage(),
                "libcuspatial": RAPIDSPackage(),
                "libcuspatial-tests": RAPIDSPackage(has_wheel_package=False),
                "cuproj": RAPIDSPackage(),
            },
        ),
        "cuxfilter": RAPIDSRepository(
            github_url="https://github.com/rapidsai/cuxfilter",
            packages={
                "cuxfilter": RAPIDSPackage(),
            },
        ),
        "dask-cuda": RAPIDSRepository(
            github_url="https://github.com/rapidsai/dask-cuda",
            packages={
                "dask-cuda": RAPIDSPackage(has_cuda_suffix=False),
            },
        ),
        "kvikio": RAPIDSRepository(
            github_url="https://github.com/rapidsai/kvikio",
            packages={
                "libkvikio": RAPIDSPackage(),
                "kvikio": RAPIDSPackage(),
            },
        ),
        "ptxcompiler": RAPIDSRepository(
            github_url="https://github.com/rapidsai/ptxcompiler",
            packages={
                "ptxcompiler": RAPIDSPackage(publishes_prereleases=False),
            },
        ),
        "pynvjitlink": RAPIDSRepository(
            github_url="https://github.com/rapidsai/pynvjitlink",
            packages={
                "pynvjitlink": RAPIDSPackage(),
            },
        ),
        "raft": RAPIDSRepository(
            github_url="https://github.com/rapidsai/raft",
            packages={
                "libraft": RAPIDSPackage(has_wheel_package=False),
                "libraft-headers": RAPIDSPackage(has_wheel_package=False),
                "libraft-headers-only": RAPIDSPackage(has_wheel_package=False),
                "libraft-static": RAPIDSPackage(has_wheel_package=False),
                "pylibraft": RAPIDSPackage(),
                "raft-ann-bench": RAPIDSPackage(has_wheel_package=False),
                "raft-ann-bench-cpu": RAPIDSPackage(has_wheel_package=False),
                "raft-dask": RAPIDSPackage(),
            },
        ),
        "rapids-dask-dependency": RAPIDSRepository(
            github_url="https://github.com/rapidsai/rapids-dask-dependency",
            packages={
                "rapids-dask-dependency": RAPIDSPackage(has_cuda_suffix=False),
            },
        ),
        "rmm": RAPIDSRepository(
            github_url="https://github.com/rapidsai/rmm",
            packages={
                "librmm": RAPIDSPackage(),
                "rmm": RAPIDSPackage(),
            },
        ),
        "ucxx": RAPIDSRepository(
            github_url="https://github.com/rapidsai/ucxx",
            packages={
                "distributed-ucxx": RAPIDSPackage(),
                "libucxx": RAPIDSPackage(),
                "ucxx": RAPIDSPackage(),
            },
        ),
        "ucx-py": RAPIDSRepository(
            github_url="https://github.com/rapidsai/ucx-py",
            packages={
                "ucx-py": RAPIDSPackage(),
            },
        ),
        "wholegraph": RAPIDSRepository(
            github_url="https://github.com/rapidsai/wholegraph",
            packages={
                "pylibwholegraph": RAPIDSPackage(),
                "libwholegraph": RAPIDSPackage(has_wheel_package=False),
            },
        ),
    }
)

all_metadata.versions["24.10"] = deepcopy(all_metadata.versions["24.08"])
all_metadata.versions["24.10"].repositories["cudf"].packages["pylibcudf"] = (
    RAPIDSPackage()
)
all_metadata.versions["24.10"].repositories["cuvs"] = RAPIDSRepository(
    github_url="https://github.com/NVIDIA/cuvs",
    packages={
        "cuvs": RAPIDSPackage(),
        "libcuvs": RAPIDSPackage(has_wheel_package=False),
    },
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
    github_url="https://github.com/rapidsai/cugraph-gnn",
    packages={
        "cugraph-dgl": RAPIDSPackage(),
        "cugraph-pyg": RAPIDSPackage(),
        "pylibwholegraph": RAPIDSPackage(),
        "libwholegraph": RAPIDSPackage(has_wheel_package=False),
    },
)

all_metadata.versions["24.12"].repositories["nx-cugraph"] = RAPIDSRepository(
    github_url="https://github.com/rapidsai/nx-cugraph",
    packages={
        "nx-cugraph": RAPIDSPackage(),
    },
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
    github_url="https://github.com/rapidsai/cugraph-docs", packages=dict()
)
del all_metadata.versions["25.02"].repositories["cugraph-ops"]
all_metadata.versions["25.02"].repositories["cugraph"].packages["libcugraph"] = (
    RAPIDSPackage(has_wheel_package=True)
)
all_metadata.versions["25.02"].repositories["cuml"].packages["libcuml"] = RAPIDSPackage(
    has_wheel_package=True
)
all_metadata.versions["25.02"].repositories["cuvs"].packages["libcuvs"] = RAPIDSPackage(
    has_wheel_package=True
)
all_metadata.versions["25.02"].repositories["raft"].packages["libraft"] = RAPIDSPackage(
    has_wheel_package=True
)
all_metadata.versions["25.02"].repositories["cudf"].packages["libcudf-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["cugraph"].packages["libcugraph-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["cuvs"].packages["libcuvs-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["kvikio"].packages["libkvikio-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["raft"].packages["libraft-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["rmm"].packages["librmm-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)
all_metadata.versions["25.02"].repositories["cugraph-gnn"].packages[
    "libwholegraph-tests"
] = RAPIDSPackage(
    publishes_prereleases=True,
    has_cuda_suffix=True,
    has_conda_package=True,
    has_wheel_package=False,
)
all_metadata.versions["25.02"].repositories["ucxx"].packages["libucxx-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)

all_metadata.versions["25.04"] = deepcopy(all_metadata.versions["25.02"])
all_metadata.versions["25.04"].repositories["rapids-logger"] = RAPIDSRepository(
    github_url="https://github.com/rapidsai/rapids-logger",
    packages={"rapids-logger": RAPIDSPackage(has_cuda_suffix=False)},
)
all_metadata.versions["25.04"].repositories["ucxx"].packages["ucxx-tests"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=False,
    )
)

all_metadata.versions["25.06"] = deepcopy(all_metadata.versions["25.04"])
all_metadata.versions["25.06"].repositories["cugraph-gnn"].packages["libwholegraph"] = (
    RAPIDSPackage(has_wheel_package=True)
)
all_metadata.versions["25.06"].repositories["rapids-cli"] = RAPIDSRepository(
    github_url="https://github.com/rapidsai/rapids-cli",
    packages={
        "rapids-cli": RAPIDSPackage(
            publishes_prereleases=False,
            has_cuda_suffix=False,
        ),
    },
)
all_metadata.versions["25.06"].repositories["rapidsmpf"] = RAPIDSRepository(
    github_url="https://github.com/rapidsai/rapidsmpf",
    packages={
        "rapidsmpf": RAPIDSPackage(),
        "librapidsmpf": RAPIDSPackage(),
        "librapidsmpf-tests": RAPIDSPackage(has_wheel_package=False),
    },
)

del all_metadata.versions["25.06"].repositories["cuspatial"]
del all_metadata.versions["25.06"].repositories["cuml"].packages["cuml-cpu"]

all_metadata.versions["25.08"] = deepcopy(all_metadata.versions["25.06"])
del all_metadata.versions["25.08"].repositories["ptxcompiler"]
del all_metadata.versions["25.08"].repositories["cugraph-gnn"].packages["cugraph-dgl"]
del all_metadata.versions["25.08"].repositories["_nvidia"]  # Only cubinlinker

all_metadata.versions["25.10"] = deepcopy(all_metadata.versions["25.08"])
del all_metadata.versions["25.10"].repositories["pynvjitlink"]
del all_metadata.versions["25.10"].repositories["ucx-py"]

all_metadata.versions["25.10"].repositories["cuvs-lucene"] = RAPIDSRepository(
    github_url="https://github.com/NVIDIA/cuvs-lucene",
    packages={
        "cuvs-lucene": RAPIDSPackage(
            publishes_prereleases=False,
            has_cuda_suffix=False,
            has_conda_package=False,
            has_wheel_package=False,
        ),
    },
)

all_metadata.versions["25.12"] = deepcopy(all_metadata.versions["25.10"])
all_metadata.versions["25.12"].repositories["rapids-logger"].packages[
    "rapids-logger"
] = RAPIDSPackage(publishes_prereleases=False, has_cuda_suffix=False)
del (
    all_metadata.versions["25.12"]
    .repositories["cugraph"]
    .packages["cugraph-service-client"]
)
del (
    all_metadata.versions["25.12"]
    .repositories["cugraph"]
    .packages["cugraph-service-server"]
)

all_metadata.versions["26.02"] = deepcopy(all_metadata.versions["25.12"])
del all_metadata.versions["26.02"].repositories["cumlprims_mg"]

all_metadata.versions["26.04"] = deepcopy(all_metadata.versions["26.02"])
all_metadata.versions["26.04"].repositories["nvforest"] = RAPIDSRepository(
    github_url="https://github.com/rapidsai/nvforest",
    packages={
        "libnvforest": RAPIDSPackage(
            publishes_prereleases=True,
            has_cuda_suffix=True,
            has_conda_package=True,
            has_wheel_package=True,
        ),
        "nvforest": RAPIDSPackage(
            publishes_prereleases=True,
            has_cuda_suffix=True,
            has_conda_package=True,
            has_wheel_package=True,
        ),
        "libnvforest-tests": RAPIDSPackage(
            publishes_prereleases=True,
            has_cuda_suffix=True,
            has_conda_package=True,
            has_wheel_package=False,
        ),
    },
)

all_metadata.versions["26.06"] = deepcopy(all_metadata.versions["26.04"])

all_metadata.versions["26.08"] = deepcopy(all_metadata.versions["26.06"])
del all_metadata.versions["26.08"].repositories["cuxfilter"]

all_metadata.versions["26.08"].repositories["cudf"].packages["libcudf-streaming"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=True,
    )
)
all_metadata.versions["26.08"].repositories["cudf"].packages[
    "libcudf-streaming-tests"
] = RAPIDSPackage(
    publishes_prereleases=True,
    has_cuda_suffix=True,
    has_conda_package=True,
    has_wheel_package=False,
)

all_metadata.versions["26.08"].repositories["cudf"].packages["cudf-streaming"] = (
    RAPIDSPackage(
        publishes_prereleases=True,
        has_cuda_suffix=True,
        has_conda_package=True,
        has_wheel_package=True,
    )
)
all_metadata.versions["26.10"] = deepcopy(all_metadata.versions["26.08"])
del all_metadata.versions["26.10"].repositories["cuvs-lucene"]

# These repositories moved to the NVIDIA organization for the 26.10 release.
for repository in ("cudf", "cuml", "raft"):
    all_metadata.versions["26.10"].repositories[
        repository
    ].github_url = f"https://github.com/NVIDIA/{repository}"

all_metadata.versions["26.10"].repositories["cuvs"].packages["cuvs-lucene"] = (
    RAPIDSPackage(
        publishes_prereleases=False,
        has_cuda_suffix=False,
        has_conda_package=False,
        has_wheel_package=False,
    )
)
