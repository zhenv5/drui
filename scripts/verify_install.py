"""Read-only, per-Agent DRUI Skill installation inventory.

Filesystem verification does not prove that an Agent has loaded or executed a Skill.
Never execute or mutate a third-party Skill while reporting installation state.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

STATUSES_OK = frozenset({'OK'})


def _metadata(path: Path) -> dict[str, str]:
    """Read small YAML front matter without importing/executing Skill code."""
    if path.is_symlink() or not path.is_file():
        return {}
    try:
        with path.open('r', encoding='utf-8') as stream:
            header = stream.read(16384)
    except (OSError, UnicodeError):
        return {}
    if not header.startswith('---\n'):
        return {}
    match = re.search(r'^---\s*$', header[4:], re.MULTILINE)
    if not match:
        return {}
    front = header[4:4 + match.start()]
    result = {}
    for field in ('name', 'version', 'description'):
        item = re.search(rf'^{field}:\s*[\'\"]?([^\n\'\"]+)', front, re.MULTILINE)
        if item:
            result[field] = item.group(1).strip()
    return result


def _target_status(target: Path, source: Path, expected_name: str) -> tuple[str, str]:
    """Only an exact symlink to bundled source is counted as DRUI-installed."""
    if target.is_symlink():
        if not target.exists():
            return 'BROKEN', 'symlink target missing'
        try:
            if target.resolve(strict=True) != source.resolve(strict=True):
                return 'COLLISION', 'symlink points to another Skill; left untouched'
        except (OSError, RuntimeError):
            return 'BROKEN', 'symlink could not be resolved'
        metadata = _metadata(source / 'SKILL.md')
        if metadata.get('name') != expected_name:
            return 'INVALID', 'bundled SKILL.md missing or name mismatch'
        return 'OK', 'managed symlink and SKILL.md validated'
    if target.exists():
        return 'COLLISION', 'existing user-owned file/directory; never overwritten'
    return 'MISSING', 'no Skill installed at this path'


def _external_slot(slot_dir: Path, bundled_names: set[str]) -> list[dict]:
    """List other Skill names and declared versions; do not hash/execute them."""
    result = []
    try:
        items = sorted(slot_dir.iterdir(), key=lambda p: p.name) if slot_dir.is_dir() else []
    except OSError:
        return result
    for entry in items:
        if entry.name in bundled_names or not entry.is_dir():
            continue
        skill_md = entry / 'SKILL.md'
        if not skill_md.is_file():
            continue
        # Do not follow a linked SKILL.md or load any nested dependency code.
        meta = _metadata(skill_md)
        result.append({'name': entry.name, 'version': meta.get('version'),
                       'path': str(entry), 'origin': 'USER/EXTERNAL',
                       'note': 'not installed or versioned by DRUI'})
    return result


def inspect(root: Path, home: Path, agents: list[str], agent_paths: dict[str, list[str]],
            *, project: Path | None = None) -> dict:
    root = Path(root).expanduser().absolute()
    home = Path(home).expanduser().absolute()
    source_dir = root / 'skills'
    if not source_dir.is_dir():
        raise RuntimeError(f'DRUI Skill source directory missing: {source_dir}')
    version_path = root / 'VERSION'
    if not version_path.is_file():
        raise RuntimeError(f'DRUI VERSION file missing: {version_path}')
    kit_version = version_path.read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', kit_version):
        raise RuntimeError(f'Invalid GameAgentKit VERSION: {kit_version!r}')
    sources = sorted(p for p in source_dir.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())
    if not sources:
        raise RuntimeError('No bundled DRUI Skills found')
    names = {p.name for p in sources}
    result_agents = []
    total, installed = 0, 0
    for agent in agents:
        agent_rows = []
        external = []
        for rel in agent_paths[agent]:
            slot_dir = home / rel
            for src in sources:
                target = slot_dir / src.name
                status, reason = _target_status(target, src, src.name)
                agent_rows.append({'name': src.name, 'version': kit_version,
                                   'version_source': 'GameAgentKit bundle (not an independent Skill version)',
                                   'status': status, 'agent': agent, 'slot': rel,
                                   'path': str(target), 'source': str(src), 'detail': reason})
                total += 1
                if status in STATUSES_OK:
                    installed += 1
            external.extend([dict(item, slot=rel) for item in _external_slot(slot_dir, names)])
        result_agents.append({'agent': agent, 'installed': sum(r['status'] == 'OK' for r in agent_rows),
                              'expected': len(agent_rows), 'skills': agent_rows, 'external': external})
    cli_source = root / 'scripts' / 'drui'
    cli_path = home / '.local' / 'bin' / 'drui'
    if cli_path.is_symlink():
        cli_status = 'OK' if cli_path.exists() and cli_path.resolve() == cli_source.resolve() and os.access(cli_source, os.X_OK) else 'BROKEN/CONFLICT'
    elif cli_path.exists():
        cli_status = 'COLLISION'
    else:
        cli_status = 'MISSING'
    path_ok = (cli_path.parent in [Path(p).expanduser() for p in os.environ.get('PATH', '').split(os.pathsep)])
    warnings = []
    if project is not None:
        project = Path(project).expanduser().absolute()
        for agent in agents:
            for rel in agent_paths[agent]:
                folder = project / rel
                for source in sources:
                    local = folder / source.name
                    if local.exists() or local.is_symlink():
                        warnings.append(f'{agent}: project-local {source.name} at {local} may shadow global DRUI Skill; actual resolution unknown')
    if not path_ok:
        warnings.append('~/.local/bin is not on this process PATH; drui may be unavailable as a shell command')
    report = {'schema': 1, 'kit': 'GameAgentKit', 'version': kit_version, 'root': str(root),
              'summary': {'installed': installed, 'expected': total, 'complete': total > 0 and installed == total and cli_status == 'OK'},
              'cli': {'status': cli_status, 'path': str(cli_path), 'source': str(cli_source), 'on_path': path_ok},
              'agents': result_agents, 'warnings': warnings,
              'verification': 'Local filesystem/metadata only; Agent runtime loading and compatibility NOT TESTED'}
    return report


def render_compact(report: dict) -> None:
    """One-line, read-only install result. Details stay available via --verbose/--json."""
    summary = report['summary']
    failures = [
        f"{agent['agent']}/{skill['name']}:{skill['status']}"
        for agent in report['agents'] for skill in agent['skills']
        if skill['status'] != 'OK'
    ]
    if report['cli']['status'] != 'OK':
        failures.append(f"CLI:{report['cli']['status']}")
    warnings = report['warnings']
    status = 'PASS' if summary['complete'] else 'FAIL'
    print(
        f"DRUI v{report['version']} {status} | "
        f"{len(report['agents'])} agents | "
        f"{summary['installed']}/{summary['expected']} Skill links | "
        f"{len(failures)} errors, {len(warnings)} warnings | runtime untested"
    )
    if failures:
        shown = failures[:3]
        tail = f", +{len(failures) - len(shown)} more" if len(failures) > len(shown) else ""
        print("Failures: " + ", ".join(shown) + tail)
    if warnings:
        kinds = []
        if any('PATH' in message for message in warnings):
            kinds.append('PATH')
        if any('shadow' in message.lower() for message in warnings):
            kinds.append('project shadow')
        if not kinds:
            kinds.append('other')
        print("Warnings: " + ", ".join(kinds) + " (see --verbose)")


def render(report: dict) -> None:
    print(f"\nDRUI Skill verification — GameAgentKit v{report['version']}")
    print(f"Source: {report['root']}")
    for agent in report['agents']:
        print(f"\n[{agent['agent']}] {agent['installed']}/{agent['expected']} installed slots")
        for row in agent['skills']:
            print(f"  {row['status']:<9} {row['name']:<22} bundle v{row['version']}  {row['path']}")
            if row['status'] != 'OK':
                print(f"            {row['detail']}")
        if agent['external']:
            print('  User/third-party Skills (unmanaged by DRUI):')
            for ext in agent['external']:
                print(f"    {ext['name']}  version: {ext['version'] or 'unknown'}  {ext['path']}")
    cli = report['cli']
    print(f"\nCLI: {cli['status']}  {cli['path']}")
    print('Shell PATH: ' + ('~/.local/bin is available' if cli['on_path'] else '~/.local/bin not found on PATH'))
    count = report['summary']
    print(f"Result: {count['installed']}/{count['expected']} managed Skill slots OK" +
          (' (COMPLETE)' if count['complete'] else ' (INCOMPLETE; inspect messages above)'))
    for note in report['warnings']:
        print('WARNING: ' + note)
    print('Agent actual loading/execution: NOT TESTED by this command.')
    print('For third-party fingerprints: drui deps check | drui deps conflicts')
    if not count['complete']:
        print('Fix missing links with: python3 ~/GameAgentKit/gamekit.py link --agents codex,claude,antigravity,cursor')
