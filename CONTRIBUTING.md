# Contributing

Contributions to general-purpose game-development workflow skills are welcome.

1. Discuss larger changes in a GitHub issue first.
2. Do not include copyrighted/proprietary Oil UI Pro content, third-party skills, model weights, paid templates, private screenshots or credentials.
3. Make a branch, edit a `SKILL.md` or its prompt, add/adjust tests, and run `python3 -m unittest discover -s tests -v`.
4. Open a PR with reproducible changes, clear scope, and tested Agent paths.
5. For releases, update root `VERSION`, `gamekit.py`'s `VERSION`, `.github/workflows/publish.yml`'s version assertion, `tests/test_public_release.py`, and `CHANGELOG.md`. Check current-version examples in README/Quickstart/docs. Do not manually push a competing tag.
6. Merge the reviewed PR after CI succeeds. The `publish.yml` workflow creates the source-only Git tag and GitHub Release. Confirm the publish workflow succeeded and the tag points at the merged commit; never move a published tag. GitHub's auto-generated source archives are not DRUI installers.
7. Follow the [maintainer release checklist](docs/MAINTENANCE.md) and [installation guide](docs/INSTALL_AND_VERIFY.md) for release verification.

Security issues: follow [SECURITY.md](SECURITY.md).
