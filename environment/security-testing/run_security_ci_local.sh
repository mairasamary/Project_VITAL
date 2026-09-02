#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT/fixtures/security_fixture_server.py" --port 8765 >/dev/null 2>&1 &
PID=$!
trap 'kill "$PID" >/dev/null 2>&1 || true' EXIT
for _ in $(seq 1 30); do
  if python3 -c 'import http.client;c=http.client.HTTPConnection("127.0.0.1",8765,timeout=.2);c.request("GET","/");r=c.getresponse();r.read();c.close()' 2>/dev/null; then break; fi
  sleep .1
done
python3 "$ROOT/tests/test_security_fixture.py"
