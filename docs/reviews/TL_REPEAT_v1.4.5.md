# Repeat TL review — DRUI v1.4.5

**Review mode:** Separate Tech Lead lens, evaluated against v1.4.4 source and tests before comparison with the novice lens. This is not a separate human reviewer or isolated external coding agent.

## Pass A — new findings

| ID | Severity | Evidence | Implemented check |
|---|---|---|---|
| TL-05-01 | P1 | `ensure_link` checks final destination but can create entries under a symlinked parent, redirecting writes outside the user's intended Agent folder | Refuse pre-existing symlinks in destination parent path; add outside-directory unchanged regression |
| TL-05-02 | P1 | `--copy` was accepted while `drui verify` only accepts exact bundled symlink and Git source updates do not maintain copies | Fail fast in public install/link entrypoints before copying any Skill; regression asserts no partial install |
| TL-05-03 | P2 | Updater module documented Tag as immutable despite maintainer ability to move Git tags | Correct docstring to reviewed/tagged provenance, not immutable attestation |

## Pass B — review gates

- Verify failed installs return nonzero and existing same-name Skills remain untouched.
- Confirm default four-Agent Git-clone smoke, one-Agent verification, JSON and compact output remain unchanged.
- Confirm no undocumented ZIP installation returns; `README`, `QUICKSTART`, source docs and version in sync.
- Inspect GitHub CI logs and run a fresh independent source review after fixes. Document any new issues instead of claiming impossibility of future bugs.

**Scope limitation:** Direct Mac/GUI Agent Skill loading, GitHub signer attestation, update interruption recovery, and symlink race-free guarantees not established by local CI. They remain separate acceptance activities.
