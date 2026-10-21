# Security and trust model

- **Treat every Skill as instructions for a capable coding agent.** Inspect `SKILL.md` and shell/Python scripts before installing or invoking them.
- The installer only creates the chosen central kit root and non-overwriting symlinks; it does not download or install optional third-party skills.
- `drui update --check` only fetches GitHub public Release metadata. `drui update --yes` is an explicitly approved action: it pins an owner/repository, verifies a matching Release SHA-256 and archive structure, and upgrades bundled files with backups.
- SHA-256 validates that the ZIP matches the checksum published by the **same repository**; it **does not** prove the maintainer's identity or protect against a compromised upstream release account. Check repository ownership, release notes and code changes before upgrading.
- Users' external `oil-ui`, project files and local custom skills must not be overwritten by release upgrades. If there is a name collision, installation skips it.
- Report suspected vulnerabilities via a private GitHub security advisory if enabled, rather than disclosing exploit details publicly.
