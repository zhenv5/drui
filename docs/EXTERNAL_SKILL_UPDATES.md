# Third-party Skill upgrades: current DRUI dependency policy

**No silent dependency upgrades.** `drui update` only switches the official GitHub-tagged GameAgentKit source and bundled DRUI/Oil UI Plus. External Skills belong to their respective publishers or the user. A symlink may expose upstream changes instantly, so DRUI verifies the approved **content fingerprint** rather than assuming an unchanged install.

## Recommended workflow

```bash
# Optional opt-in baseline, only after reviewing external Skills and their sources:
drui deps list
drui deps conflicts
drui deps lock  # opt-in; do NOT auto-lock during install/update

# Before a DRUI review, and after updating any external Skill:
drui deps check
drui deps conflicts --project /path/to/my-game

drui sources --agent codex

# After independent review and a real compatibility test:
drui deps approve --name oil-ui --agent codex --evidence /path/to/approved-review.md

# Recheck; if the same source is shared by several agents, approve each scope:
drui deps check --agent codex
```

- `deps list`: shows installed third-party Skill source directories and SHA-256 prefixes (does not execute them).
- `deps lock`: makes a local baseline **only once** in `~/GameAgentKit/.state/external-skills.lock.json`. Do this after you have reviewed what is installed. The baseline is not proof of safety.
- `deps check`: reports `OK`, `NEW`, `CHANGED`, `MISSING`; returns nonzero if drift is detected. **No existing baseline also returns nonzero; it is not a bundled DRUI installation failure**. Never auto-create a lock just to suppress this result. This operation does not modify the lock.
- `deps approve`: requires a non-empty on-disk written compatibility review; backs up and updates only the selected external Skill fingerprint. **It records human/agent approval, not proof of actual runtime safety.**
- `drui sources`: auto-selects official `oil-ui-pro` if installed and approved; otherwise bundled `oil-ui-plus`, then approved open `oil-ui`, then DRUI generic. If no lock exists, mark external sources as `UNLOCKED` and do not claim verified compatibility.
- **For forced sources** (`drui prompt full --ui-source pro`): an unapproved external version is an error, never silent downgrade.
- A lock file is **local state**, not published in Git or GameAgentKit releases; external Skills are not redistributed.
- A change to a nested file or required asset invalidates its fingerprint. It is intentionally conservative.

## Reviewing upstream changes

1. Inspect the upstream changelog and diff; confirm publisher and license. Do not execute unfamiliar install scripts automatically.
2. Check changes to `SKILL.md`, tool permissions, commands, configuration paths, and output contracts.
3. Run a small read-only DRUI visual-review in a disposable workspace, then a limited real task with captured evidence and QA.
4. Write the review evidence file with results/known issues; run `drui deps approve` only if satisfactory.
5. If incompatible: leave it flagged, use bundled `oil-ui-plus`, pin or restore the old upstream dependency yourself. DRUI cannot roll back third-party packages for you.

**Limits:** SHA-256 detects file changes but does not validate semantics, prevent external scripts from running inside another agent, or prove three-party independent review. Actual Agent loading and runtime testing remain necessary.

## User installs a same-name Skill or upgrades it themselves

**User-installed Skills always remain user-owned.** GameAgentKit installs symlinks only into EMPTY target names and never overwrites a real file, directory or different symlink. If the name is already occupied, it records a `COLLISION` and preserves the user's installation. A user may independently upgrade it; GameAgentKit never executes an upstream installer or performs rollback.

- `drui deps conflicts`: shows paths that reuse a bundled Skill name such as `game-feel-polish`, `drui`, or `oil-ui-plus`. With `--project` it ALSO inspects typical local Skill locations. Because Agent resolution differs by version, the report warns rather than claims which copy wins.
- `drui deps list`: lists **all unmanaged skills**, including user copies with the same name as a built-in Skill, their resolved directories and file hashes.
- `drui deps lock` / `drui deps check`: preserve a content baseline for each Agent installation slot. If the user upgrades the Skill themselves, it becomes `CHANGED`, not silently accepted. The files are NEVER modified.
- `drui deps approve --name game-feel-polish --evidence REVIEW.md`: after inspecting the diff and testing actual Agent loading, approves a new fingerprint for the requested name in the specified Agent scope (does not install, downgrade, or move the Skill).
- If an external copy shadows our bundled `oil-ui-plus` or `drui`, DRUI CLI refuses to claim the bundled one is selected. Rename/remove only with the user's explicit consent; the safest alternative is leaving both untouched and manually choosing a distinct Skill name.
- **Project-specific Skills may override or coexist with global ones depending on Agent implementation**. This tool reports likely conflicts; it cannot guarantee the Agent runtime's actual loading order.
- Bundled GameAgentKit files are managed separately from user installs. Do not put a hand-maintained independent Skill *inside* `~/GameAgentKit/skills`; put it in your own directory and link it with `register-external`.

No content checksum can ensure an upgraded third-party Skill is benign or compatible; passing the fingerprint check only indicates matching previously reviewed files.

For installation success use `drui verify` (filesystem links, concise by default). This is a separate check from optional external Skill fingerprint approval. For full four-Agent coverage use `--agent codex,claude,antigravity,cursor`, because `all` now includes Cursor. See [Install & Verify](INSTALL_AND_VERIFY.md).
