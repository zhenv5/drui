"""Conservative GitHub Release updater for GameAgentKit.

- GitHub public releases only, explicit repository pinning.
- Versioned zip and SHA-256 are downloaded from the same release.
- Validate every ZIP entry before extraction (including symlink/type checks).
- Delegate mutations to existing backup-preserving `cmd_upgrade`.
- Never install arbitrary GitHub Actions, execute released scripts, or delete custom skills.

The checksum detects corruption; it does not defend against compromise of the
upstream GitHub account or release artifacts. Review publisher and source.
"""
from __future__ import annotations

import hashlib
import json
import re
import stat
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from types import SimpleNamespace

REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
MAX_ARCHIVE_BYTES = 25 * 1024 * 1024
MAX_UNPACKED_BYTES = 40 * 1024 * 1024
MAX_ZIP_FILES = 500
USER_AGENT = "GameAgentKit/1.6 (+https://github.com)"


def normalize_repo(raw: str) -> str:
    if not REPO_RE.fullmatch(raw or "") or ".." in raw:
        raise RuntimeError("Repository must be a GitHub owner/repo, e.g. alice/game-agent-kit")
    return raw


def release_asset_name(tag: str) -> str:
    if not TAG_RE.fullmatch(tag):
        raise RuntimeError(f"Invalid release tag: {tag!r} (expected vMAJOR.MINOR.PATCH)")
    return f"GameAgentKit-{tag}.zip"


def semver(tag: str) -> tuple[int, int, int]:
    m = TAG_RE.fullmatch(tag)
    if not m:
        raise RuntimeError(f"Invalid version: {tag}")
    return tuple(map(int, m.groups()))


def _request(url: str, *, limit: int) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in {"api.github.com", "github.com"}:
        raise RuntimeError(f"Refusing non-GitHub HTTPS source: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            if response.status != 200:
                raise RuntimeError(f"GitHub HTTP {response.status} at {url}")
            data = response.read(limit + 1)
    except (urllib.error.URLError, TimeoutError) as ex:
        raise RuntimeError(f"GitHub download failed: {ex}") from ex
    if len(data) > limit:
        raise RuntimeError("Release metadata or asset exceeds safe size limit")
    return data


def _json(url: str) -> dict:
    obj = json.loads(_request(url, limit=2 * 1024 * 1024))
    if not isinstance(obj, dict):
        raise RuntimeError("Invalid GitHub release metadata")
    return obj


def _asset_url(release: dict, name: str) -> str:
    for asset in release.get("assets", []):
        if asset.get("name") == name:
            uri = asset.get("browser_download_url", "")
            parsed = urllib.parse.urlparse(uri)
            if parsed.scheme != "https" or parsed.hostname != "github.com":
                raise RuntimeError("Unexpected GitHub release asset URL")
            return uri
    raise RuntimeError(f"Required release asset missing: {name}")


def validate_zip(data: bytes, tag: str, temp_dir: Path) -> Path:
    """Refuse traversal, absolute paths, symlinks, bombs, unexpected root."""
    from io import BytesIO
    root = temp_dir / "GameAgentKit"
    with zipfile.ZipFile(BytesIO(data)) as z:
        files = z.infolist()
        if not files or len(files) > MAX_ZIP_FILES:
            raise RuntimeError("Invalid or oversized ZIP file list")
        seen = set()
        total = 0
        for item in files:
            name = item.filename
            parts = name.rstrip("/").split("/")
            if ("\\" in name or name.startswith("/") or
                any(x in ("", ".", "..") for x in parts) or parts[0] != "GameAgentKit"):
                raise RuntimeError(f"Unsafe ZIP path: {name!r}")
            if name in seen:
                raise RuntimeError("Duplicate ZIP entry")
            seen.add(name)
            kind = stat.S_IFMT((item.external_attr >> 16) & 0o170000)
            if kind not in (0, stat.S_IFDIR, stat.S_IFREG):
                raise RuntimeError(f"Unsupported ZIP entry (symlink/device): {name}")
            total += item.file_size
            if total > MAX_UNPACKED_BYTES:
                raise RuntimeError("ZIP exceeds safe unpacked size limit")
        z.extractall(temp_dir)
    if not (root / "gamekit.py").is_file() or not (root / "scripts" / "drui").is_file():
        raise RuntimeError("Release archive does not contain GameAgentKit")
    installed = (root / "VERSION").read_text(encoding="utf-8").strip()
    if installed != tag[1:]:
        raise RuntimeError("Release tag and packaged VERSION mismatch")
    return root


def source_config_path(root: Path) -> Path:
    return root / ".gamekit-updates.json"


def save_repo(root: Path, repo: str) -> None:
    p = source_config_path(root)
    if p.is_symlink():
        raise RuntimeError("Refusing symlinked update config")
    if p.exists():
        stored = json.loads(p.read_text(encoding="utf-8"))
        old = stored.get("repository")
        if old != repo:
            raise RuntimeError(f"Update source already pinned to {old}; refusing automatic switch to {repo}")
        return
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps({"repository": repo}, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


def configured_repo(root: Path) -> str | None:
    p = source_config_path(root)
    if not p.exists():
        return None
    if p.is_symlink():
        raise RuntimeError("Refusing symlinked update config")
    return normalize_repo(json.loads(p.read_text(encoding="utf-8"))["repository"])


def update(*, root: Path, repo: str | None = None, check: bool = False,
           dry_run: bool = False, yes: bool = False, upgrade_callback=None) -> str:
    if not (root / "gamekit.py").is_file() or not (root / "VERSION").is_file():
        raise RuntimeError(f"Not a GameAgentKit installation: {root}")
    pinned = configured_repo(root)
    if pinned and repo and normalize_repo(repo) != pinned:
        raise RuntimeError(f"Already pinned to {pinned}; refusing change to {repo}")
    repo = normalize_repo(repo or pinned or "")
    current = "v" + (root / "VERSION").read_text(encoding="utf-8").strip()
    obj = _json(f"https://api.github.com/repos/{repo}/releases/latest")
    tag = obj.get("tag_name", "")
    latest = semver(tag)
    local = semver(current)
    print(f"GitHub: {repo} | installed: {current} | latest stable: {tag}")
    if latest <= local:
        print("Already up to date; nothing to change.")
        if not dry_run and not check and not pinned:
            save_repo(root, repo)
        return "current"
    release_asset_name(tag)
    asset = f"GameAgentKit-{tag}.zip"
    url = _asset_url(obj, asset)
    sum_url = _asset_url(obj, asset + ".sha256")
    print(f"Available: {tag} (verified release ZIP + SHA-256 required)")
    if check or dry_run:
        print("Check/preview mode: no download or modifications.")
        return "available"
    if not yes:
        raise RuntimeError("Upgrade not started. Rerun with --yes after reviewing the source and publisher.")
    checksum = _request(sum_url, limit=8192).decode("utf-8")
    line = checksum.strip().splitlines()
    if len(line) != 1:
        raise RuntimeError("Invalid checksum asset format")
    parts = line[0].split()
    if len(parts) != 2 or parts[1].lstrip("*") != asset or not re.fullmatch(r"[a-fA-F0-9]{64}", parts[0]):
        raise RuntimeError("Checksum filename or hash mismatch")
    data = _request(url, limit=MAX_ARCHIVE_BYTES)
    digest = hashlib.sha256(data).hexdigest()
    if digest.lower() != parts[0].lower():
        raise RuntimeError("SHA-256 verification failed; refusing upgrade")
    with tempfile.TemporaryDirectory(prefix="gamekit-release-") as tmp:
        source = validate_zip(data, tag, Path(tmp))
        if upgrade_callback is None:
            raise RuntimeError("Missing safe upgrade callback")
        upgrade_callback(SimpleNamespace(root=str(root), source=str(source), dry_run=False))
    save_repo(root, repo)
    print("Update installed. Run `python3 ~/GameAgentKit/gamekit.py link --agents all` if links were missing.")
    return "updated"
