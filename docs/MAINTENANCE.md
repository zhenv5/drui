# DRUI GitHub source maintenance

Install from the reviewed official GitHub [source-only Release](https://github.com/zhenv5/drui/releases/latest). No ZIP installer. See [INSTALL_AND_VERIFY.md](INSTALL_AND_VERIFY.md) for the complete manual CLI/Agent workflow, troubleshooting and security boundaries.

```bash
"$HOME/GameAgentKit/scripts/drui" version
"$HOME/GameAgentKit/scripts/drui" verify    # one-line, read-only summary
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --check
# Review release changes and make sure git status is clean:
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --yes
python3 "$HOME/GameAgentKit/gamekit.py" link --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify    # must exit 0
```

As of v1.4.4, `install.sh` and `link` **propagate failed post-install verification via a nonzero exit code** (while preserving user-owned same-name Skills). Keep a separately executed `verify` for audit or specific-Agent scope. Four agents use five Skill slots, so the default full check expects 60 links. Use `verify --verbose` for details or `--json` for tooling. `--agents all` now includes Cursor, consistent with the default verification scope.

`--check` is read-only, and update requires an official origin and clean Git checkout. Checkout is not crash-atomic; inspect status after an interruption, do not forcibly reset user modifications.

DRUI never upgrades third-party Skills. `deps check` requires an opt-in approved fingerprint baseline; the absence of this baseline is not an install failure. Run `deps list` and independently review before optionally using `deps lock`. Successful local verification does not prove real Agent discovery/loading.

## Maintainer release checklist (source-only)

1. Open a PR and update root `VERSION`, `gamekit.py`'s version constant, `tests/test_public_release.py` and `.github/workflows/publish.yml`'s exact version assertion. Update `CHANGELOG.md`. Keep the public release number separate from archived **GameAgentKit internal historical** version labels.
2. Audit current-version clone examples in `README.md`, `QUICKSTART.md`, `docs/INSTALL_AND_VERIFY.md`, `docs/DRUI_USAGE.md` and `docs/DRUI_REVIEW_CHEATSHEET_ZH.md`. Do not rewrite frozen legacy changelog history.
3. Ensure `prompts/agent-setup/install.txt` and `update.txt` match the mirrored README blocks exactly; maintain CLI `drui agent`/`drui copy` contract. The install/update prompts must check `drui verify` return codes and keep output compact.
4. Run `python3 -m unittest discover -s tests -v` and `bash tests/smoke_git_install.sh`. GitHub CI must pass on the PR before merging.
5. Merge to `main` after approval. `.github/workflows/publish.yml` automatically creates the annotated Tag `v$(cat VERSION)` and **source-only GitHub Release**. Do **not** manually push a parallel tag or rerun a historical ZIP-publishing workflow.
6. Check both CI and publishing workflow results; confirm the new Tag points to the merged commit, Release is non-draft/non-prerelease, and **no installer ZIP** was attached. Never move a published tag.
7. Verify the canonical GitHub clone/dry-run/install/`drui verify` flow in CI. Genuine Agent discovery and execution still require separate local Codex/Claude/Antigravity/Cursor testing; filesystem verification alone must not be described as Agent-loaded.

**Trust notes:** A Git Tag is not intrinsically immutable or signed; protect repository administration and release permissions. An interrupted checkout is not an atomic upgrade.

**Install safety check:** `install --copy` and `link --copy` fail before any file changes; only managed symlink deployments are supported. A symlinked parent in Agent Skill target paths is refused (prevents unintended writes elsewhere). Do not silently delete or dereference user-owned directories; manually resolve before retrying. Document this in the novice setup guide.
