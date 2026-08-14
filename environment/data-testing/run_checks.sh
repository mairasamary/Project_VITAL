#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT="${ROOT}/.project-vital/data-testing/validation-small"
rm -rf "${OUT}"

python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small --seed 42 --output "${OUT}"

python3 "${ROOT}/environment/data-testing/validate_data.py" "${OUT}"

python3 "${ROOT}/environment/data-testing/test_generator.py"
