#!/usr/bin/env python3
"""Produce version-matched, inspectable GitHub Release ZIP + SHA-256.

No third-party packaging dependencies. Zip contains one GameAgentKit/ root.
"""
from __future__ import annotations

import hashlib
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".git", ".github", "__pycache__", ".pytest_cache", ".venv", "dist", ".backups", ".state"}
EXCLUDE_FILES = {".DS_Store", ".gamekit-updates.json", ".coverage"}


def create_release(destination: Path | None = None) -> tuple[Path, Path]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or any(not x.isdecimal() for x in version.split(".")) or len(version.split(".")) != 3:
        raise SystemExit("VERSION must be x.y.z")
    tag = "v" + version
    if os.environ.get("GITHUB_REF_TYPE") == "tag" and os.environ.get("GITHUB_REF_NAME") != tag:
        raise SystemExit(f"Git tag {os.environ['GITHUB_REF_NAME']} != VERSION {tag}")
    code = (ROOT / "gamekit.py").read_text(encoding="utf-8")
    if f'VERSION = "{version}"' not in code:
        raise SystemExit("gamekit.py VERSION disagrees with VERSION file")
    dest = destination or (ROOT / "dist")
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / f"GameAgentKit-{tag}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for file in sorted(ROOT.rglob("*")):
            if not file.is_file() or file.is_symlink():
                continue
            rel = file.relative_to(ROOT)
            if any(part in EXCLUDE_DIRS for part in rel.parts) or file.name in EXCLUDE_FILES or file.suffix in {".pyc", ".pyo"}:
                continue
            # Explicitly give ZIP entries simple, portable filenames.
            z.write(file, arcname=str(Path("GameAgentKit") / rel))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    sha = archive.with_suffix(archive.suffix + ".sha256")
    sha.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    print(f"Created {archive.name} ({archive.stat().st_size} bytes)")
    print(f"Checksum {digest}")
    return archive, sha


if __name__ == "__main__":
    out = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else None
    create_release(out)
