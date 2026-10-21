# Repeat first-time user review — DRUI v1.4.5

**Review mode:** Separate beginner usability walkthrough, simulating a fresh user, not an externally recruited human test session.

## First task: install safely

- Follow `README → Install via Agent` or `README → Terminal` to clone a reviewed GitHub Tag.
- `install.sh` shares Skills using symlinks and prints compact verification; `drui start` next suggests an initial read-only task.
- **New finding (P1):** Previously, users attempting `--copy` on a filesystem where they preferred copying might see Skill files installed but a failed verifier. **Fixed** by rejecting `--copy` before any writes and explaining why.
- **New finding (P1):** Existing Agent Skill directory links can silently redirect new files to a different directory. **Fixed** by refusing symlinked parents and directing users to inspect them manually rather than deleting them.

## Repeat user flow

1. Clone stable GitHub source Tag into unused `~/GameAgentKit`.
2. Run dry-run; if a linked parent/unknown location appears, stop and inspect.
3. Install all four Agents or only the desired Agent; do not mix the verification scopes.
4. Read `DRUI ... PASS` (one-line); `runtime untested` accurately says Agent-loading wasn't tested.
5. Run `drui start` or the absolute CLI path, then try a read-only `usability-review` on an example project.
6. For `FAIL`, use `drui verify --verbose` and consult the troubleshooting table; never force-overwrite personal Skills.

**Not verified:** No real beginner observed independently; no macOS app testing, no runtime Agent skill invocation. Confidence limited to code/doc walkthrough + CI test evidence.

## Third-pass beginner re-check

A failure on the fourth Agent should not unexpectedly leave the first three installed. The new install/link preflight rejects existing redirected destination directories **before** starting any writes. Beginner action: inspect the offending path; do not force-remove it. Retrying after manually resolving the layout is safe but should still run a scoped `drui verify`.
