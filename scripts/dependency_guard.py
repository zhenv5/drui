"""Local read-only fingerprints for optional, third-party Agent Skills.

Never updates, executes or copies external Skills. Locks record content approval
snapshots; hashes are NOT a sandbox, license check or proof of behavioral safety.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = 1
OMIT = frozenset({'.git', '.venv', '__pycache__', 'node_modules', '.DS_Store', '.pytest_cache', 'dist', 'build'})


def lock_path(root):
    return root / '.state' / 'external-skills.lock.json'


def digest_skill(directory):
    """Hash filenames + bytes, sorted; don't follow nested symlinks outside tree."""
    directory = Path(directory).resolve()
    h = hashlib.sha256()
    count, total = 0, 0
    for base, dirs, files in os.walk(directory, followlinks=False):
        for d in dirs:
            if d not in OMIT and (Path(base) / d).is_symlink():
                raise RuntimeError(f'External Skill contains linked directory; manual review required: {Path(base) / d}')
        dirs[:] = sorted(d for d in dirs if d not in OMIT)
        for name in sorted(files):
            if name in OMIT:
                continue
            file = Path(base) / name
            if file.is_symlink():
                raise RuntimeError(f'External Skill contains linked file; manual review required: {file}')
            if not file.is_file():
                continue
            rel = file.relative_to(directory).as_posix()
            h.update(rel.encode('utf-8') + b'\0')
            with file.open('rb') as f:
                while True:
                    block = f.read(1024*1024)
                    if not block:
                        break
                    h.update(block)
                    total += len(block)
                    if total > 300 * 1024 * 1024:
                        raise RuntimeError(f'External Skill too large to fingerprint safely: {directory}')
            count += 1
    if not count or not (directory / 'SKILL.md').is_file():
        raise RuntimeError(f'Not a valid external Skill: {directory}')
    return h.hexdigest()


def scan_skills(root, home, agents, paths, *, project=None):
    """Discover exact installed slots, including same-name user copies and project overrides.

    Only exact symlinks to the kit's source are considered managed. A copy, even
    if its hash currently matches, is user-owned because later edits/upgrades
    will not be managed by the kit. Nothing is executed or modified.
    """
    root = Path(root).resolve()
    home = Path(home)
    result = {}
    for agent in agents:
        dirs = [(home / rel, f'home:{rel}') for rel in paths[agent]]
        if project is not None:
            # Discovery varies by agent and version. These locations are
            # advisory; actual loading must be verified in the target agent.
            dirs += [(Path(project).resolve() / rel, f'project:{Path(project).resolve()}:{rel}')
                     for rel in paths[agent]]
        for directory, slot in dirs:
            if not directory.is_dir():
                continue
            for item in sorted(directory.iterdir()):
                if not item.is_dir() or not (item / 'SKILL.md').is_file():
                    continue
                name = item.name
                owned = root / 'skills' / name
                managed = item.is_symlink() and owned.is_dir() and item.resolve() == owned.resolve()
                source = item.resolve()
                key = f'{agent}|{slot}|{name}'
                entry = {'agent': agent, 'slot': slot, 'name': name,
                         'source': str(source), 'managed': managed,
                         'owner': 'GAMEAGENTKIT' if managed else 'USER',
                         'same_name_collision': owned.is_dir() and not managed}
                if not managed:
                    entry['sha256'] = digest_skill(source)
                result[key] = entry
    return result


def enumerate_external(root, home, agents, paths, *, project=None):
    """Return ALL unmanaged Skills, including user installs shadowing kit names."""
    return {key: info for key, info in
            scan_skills(root, home, agents, paths, project=project).items()
            if not info['managed']}


def read_lock(root):
    path = lock_path(root)
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f'Unsafe dependency lock: {path}')
    doc = json.loads(path.read_text(encoding='utf-8'))
    if doc.get('schema') != SCHEMA or not isinstance(doc.get('approved'), dict):
        raise RuntimeError(f'Unsupported external dependency lock format: {path}')
    return doc


def save_lock(root, doc, *, backup=True):
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise RuntimeError(f'Refusing symlink dependency lock: {path}')
    if path.exists() and backup:
        folder = root / '.state' / 'backups'
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, folder / f'external-skills-{stamp}.json')
    temp = path.with_name(path.name + '.tmp')
    if temp.exists() or temp.is_symlink():
        raise RuntimeError(f'Temporary lock exists: {temp}')
    try:
        temp.write_text(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def compare(current, baseline):
    if baseline is None:
        return {'UNLOCKED': list(current)}
    approved = baseline['approved']
    status = {}
    for key, entry in current.items():
        old = approved.get(key)
        if old is None:
            status[key] = 'NEW'
        elif old.get('source') != entry['source'] or old.get('sha256') != entry['sha256']:
            status[key] = 'CHANGED'
        else:
            status[key] = 'OK'
    for key in approved:
        if key not in current:
            status[key] = 'MISSING'
    return status


def is_approved_source(root, name, path, *, agent='all', agent_paths=None):
    """If a lock exists, fail closed for modified/new external sources.

    With no lock preserve backwards compatibility but DO NOT imply verified.
    """
    doc = read_lock(root)
    if doc is None:
        return True, 'UNLOCKED; run drui deps lock'
    p = str(Path(path).resolve().parent)
    for key, item in doc['approved'].items():
        if item.get('name') != name or item.get('source') != p:
            continue
        if agent != 'all' and not key.startswith(agent + '|'):
            continue
        try:
            if digest_skill(Path(p)) == item.get('sha256'):
                return True, 'APPROVED'
        except (OSError, RuntimeError):
            pass
    return False, 'CHANGED or UNAPPROVED external Skill; run drui deps check'


def fresh_doc(entries):
    return {'schema': SCHEMA, 'updated_at': datetime.now(timezone.utc).isoformat(),
            'approved': entries}
