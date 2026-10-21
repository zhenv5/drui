#!/usr/bin/env bash
set -euo pipefail
SOURCE="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
export HOME="$T/home"
mkdir -p "$HOME"
# Local Git clone exercises the exact on-disk layout with .git but not network.
git clone --quiet --no-hardlinks "$SOURCE" "$HOME/GameAgentKit"
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify --json > "$T/verification.json"
python3 -c 'import json,sys; r=json.load(open(sys.argv[1])); assert r["summary"]["complete"]; assert len(r["agents"]) == 4' "$T/verification.json"
"$HOME/GameAgentKit/scripts/drui" version
"$HOME/GameAgentKit/scripts/drui" list --beginner
"$HOME/GameAgentKit/scripts/drui" deps conflicts
