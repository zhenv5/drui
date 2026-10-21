#!/usr/bin/env bash
set -u
printf 'OS: %s\n' "$(uname -s)"
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'BLOCKED: native Xcode builds and iOS simulators need macOS.'
  exit 2
fi
if ! command -v xcodebuild >/dev/null 2>&1; then
  echo 'BLOCKED: xcodebuild not installed.'; exit 2
fi
xcodebuild -version || exit 2
xcrun simctl list devices available | head -30
printf '\nNOTE: Environment check only; no project build or UI run was performed.\n'
