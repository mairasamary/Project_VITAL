#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
BASE="${ROOT}/.project-vital/data-testing/local-ci"

rm -rf "${BASE}"
mkdir -p "${BASE}"

echo "== 1. Generator unit tests =="
python3 "${ROOT}/environment/data-testing/test_generator.py"

echo
echo "== 2. Generate deterministic 25-patient dataset =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small \
  --patients 25 \
  --seed 424242 \
  --output "${BASE}/sample"

echo
echo "== 3. Validate deterministic sample =="
python3 "${ROOT}/environment/data-testing/validate_data.py" \
  "${BASE}/sample"

echo
echo "== 4. Verify reproducibility =="
python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small \
  --patients 25 \
  --seed 424242 \
  --output "${BASE}/repro-a"

python3 "${ROOT}/environment/data-testing/generate_data.py" \
  --size small \
  --patients 25 \
  --seed 424242 \
  --output "${BASE}/repro-b"

diff -q "${BASE}/repro-a/patients.csv" "${BASE}/repro-b/patients.csv"
diff -q "${BASE}/repro-a/encounters.csv" "${BASE}/repro-b/encounters.csv"
diff -q "${BASE}/repro-a/vitals.csv" "${BASE}/repro-b/vitals.csv"

echo
echo "== 5. Verify validator rejects controlled corruption =="
cp -R "${BASE}/sample" "${BASE}/broken"

python3 "${ROOT}/environment/data-testing/corrupt_data.py" \
  "${BASE}/broken" \
  --defect orphan-vitals

set +e
python3 "${ROOT}/environment/data-testing/validate_data.py" \
  "${BASE}/broken"
rc=$?
set -e

if [ "${rc}" -eq 0 ]; then
  echo "ERROR: validator unexpectedly accepted corrupted data."
  exit 1
fi

echo "Validator correctly rejected corrupted data."
echo
echo "LOCAL DATA CI CHECKS PASSED"
