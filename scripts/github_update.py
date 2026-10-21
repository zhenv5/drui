"""GitHub source-only updater for DRUI.

The canonical ~/GameAgentKit installation is a git clone of the official
repository, checked out at an immutable public GitHub Release tag. No ZIP,
installer download, archive extraction, or third-party Skill mutation occurs.
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OFFICIAL_REPO = 'zhenv5/drui'
OFFICIAL_REMOTES = frozenset({
    'https://github.com/zhenv5/drui.git',
    'https://github.com/zhenv5/drui',
    'git@github.com:zhenv5/drui.git',
    'git@github.com:zhenv5/drui',
})
TAG_RE = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
USER_AGENT = 'DRUI/GitSource (+https://github.com/zhenv5/drui)'


def normalize_repo(raw: str) -> str:
    if raw != OFFICIAL_REPO:
        raise RuntimeError(f'Only the official GitHub repository {OFFICIAL_REPO} is supported')
    return raw


def semver(tag: str) -> tuple[int, int, int]:
    match = TAG_RE.fullmatch(tag)
    if not match:
        raise RuntimeError(f'Invalid stable DRUI version tag: {tag!r}')
    return tuple(int(v) for v in match.groups())


def _run(root: Path, *args: str, check: bool = True) -> str:
    try:
        proc = subprocess.run(['git', '-C', str(root), *args], text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=75, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as ex:
        raise RuntimeError(f'Git command unavailable or timed out: {ex}') from ex
    if check and proc.returncode:
        raise RuntimeError(f'Git {args[0]} failed: {proc.stderr.strip() or proc.stdout.strip()}')
    return proc.stdout.strip()


def _verify_root(root: Path) -> None:
    if root.is_symlink() or not root.is_dir() or not (root / 'VERSION').is_file():
        raise RuntimeError('Expected a DRUI Git checkout at ~/GameAgentKit')
    if _run(root, 'rev-parse', '--is-inside-work-tree') != 'true':
        raise RuntimeError('The DRUI directory is not a Git checkout')
    if Path(_run(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
        raise RuntimeError('DRUI must be the root of its own Git checkout')
    origin = _run(root, 'remote', 'get-url', 'origin')
    if origin not in OFFICIAL_REMOTES:
        raise RuntimeError(f'Untrusted Git origin {origin!r}; expected {OFFICIAL_REPO}')
    # Reject hostile user-defined repository-local hooks / redirects on this entrypoint.
    if _run(root, 'config', '--local', '--get', 'core.hooksPath', check=False):
        raise RuntimeError('Custom repository hooksPath configured; review manually')


def configured_repo(root: Path) -> str | None:
    try:
        _verify_root(root)
        return OFFICIAL_REPO
    except RuntimeError:
        return None


def _latest_tag() -> str:
    url = f'https://api.github.com/repos/{OFFICIAL_REPO}/releases/latest'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/vnd.github+json'})
    # No third-party host redirects, even when the original URL was GitHub.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise RuntimeError(f'Unexpected release metadata redirect: {newurl}')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=15) as response:
            if response.geturl() != url or response.status != 200:
                raise RuntimeError('Unexpected GitHub release metadata response')
            data = response.read(131073)
    except (urllib.error.URLError, TimeoutError) as ex:
        raise RuntimeError(f'Unable to check GitHub release: {ex}') from ex
    if len(data) > 131072:
        raise RuntimeError('Oversized GitHub metadata response')
    obj = json.loads(data)
    if not isinstance(obj, dict) or obj.get('draft') or obj.get('prerelease'):
        raise RuntimeError('GitHub did not return a stable release')
    tag = obj.get('tag_name')
    semver(tag)
    return tag


def update(*, root: Path, repo: str | None = None, check: bool = False,
           dry_run: bool = False, yes: bool = False, upgrade_callback=None) -> str:
    """Check GitHub Release, then fetch + checkout its tagged *source* with Git.

    upgrade_callback is ignored; it is accepted only for the existing core
    caller. No extraction, file copying, hooks, external Skill modification.
    """
    root = Path(root).expanduser().absolute()
    if repo is not None:
        normalize_repo(repo)
    _verify_root(root)
    if yes and _run(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise RuntimeError('Git checkout has local changes or untracked files; refusing update')
    installed = (root / 'VERSION').read_text(encoding='utf-8').strip()
    current = 'v' + installed
    semver(current)
    latest = _latest_tag()
    print(f'GitHub source: {OFFICIAL_REPO} | installed: {current} | latest stable tag: {latest}')
    if semver(latest) <= semver(current):
        print('Already up to date.')
        return 'current'
    print(f'Available: {latest} (GitHub tagged source; no release ZIP)')
    if check or dry_run:
        print('Check only: no local Git refs or files modified.')
        return 'available'
    if not yes:
        raise RuntimeError('Upgrade not started: inspect changes and rerun with --yes')
    # Never overwrite a user-edited checkout. Local-only state stays .gitignored.
    previous_sha = _run(root, 'rev-parse', 'HEAD')
    # Named tag ref, not branch: protect from mutable main changes.
    _run(root, '-c', 'protocol.file.allow=never', 'fetch', '--no-tags', '--depth=1',
         'origin', f'refs/tags/{latest}:refs/tags/{latest}')
    tag_sha = _run(root, 'rev-parse', f'refs/tags/{latest}^{{commit}}')
    found_version = _run(root, 'show', f'{tag_sha}:VERSION')
    if found_version != latest[1:]:
        raise RuntimeError('Remote tag and VERSION file disagree; no changes applied')
    if not _run(root, 'show', f'{tag_sha}:scripts/drui').startswith('#!/usr/bin/env python3'):
        raise RuntimeError('Git release tag missing DRUI CLI')
    # Clean checkout, stable tag, no shell hooks. Git controls managed source files.
    _run(root, '-c', 'core.hooksPath=/dev/null', 'checkout', '--detach', tag_sha)
    print(f'Updated {previous_sha[:12]} -> {tag_sha[:12]} ({latest})')
    print('Installed Skill symlinks still point to ~/GameAgentKit/skills. Run drui deps check and doctor.')
    return 'updated'
