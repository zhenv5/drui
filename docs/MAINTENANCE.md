# Maintenance and safety

## One source of truth

Each bundled skill is a physical folder under `~/GameAgentKit/skills/`. Global agent paths contain symlinks pointing to that folder. Symlinks are installed once; editing one canonical SKILL.md updates all agents without copying. Agents may require restart to re-index.

## Updating

Do not overwrite the central root with Finder dragging or `cp -R` over it. Use:

```
python3 ~/GameAgentKit/gamekit.py upgrade --from /path/to/new/extracted/GameAgentKit --dry-run
python3 ~/GameAgentKit/gamekit.py upgrade --from /path/to/new/extracted/GameAgentKit
python3 ~/GameAgentKit/gamekit.py link --agents all
```

All overwritten kit-owned files are copied under `~/GameAgentKit/.backups/<timestamp>/`. Custom skills with names not in the package are left alone. If you directly modify a bundled Skill, upgrade backs it up but replaces it with the new package's version.

## Safety

- The base installer uses Python standard library only, never calls npx/git/curl, and does not require network or credentials.
- It refuses to overwrite pre-existing skill directories or symlinks under agent global settings.
- The per-project `attach` command only adds `.game-agent-kit/` plus minimal new root instruction files; existing root instructions must be linked manually.
- `unlink` removes only symbolic links pointing to the canonical kit; it never deletes custom Agent files, copies, global configuration parents or game repositories.
- For a full kit removal, unlink it, then manually archive/remove `~/GameAgentKit` after checking for your own skills.
- The optional third-party sources in `THIRD_PARTY.md` are not installed or audited by this package; confirm their trust and license yourself.

## Compatibility

- Mac/Linux shell: Python 3.9+ recommended, Bash for `install.sh` and iOS preflight.
- macOS native Xcode builds need Xcode and simulators; the bundled static tests do not replace them.
- Windows can run `python gamekit.py install --copy ...` in a compatible Python environment; Windows native/link-path interoperability is not tested and platform-specific paths may differ. The supported and tested flow is Unix-like.
