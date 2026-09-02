#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project VITAL Security Testing — Stage 1"
python3 --version
python3 -m py_compile "$ROOT/security_baseline.py" "$ROOT/unauthenticated_check.py" "$ROOT/fixtures/security_fixture_server.py" "$ROOT/tests/test_security_fixture.py"
echo "Python syntax validation: PASS"
bash "$ROOT/run_security_ci_local.sh"
echo "STAGE 1 SECURITY VALIDATION PASSED"
