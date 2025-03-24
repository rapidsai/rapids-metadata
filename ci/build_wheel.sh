#!/bin/bash
# Copyright (c) 2024, NVIDIA CORPORATION.

set -euo pipefail

wheel_dir="${RAPIDS_WHEEL_BLD_OUTPUT_DIR}"

mkdir -p "${wheel_dir}"

python -m pip wheel . -w "${wheel_dir}" -vv --no-deps --disable-pip-version-check

# Run tests
WHL_FILE=$(ls "${wheel_dir}"/*.whl)
python -m pip install "${WHL_FILE}[test]"
python -m pytest -v tests/

RAPIDS_PY_WHEEL_NAME="rapids-metadata" rapids-upload-wheels-to-s3 python "${wheel_dir}"
