#!/bin/bash
# Copyright (c) 2024, NVIDIA CORPORATION.

set -euo pipefail

python -m pip wheel . -w "${RAPIDS_WHEEL_BLD_OUTPUT_DIR}" -vv --no-deps --disable-pip-version-check

# Run tests
WHL_FILE=$(ls "${RAPIDS_WHEEL_BLD_OUTPUT_DIR}"/*.whl)
python -m pip install "${WHL_FILE}[test]"
python -m pytest -v tests/

RAPIDS_PY_WHEEL_NAME="rapids-metadata" rapids-upload-wheels-to-s3 python "${RAPIDS_WHEEL_BLD_OUTPUT_DIR}"
