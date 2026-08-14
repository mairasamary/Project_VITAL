#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"

echo "== Project VITAL Benchmark Utility Validation =="
echo
echo "Running SMALL only."
echo

python3 "${ROOT}/environment/data-testing/benchmark.py" \
  --size small \
  --seed 314159

echo
echo "Checking generated reports..."

CSV="${ROOT}/.project-vital/data-testing/benchmark-results/benchmark-results.csv"
MD="${ROOT}/.project-vital/data-testing/benchmark-results/benchmark-results.md"

test -s "${CSV}"
test -s "${MD}"

grep -q "small" "${CSV}"
grep -q "valid" "${CSV}"
grep -q "Project VITAL" "${MD}"

echo
echo "BENCHMARK UTILITY VALIDATION PASSED"
echo "CSV: ${CSV}"
echo "MD:  ${MD}"
