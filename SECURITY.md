# Security and trust model

DRUI **only** installs and updates via the official GitHub Git source repository: https://github.com/zhenv5/drui . Current releases are source-only. The auto-generated “Source code (zip)” link is **not** a supported DRUI installer. No Release ZIP/SHA-256 installer is used.

- **Review first:** Agent Skills are instructions that can be executed by capable coding agents. Review bundled `SKILL.md`, `install.sh`, `gamekit.py` and the release diff before running them.
- **Install:** Clone a reviewed stable GitHub Release Tag into an unused `~/GameAgentKit`. The installer creates only missing Skill/CLI symlinks and never overwrites a same-name user-owned Skill. Because an intentional name collision may leave `install.sh` exiting 0, sign-off requires a successful, nonzero-failure-aware `drui verify` run.
- **Update:** `drui update --check` reads official latest-stable Release metadata without mutating local checkout; `--yes` needs explicit approval, checks official Git origin and clean working tree, fetches the stable Tag and validates its VERSION / bundled CLI before Git checkout.
- **Source integrity vs. publisher trust:** Git hashes identify Git objects, **not publisher identity**, protection against a compromised GitHub repository, or administrator-controlled Tag mutation. Do not claim cryptographic publisher attestation or signed release provenance where no such mechanism exists.
- **Crash handling:** Git checkout is not crash-atomic. After interruption preserve logs and inspect `git status` and current version; never force-reset or clean away unreviewed user changes.
- **External Skills:** User-owned Skills and projects are not automatically downloaded, overwritten, approved or upgraded. Conflicting names are preserved. Fingerprints detect file changes, not their safety.
- **Verification:** `drui verify` audits local links, metadata and CLI paths; it cannot prove that Codex, Claude Code, Antigravity or Cursor actually loaded or ran them.

See the [installation and verification guide](docs/INSTALL_AND_VERIFY.md). Privately report security issues with GitHub security advisories when enabled.
