#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is required to install GameAgentKit.' >&2
  exit 1
fi
exec python3 "$BASE/gamekit.py" install "$@"
