#!/usr/bin/env python3
"""GameAgentKit CLI. Standard-library only, safe by default."""
from __future__ import annotations

import argparse
import json
import re
import stat
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from scripts import dependency_guard as depguard

VERSION = "1.4.2"
HERE = Path(__file__).resolve().parent
AGENT_PATHS = {
    "codex": [".agents/skills"],
    "claude": [".claude/skills"],
    "antigravity": [".gemini/config/skills", ".gemini/antigravity-cli/skills"],
    "cursor": [".cursor/skills"],
}
ALIASES = {"claude-code": "claude", "agy": "antigravity", "all": "codex,claude,antigravity"}
PROFILES = ["ios-swiftui", "web-game", "puzzle", "arcade", "3d-game", "generic"]
START = "<!-- GameAgentKit: begin (managed) -->"
END = "<!-- GameAgentKit: end (managed) -->"


def fail(message):
    raise RuntimeError(message)


def args_agents(raw):
    if raw == "all":
        raw = ALIASES["all"]
    result = []
    for token in raw.split(","):
        agent = ALIASES.get(token.strip(), token.strip())
        if agent not in AGENT_PATHS:
            fail(f"Unknown agent '{agent}'. Choose: {', '.join(AGENT_PATHS)}, all")
        if agent not in result:
            result.append(agent)
    if not result:
        fail("No agents selected")
    return result


def ensure_link(dest: Path, source: Path, *, dry_run=False, copy=False, verbose=True):
    """Only create a new link; do not replace an existing file/directory/symlink."""
    if dest.is_symlink():
        if dest.resolve() == source.resolve():
            return "ok"
        if verbose:
            print(f"  SKIP different existing link: {dest}")
        return "collision"
    if dest.exists():
        if verbose:
            print(f"  SKIP existing content: {dest}")
        return "collision"
    if verbose:
        print(f"  {'WOULD ' if dry_run else ''}{'COPY' if copy else 'LINK'} {dest} -> {source}")
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if copy:
            shutil.copytree(source, dest)
        else:
            dest.symlink_to(source, target_is_directory=True)
    return "created"


def core_skills(root):
    skills = root / "skills"
    if not skills.is_dir():
        fail(f"Missing skills folder: {skills}")
    result = []
    for item in sorted(skills.iterdir()):
        if item.is_dir() and (item / "SKILL.md").is_file():
            result.append(item)
    if not result:
        fail("No valid skills found")
    return result


def copy_bundle(src: Path, dest: Path, *, dry_run=False):
    if src == dest:
        print("Root already contains the kit. Skipping copy.")
        return
    if dest.exists():
        fail(f"Install root already exists: {dest}. To upgrade, run 'upgrade --from ...' instead.")
    if dest == src or src in dest.parents:
        fail("Install destination must not be inside the extracted kit")
    print(f"{'WOULD INSTALL' if dry_run else 'INSTALL'} {src} -> {dest}")
    if not dry_run:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", ".pytest_cache", ".git", ".venv", "dist"))


def provision(root, agents, *, dry_run=False, copy=False, home=None, link_root=None):
    home = home or Path.home()
    link_root = link_root or root
    installed, collisions = 0, 0
    for agent in agents:
        for rel in AGENT_PATHS[agent]:
            dest_root = home / rel
            print(f"[{agent}] {dest_root}")
            for skill in core_skills(root):
                status = ensure_link(dest_root / skill.name, link_root / "skills" / skill.name, dry_run=dry_run, copy=copy)
                if status == "created":
                    installed += 1
                if status == "collision":
                    collisions += 1
    print(f"Skill entries: {installed} {'planned' if dry_run else 'created'}; {collisions} conflicts left untouched.")
    return collisions


DRUI_UI_SOURCE_ORDER = ("pro", "plus", "oil-ui", "drui")
DRUI_UI_SKILLS = {"pro": "oil-ui-pro", "plus": "oil-ui-plus", "oil-ui": "oil-ui", "drui": "drui"}
DRUI_UI_SOURCE_CHOICES = ("auto",) + DRUI_UI_SOURCE_ORDER


def discover_ui_sources(root: Path, *, home=None, agent="all"):
    """Find accessible SKILL.md files without fetching or running third-party code.

    A source located under ONE agent directory may not be available to another;
    use --agent to narrow CLI checks and always recheck from inside the agent.
    """
    home = home or Path.home()
    locations = {}
    agents = args_agents(agent)
    for choice, name in DRUI_UI_SKILLS.items():
        found = []
        if choice in ("plus", "drui"):
            bundled = root / "skills" / name / "SKILL.md"
            if bundled.is_file():
                found.append(bundled)
        for agent_name in agents:
            for rel in AGENT_PATHS[agent_name]:
                installed = home / rel / name / "SKILL.md"
                if installed.is_file():
                    found.append(installed)
        locations[choice] = list(dict.fromkeys(map(str, found)))
    return locations


def select_ui_source(root: Path, requested="auto", *, home=None, agent="all", project=None):
    if requested not in DRUI_UI_SOURCE_CHOICES:
        fail(f"Unknown UI source {requested}; choose {', '.join(DRUI_UI_SOURCE_CHOICES)}")
    home = home or Path.home()
    available = discover_ui_sources(root, home=home, agent=agent)
    slots = depguard.scan_skills(root, home, args_agents(agent), AGENT_PATHS, project=project)
    # If user installed a same-name skill under an Agent or project, a bundled
    # candidate cannot be considered reliably loaded. Do not silently select
    # the bundled copy and claim the agent will execute it.
    shadows = {v['name'] for v in slots.values() if v['same_name_collision']}

    def trusted(choice, path):
        if choice in ('plus', 'drui') and DRUI_UI_SKILLS[choice] in shadows:
            return False
        if choice in ('pro', 'oil-ui'):
            # This hash guard only applies to external versions. Even if
            # unpinned initially, report the UNLOCKED state separately.
            return depguard.is_approved_source(root, DRUI_UI_SKILLS[choice], path, agent=agent)[0]
        return True

    if requested == "auto":
        for choice in DRUI_UI_SOURCE_ORDER:
            for path in available[choice]:
                if trusted(choice, path):
                    return choice, path, available
        fail("No unambiguous, approved UI method source. Run `drui deps conflicts` and resolve duplicate names; no fallback was assumed.")
    if not available[requested]:
        fail(f"Requested UI source '{requested}' ({DRUI_UI_SKILLS[requested]}) is not installed for agent '{agent}'. No fallback was performed.")
    safe = [path for path in available[requested] if trusted(requested, path)]
    if not safe:
        fail(f"Requested UI source '{requested}' cannot be verified: CHANGED/UNAPPROVED external Skill or same-name user copy. "
             "Run `drui deps check` and `drui deps conflicts`, then review and resolve. No fallback performed.")
    return requested, safe[0], available


def show_ui_sources(root: Path, *, agent="all", home=None):
    selected, path, available = select_ui_source(root, "auto", home=home, agent=agent)
    print("DRUI UI source priority: oil-ui-pro > oil-ui-plus > oil-ui > drui")
    print(f"Scope: {agent}; selected automatically: {DRUI_UI_SKILLS[selected]}")
    for source in DRUI_UI_SOURCE_ORDER:
        paths = available[source]
        print(f"  {DRUI_UI_SKILLS[source]:13} {'AVAILABLE' if paths else 'NOT AVAILABLE'}" + (f"  {paths[0]}" if paths else ""))
    lock = depguard.read_lock(root)
    print("External Skill fingerprint lock: " + ("ACTIVE (changed external sources excluded from auto selection)" if lock else "NOT CREATED; run `drui deps lock`"))
    for source in ('pro', 'oil-ui'):
        for p in available[source]:
            approved, reason = depguard.is_approved_source(root, DRUI_UI_SKILLS[source], p, agent=agent)
            print(f"  {DRUI_UI_SKILLS[source]}: {'APPROVED' if approved and lock else reason}")
    print("Note: fingerprints detect file changes, not semantic/API compatibility or independent Agent execution.")


def cmd_ui_sources(args):
    show_ui_sources(Path(args.root).expanduser().resolve(), agent=args.agent)


DRUI_CLI = "drui"


def ensure_drui_executable(root: Path, *, dry_run=False):
    """A GitHub Release ZIP extracted by Python may lose UNIX executable bits.

    Only change the toolkit-owned command under its canonical root; this never
    chmods a user-installed `drui` file or foreign Agent Skill.
    """
    source = root / "scripts" / DRUI_CLI
    if dry_run:
        return
    if source.is_symlink() or not source.is_file():
        fail(f"Missing or unsafe bundled DRUI command: {source}")
    mode = source.stat().st_mode
    if not mode & stat.S_IXUSR:
        source.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def link_drui_cli(root: Path, *, dry_run=False, home=None):
    """Safely share the local command via ~/.local/bin without changing shell dotfiles.

    The command is a symlink to the canonical kit's `bin/drui`. Never overwrite
    any existing file, symlink or executable named drui, even if it is broken.
    """
    home = home or Path.home()
    source = root / "scripts" / DRUI_CLI
    if not dry_run and not source.is_file():
        fail(f"Missing DRUI CLI: {source}. Upgrade/install GameAgentKit first.")
    ensure_drui_executable(root, dry_run=dry_run)
    target = home / ".local" / "bin" / DRUI_CLI
    print("[DRUI CLI] ~/.local/bin/drui")
    status = ensure_link(target, source, dry_run=dry_run)
    if status == "collision":
        print("  Existing drui command preserved. Run the kit's bin/drui directly if needed.")
    return status


def unlink_drui_cli(root: Path, *, dry_run=False, home=None):
    home = home or Path.home()
    target = home / ".local" / "bin" / DRUI_CLI
    source = root / "scripts" / DRUI_CLI
    if target.is_symlink() and target.resolve() == source.resolve():
        print(f"  {'WOULD ' if dry_run else ''}REMOVE owned CLI link {target}")
        if not dry_run:
            target.unlink()
        return True
    if target.exists() or target.is_symlink():
        print(f"  KEEP preexisting/unowned CLI {target}")
    return False


def installation_report(root, agents, *, home=None, project=None, json_format=False, compact=False):
    """Read-only audit of exact bundled Skill symlinks for selected agents."""
    from scripts.verify_install import inspect, render, render_compact
    report = inspect(root, home or Path.home(), agents, AGENT_PATHS, project=project)
    if json_format:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif compact:
        render_compact(report)
    else:
        render(report)
    return report


def cmd_verify(args):
    root = Path(args.root).expanduser().resolve()
    report = installation_report(root, args_agents(args.agents), project=args.project,
                                 json_format=args.json, compact=args.compact)
    if not report['summary']['complete']:
        fail('Installation verification incomplete; inspect missing/conflicting Skill paths (no changes made)')


def cmd_install(args):
    src = HERE
    root = Path(args.root).expanduser().resolve()
    if root == Path.home().resolve():
        fail("Refusing to install directly into home directory")
    copy_bundle(src, root, dry_run=args.dry_run)
    # If dry-run, canonical files do not exist yet; use source to inspect skill names.
    provision(src if args.dry_run else root, args_agents(args.agents), dry_run=args.dry_run, copy=args.copy, link_root=root)
    link_drui_cli(root, dry_run=args.dry_run)
    # If installed from a public GitHub clone, pin the source for `drui update`.
    # No network request and no repository change; skip ZIP/local distributions.
    if not args.dry_run:
        from scripts.github_update import configured_repo
        if configured_repo(root):
            print("Update source verified: GitHub official origin (zhenv5/drui)")
    if not args.dry_run:
        installation_report(root, args_agents(args.agents), compact=True)
    print("\nShared root:", root)
    print("New projects already see the GLOBAL skills. Optionally add per-project context:")
    print(f"  python3 {root}/gamekit.py attach --project /path/to/game --profile ios-swiftui --name 'My Game'")


def cmd_link(args):
    root = Path(args.root).expanduser().resolve()
    provision(root, args_agents(args.agents), dry_run=args.dry_run, copy=args.copy)
    link_drui_cli(root, dry_run=args.dry_run)
    if not args.dry_run:
        installation_report(root, args_agents(args.agents), compact=True)


def cmd_unlink(args):
    root = Path(args.root).expanduser().resolve()
    count = 0
    for agent in args_agents(args.agents):
        for rel in AGENT_PATHS[agent]:
            for skill in core_skills(root):
                target = Path.home() / rel / skill.name
                if target.is_symlink() and target.resolve() == skill.resolve():
                    print(f"  {'WOULD ' if args.dry_run else ''}REMOVE owned link {target}")
                    if not args.dry_run:
                        target.unlink()
                    count += 1
                elif target.exists() or target.is_symlink():
                    print(f"  KEEP unowned entry {target}")
    unlink_drui_cli(root, dry_run=args.dry_run)
    print(f"Removed/previewed {count} skill symlinks. Canonical root, copies and project docs preserved.")


def project_block():
    return f"{START}\nRead `.game-agent-kit/PROFILE.md` for this game's platform, design, constraints and QA expectations.\nUse `game-qa-review` for independent review. For UI tasks use `drui` and select UI guidance in priority order: official `oil-ui-pro` (only if installed) > original bundled `oil-ui-plus` > external `oil-ui` > DRUI fallback. Never fake Pro access.\nDo not report emulator/device validation unless actual screenshots and test logs exist.\n{END}\n"


def add_agent_entrypoint(path: Path, content: str, *, dry_run=False):
    if path.exists():
        current = path.read_text(encoding="utf-8", errors="replace")
        if START in current:
            print(f"  KEEP managed entry already present: {path}")
            return "present"
        print(f"  KEEP existing entrypoint untouched: {path}")
        print(f"    Add manually if desired:\n{content.strip()}\n")
        return "manual"
    print(f"  {'WOULD ' if dry_run else ''}CREATE {path}")
    if not dry_run:
        path.write_text("# Project instructions\n\n" + content, encoding="utf-8")
    return "created"


def check_project_safety(project: Path):
    if not project.is_dir():
        fail(f"Project directory not found: {project}")
    if project == Path.home().resolve():
        fail("Project must not be your entire home directory")


def cmd_attach(args):
    project = Path(args.project).expanduser().resolve()
    check_project_safety(project)
    name = args.name or project.name
    if "\n" in name or "\r" in name:
        fail("Project name must be one line")
    root = Path(args.root).expanduser().resolve()
    if not (root / "profiles" / f"{args.profile}.md").is_file():
        fail(f"Profile '{args.profile}' not found under root {root}")
    configdir = project / ".game-agent-kit"
    configfile = configdir / "config.json"
    profilefile = configdir / "PROFILE.md"
    if (configfile.exists() or profilefile.exists()) and not args.dry_run:
        fail(f"Project already attached: {configdir}. Edit its files manually; attach will not overwrite.")
    doc = (root / "profiles" / "common.md").read_text(encoding="utf-8")
    doc += "\n---\n\n" + (root / "profiles" / f"{args.profile}.md").read_text(encoding="utf-8")
    doc = f"# {name} — Game Agent Project Profile\n\nSelected profile: `{args.profile}`\n\n" + doc
    # Config is metadata only and portable between machines; never store machine-specific roots here.
    config = {"schema": 1, "project": name, "profile": args.profile, "kit": "GameAgentKit", "skills": "global"}
    print(f"Attach '{name}' ({args.profile}) at {project}")
    print(f"  {'WOULD ' if args.dry_run else ''}WRITE {configfile} and {profilefile}")
    if not args.dry_run:
        configdir.mkdir(parents=True, exist_ok=False)
        configfile.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        profilefile.write_text(doc, encoding="utf-8")
    for entry in ["AGENTS.md", "CLAUDE.md"]:
        add_agent_entrypoint(project / entry, project_block(), dry_run=args.dry_run)
    print("Project-specific instructions are a small optional attachment; skill source remains global.")


def report_skill_conflicts(root, agents, *, home=None, project=None):
    slots = depguard.scan_skills(root, home or Path.home(), agents, AGENT_PATHS,
                                project=project)
    collisions = {k: v for k, v in slots.items() if v['same_name_collision']}
    if collisions:
        print(f"WARNING: {len(collisions)} user-owned Skill(s) share names with bundled GameAgentKit Skills:")
        for key, info in sorted(collisions.items()):
            print(f"  COLLISION {key} -> {info['source']} (USER-owned; kit not overwriting)")
        print("Which duplicate loads depends on the Agent/project. Verify the actual loaded SKILL.md; ")
        print("use `drui deps conflicts` to inspect. GameAgentKit will NOT replace user-owned files.")
    return collisions


def cmd_doctor(args):
    root = Path(args.root).expanduser().resolve()
    print(f"GameAgentKit root: {root}")
    skills = core_skills(root)
    failures = 0
    for sk in skills:
        content = (sk / "SKILL.md").read_text(encoding="utf-8")
        valid = content.startswith("---\n") and re.search(r"\nname:\s*[^\n]+", content) and re.search(r"\ndescription:\s*[^\n]+", content)
        if not valid:
            print("FAIL malformed skill", sk)
            failures += 1
    print(f"Valid skill folders: {len(skills) - failures}/{len(skills)}")
    for agent in args_agents(args.agents):
        for rel in AGENT_PATHS[agent]:
            directory = Path.home() / rel
            missing = [sk.name for sk in skills if not (directory / sk.name / "SKILL.md").is_file()]
            print(f"{agent} {directory}: {len(skills) - len(missing)}/{len(skills)} discovered")
            if missing:
                print("  Missing:", ", ".join(missing))
                failures += 1
    command = Path.home() / ".local" / "bin" / "drui"
    source = root / "scripts" / "drui"
    if command.is_symlink() and command.resolve() == source.resolve():
        print("DRUI CLI: installed (~/.local/bin/drui). Confirm ~/.local/bin is in PATH.")
    else:
        print("DRUI CLI: NOT LINKED or occupied by another command. Run `link --agents all` or kit/scripts/drui.")
    # User-provided Oil UI is OPTIONAL; don't treat unavailable Pro access as a package failure.
    found_oil = []
    for agent in args_agents(args.agents):
        for rel in AGENT_PATHS[agent]:
            if ((Path.home() / rel / "oil-ui" / "SKILL.md").is_file()):
                found_oil.append(agent)
    print("Optional external oil-ui: " + (", ".join(dict.fromkeys(found_oil)) if found_oil else "NOT INSTALLED (drui still available)"))
    report_skill_conflicts(root, args_agents(args.agents), project=args.project)
    show_ui_sources(root, agent=args.agents)
    print("External dependencies: run `drui deps check` after any upstream Skill update.")
    if args.project:
        p = Path(args.project).expanduser().resolve()
        for suffix in [".game-agent-kit/config.json", ".game-agent-kit/PROFILE.md"]:
            if not (p / suffix).is_file():
                print(f"Project missing: {p / suffix}")
                failures += 1
    if failures:
        fail(f"Doctor found {failures} problems. Run `link` or `attach` if appropriate.")
    print("PASS static installation checks. Agent discovery and actual builds require testing on your machine.")


def cmd_upgrade(args):
    """Upgrade managed files with complete preflight, backup, and best-effort rollback.

    Interrupted processes / power loss can still leave partial state; a successful
    return requires all files updated. User-owned Skills outside bundled names
    are not enumerated from the local installation.
    """
    root = Path(args.root).expanduser().resolve()
    src = Path(args.source).expanduser().resolve()
    if src == root:
        fail("Source and target root are the same")
    if not (root / "gamekit.py").is_file() or not (src / "gamekit.py").is_file():
        fail("Source and target must each be a GameAgentKit directory")
    additions = []
    # These top-level public documents must be updated as well; previously
    # CHANGELOG and SECURITY silently stayed at the old release version.
    for base in ["gamekit.py", "install.sh", "README.md", "QUICKSTART.md",
                 "VERSION", "CHANGELOG.md", "SECURITY.md", "CONTRIBUTING.md", "LICENSE"]:
        if (src / base).is_file():
            additions.append((src / base, root / base))
    for parent in ["profiles", "templates", "prompts", "docs", "scripts", "skills",
                   "tests", "extras", "references", "examples"]:
        if not (src / parent).is_dir():
            continue
        for f in (src / parent).rglob("*"):
            if f.is_file():
                additions.append((f, root / f.relative_to(src)))

    # Preflight ALL targets before modifying ANY managed file. In particular,
    # do not follow a user-created link in target ancestry or a leftover temp.
    for s, d in additions:
        if s.is_symlink() or not s.is_file():
            fail(f"Refusing nonregular packaged source: {s}")
        relative = d.relative_to(root)
        if d.is_symlink() or (d.exists() and not d.is_file()):
            fail(f"Target path is not an ordinary file: {d}")
        path = root
        for component in relative.parts[:-1]:
            path = path / component
            if path.is_symlink() or (path.exists() and not path.is_dir()):
                fail(f"Unsafe linked/non-directory target parent: {path}")
        tmp = d.with_name(d.name + ".gamekit-tmp")
        if tmp.exists() or tmp.is_symlink():
            fail(f"Existing upgrade temporary file: {tmp}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = root / ".backups" / stamp
    if (root / ".backups").is_symlink() or backup.exists() or backup.is_symlink():
        fail(f"Unsafe or already present backup destination: {backup}")
    changed = [(s, d) for s, d in additions if not d.exists() or d.read_bytes() != s.read_bytes()]
    print(f"Upgrade {root} from {src} ({len(additions)} packaged files)")
    print(f"Backup overwritten kit files in {backup}")
    if args.dry_run:
        for s, d in changed:
            print(f"  WOULD UPDATE {d}")
        print(f"Upgrade preview. Unchanged files: {len(additions)-len(changed)}")
        return

    # Prepare all backups first; a backup write failure cannot partially
    # upgrade the installation. Restore files if a subsequent write fails.
    for _, d in changed:
        if d.exists():
            b = backup / d.relative_to(root)
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(d, b)
    replaced = []
    try:
        for s, d in changed:
            d.parent.mkdir(parents=True, exist_ok=True)
            tmp = d.with_name(d.name + ".gamekit-tmp")
            try:
                with s.open("rb") as fin, tmp.open("xb") as fout:
                    shutil.copyfileobj(fin, fout)
                shutil.copymode(s, tmp)
                tmp.replace(d)
                replaced.append(d)
            finally:
                if tmp.exists():
                    tmp.unlink()
        if (root / "scripts" / DRUI_CLI).exists():
            ensure_drui_executable(root)
    except Exception as ex:
        errors = []
        for d in reversed(replaced):
            b = backup / d.relative_to(root)
            try:
                if b.exists():
                    restore = d.with_name(d.name + ".gamekit-restore-tmp")
                    if restore.exists() or restore.is_symlink():
                        raise RuntimeError(f"Existing restore temporary file: {restore}")
                    shutil.copy2(b, restore)
                    restore.replace(d)
                else:
                    d.unlink()
            except Exception as restore_error:
                errors.append(f"{d}: {restore_error}")
        if errors:
            fail(f"Upgrade failed ({ex}); rollback INCOMPLETE: {'; '.join(errors)}. Backups: {backup}")
        fail(f"Upgrade failed ({ex}); changed files restored. Backups: {backup}")
    print(f"Upgrade completed. Unchanged files: {len(additions)-len(changed)}; custom files not in pack retained.")
    print("After upgrading, run `link --agents all` to refresh global discovery and the CLI.")



LEGACY_SKILL_NAME = "oil-ui-enhanced-review"


def cmd_migrate_drui(args):
    """Retire only the kit-owned legacy Skill and its exact links; archive originals safely.

    Requires upgrade to have installed drui. Never replaces a user's other Skill,
    copies or directories. Dry-run has no side effects.
    """
    root = Path(args.root).expanduser().resolve()
    new = root / "skills" / "drui" / "SKILL.md"
    if not new.is_file() or not re.search(r"(?m)^name:\s*drui\s*$", new.read_text(encoding="utf-8")):
        fail(f"New drui must be installed before migration: {new}")
    legacy = root / "skills" / LEGACY_SKILL_NAME
    owned = False
    if legacy.is_dir() and not legacy.is_symlink():
        old_md = legacy / "SKILL.md"
        if old_md.is_file() and not old_md.is_symlink():
            owned = bool(re.search(r"(?m)^name:\s*oil-ui-enhanced-review\s*$", old_md.read_text(encoding="utf-8")))
        if not owned:
            print(f"KEEP unknown legacy folder (not kit-owned): {legacy}")
    elif legacy.exists() or legacy.is_symlink():
        print(f"KEEP non-directory or symlink legacy entry: {legacy}")

    if owned:
        for agent in AGENT_PATHS:
            for rel in AGENT_PATHS[agent]:
                target = Path.home() / rel / LEGACY_SKILL_NAME
                if target.is_symlink() and target.resolve() == legacy.resolve():
                    print(f"  {'WOULD REMOVE' if args.dry_run else 'REMOVE'} kit-owned old link: {target}")
                    if not args.dry_run:
                        target.unlink()
                elif target.is_dir() or target.is_symlink():
                    print(f"  KEEP existing non-owned old entry: {target}")
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        archive = root / ".backups" / now / "retired-skills" / LEGACY_SKILL_NAME
        print(f"  {'WOULD ARCHIVE' if args.dry_run else 'ARCHIVE'} old canonical skill: {legacy} -> {archive}")
        if not args.dry_run:
            archive.parent.mkdir(parents=True, exist_ok=True)
            legacy.rename(archive)
    else:
        print("No kit-owned legacy skill to retire; migration is idempotent.")
    for project_arg in args.project:
        project = Path(project_arg).expanduser().resolve()
        check_project_safety(project)
        for filename in ("AGENTS.md", "CLAUDE.md"):
            path = project / filename
            if not path.is_file() or path.is_symlink():
                continue
            current = path.read_text(encoding="utf-8")
            if START not in current and END not in current:
                print(f"  KEEP unmanaged project instructions: {path}")
                continue
            if current.count(START) != 1 or current.count(END) != 1:
                print(f"  KEEP malformed managed markers: {path}")
                continue
            start = current.index(START)
            finish = current.index(END, start) + len(END)
            old_block = current[start:finish]
            if LEGACY_SKILL_NAME not in old_block:
                print(f"  KEEP already-migrated project instructions: {path}")
                continue
            new_block = old_block.replace(LEGACY_SKILL_NAME, 'drui')
            print(f"  {'WOULD REFRESH' if args.dry_run else 'REFRESH'} managed project instructions: {path}")
            if not args.dry_run:
                backup_path = path.with_name(filename + ".drui-pre-migration.bak")
                if backup_path.exists():
                    fail(f"Refusing to overwrite existing project backup: {backup_path}")
                shutil.copy2(path, backup_path)
                path.write_text(current[:start] + new_block + current[finish:], encoding="utf-8")
    print("Next: python3 ~/GameAgentKit/gamekit.py link --agents all")


def validate_external_skill(path: Path, expected_name: str):
    """Load a user-owned skill without copying or modifying it."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", expected_name):
        fail("External skill name must be lowercase kebab-case, e.g. oil-ui")
    if not path.is_dir() or not (path / "SKILL.md").is_file():
        fail(f"External skill must be a folder containing SKILL.md: {path}")
    content = (path / "SKILL.md").read_text(encoding="utf-8")
    if not content.startswith("---\n") or not re.search(r"(?m)^name:\s*[^\n]+$", content):
        fail("External skill is missing SKILL.md YAML frontmatter with a name")
    match = re.search(r"(?m)^name:\s*['\"]?([^\s'\"]+)", content)
    if match and match.group(1) != expected_name:
        fail(f"SKILL.md name {match.group(1)!r} does not match --name {expected_name!r}")
    return path.resolve()


def cmd_register_external(args):
    source = validate_external_skill(Path(args.source).expanduser().resolve(), args.name)
    count, conflicts = 0, 0
    for agent in args_agents(args.agents):
        for rel in AGENT_PATHS[agent]:
            dest = Path.home() / rel / args.name
            status = ensure_link(dest, source, dry_run=args.dry_run)
            count += status in ("created", "ok")
            conflicts += status == "collision"
    print(f"External skill {args.name}: {count} visible/planned, {conflicts} conflicts kept intact.")
    print("This command never copies or changes the external SKILL.md. Restart your agents to refresh discovery.")


def cmd_unregister_external(args):
    source = validate_external_skill(Path(args.source).expanduser().resolve(), args.name)
    count = 0
    for agent in args_agents(args.agents):
        for rel in AGENT_PATHS[agent]:
            dest = Path.home() / rel / args.name
            if dest.is_symlink() and dest.resolve() == source:
                print(f"  {'WOULD REMOVE' if args.dry_run else 'REMOVE'} owned external link {dest}")
                if not args.dry_run:
                    dest.unlink()
                count += 1
            elif dest.exists() or dest.is_symlink():
                print(f"  KEEP non-matching entry {dest}")
    print(f"Removed/previewed {count} links; original Oil UI source never touched.")



OIL_EXTENSION_START = "<!-- GameAgentKit Oil UI extension: BEGIN -->"
OIL_EXTENSION_END = "<!-- GameAgentKit Oil UI extension: END -->"


def cmd_extend_oil_ui(args):
    """Opt-in append-only customization of *the user's* installed oil-ui skill."""
    source = validate_external_skill(Path(args.source).expanduser().resolve(), "oil-ui")
    root = Path(args.root).expanduser().resolve()
    prompt_file = root / "prompts" / "OIL_UI_ENHANCED_WORKFLOW.md"
    if not prompt_file.is_file():
        fail(f"The shared kit must be installed first (missing {prompt_file})")
    skill_path = source / "SKILL.md"
    if skill_path.is_symlink():
        fail("Refusing to modify a symlinked SKILL.md; use its real source directory")
    old = skill_path.read_text(encoding="utf-8")
    existing_block = OIL_EXTENSION_START in old or OIL_EXTENSION_END in old
    if existing_block:
        if old.count(OIL_EXTENSION_START) != 1 or old.count(OIL_EXTENSION_END) != 1:
            fail("Conflicting or incomplete GameAgentKit extension markers; review manually")
        if not args.refresh:
            print("Oil UI extension already present; use --refresh to update only the managed block for drui")
            return
    block = f"""

{OIL_EXTENSION_START}
## Optional original GameAgentKit review extensions (NOT Oil UI Pro)

For a UI review, load the globally shared `drui` Skill and read:
- `{prompt_file}` for UI refresh/flow repair/component/scene selection and 3 independent review passes;
- `{root / 'docs' / 'OIL_UI_REVIEW_RUBRIC.md'}` for scored review targeting 9/10 with real screenshots/tasks;
- `{root / 'references' / 'OIL_UI_19_ORIGINAL_CARD_PATTERNS.md'}` for independent card examples.

These original instructions do not unlock, redistribute, imitate the exact templates of, or claim access to Oil UI Pro. Treat a missing runtime/simulator as BLOCKED, not a passed visual QA. Preserve this original skill's own instructions.
{OIL_EXTENSION_END}
"""
    print(f"{'WOULD REFRESH' if existing_block and args.dry_run else 'REFRESH' if existing_block else 'WOULD EXTEND' if args.dry_run else 'EXTEND'} {skill_path}")
    if args.dry_run:
        return
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = skill_path.with_name(f"SKILL.md.gamekit-backup-{timestamp}")
    if backup.exists():
        fail(f"Backup collision; retry later or rename: {backup}")
    shutil.copy2(skill_path, backup)
    temporary = skill_path.with_name("SKILL.md.gamekit-temp")
    if temporary.exists():
        fail(f"Temporary output already exists, refusing to overwrite: {temporary}")
    if existing_block:
        first = old.index(OIL_EXTENSION_START)
        last = old.index(OIL_EXTENSION_END, first) + len(OIL_EXTENSION_END)
        new_text = old[:first] + block.strip() + old[last:]
    else:
        new_text = old + block
    try:
        temporary.write_text(new_text, encoding="utf-8")
        temporary.replace(skill_path)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(f"Extension {'refreshed' if existing_block else 'appended'}; original backup: {backup}")


# Workflow stage prompts are plain-text agent instructions. This CLI does not run an
# agent, execute tools or claim evidence; users can paste the printed prompt into
# Codex, Claude Code, Antigravity or other SKILL.md-compatible agents.
WORKFLOW_STAGES = {
    'full': '完整 UI 改进循环',
    'discover': '现状诊断 / 问题分类',
    'plan': '设计方向 / 改造计划',
    'implement': '界面与交互实现',
    'visual-review': '独立视觉评审',
    'usability-review': '独立 UX / 操作性评审',
    'game-feel': '游戏手感与反馈审查',
    'fix': '按审查报告修复',
    'verify': '回归验收与评分',
    'screenshot-rebuild': '参考截图还原',
    'component-polish': '单组件极致打磨',
    'mini-game-scene': '小游戏场景专项',
    'effects': '动效 / 光效专项',
    'dashboard': '仪表盘 / 工具页专项',
    'art-3d': '角色 / 3D 资产专项',
    'review-tl': '严苛 Tech Lead 独立评审（只审查）',
    'review-pm': '严苛 PM 独立评审（只审查）',
    'review-user': '真实用户视角任务驱动评审（只审查）',
    'review-triad': '三角色独立评审与分歧仲裁（只审查）',
    'review-loop': '三方评审 → 修复 → 重审闭环（可改代码）',
 }

# Single catalog for CLI, JSON, agent-facing documentation and detailed help.
# Keys are stable command identifiers; avoid calling an AI agent from the CLI.
WORKFLOW_GROUPS = (
    ("核心开发 / Core", ("full", "discover", "plan", "implement", "fix", "verify")),
    ("界面与体验 / UI & UX", ("visual-review", "usability-review", "game-feel", "screenshot-rebuild", "component-polish")),
    ("专项设计 / Specialties", ("mini-game-scene", "effects", "dashboard", "art-3d")),
    ("严苛独立评审 / Strict Reviews", ("review-tl", "review-pm", "review-user", "review-triad", "review-loop")),
)
WORKFLOW_CATEGORIES = ("core", "ui", "specialty", "review")
WORKFLOW_WRITE_STAGES = frozenset({"full", "implement", "fix", "screenshot-rebuild", "component-polish", "review-loop"})
WORKFLOW_FLEX_STAGES = frozenset({"game-feel", "mini-game-scene", "effects", "dashboard", "art-3d"})
# The starter set is intentionally small and has both read-only and edit-capable choices.
WORKFLOW_BEGINNER = ("full", "visual-review", "usability-review", "game-feel", "review-triad", "review-loop")
# (when-to-use, expected-output, sample user request, searchable terms)
WORKFLOW_GUIDE = {
    "full": ("希望从诊断一直做到实现和验收", "改进计划、真实代码修改、测试证据及遗留问题", "从头检查并优化这个游戏的 UI 和操作流程", "start complete end to end full 开始 全流程"),
    "discover": ("不了解问题分布，想先找出瓶颈", "现状分析、任务路径与 P0/P1/P2 问题清单", "先找出这个游戏最影响体验的问题，不要改代码", "audit diagnostic problems 找问题 诊断"),
    "plan": ("需要先比较方案，尚未决定改法", "方向对比、约束、阶段计划和验收标准", "为主界面提出三种优化方案，先不修改", "strategy roadmap idea 方案 设计"),
    "implement": ("已有明确方案，需要真正落地", "可运行代码、变更说明及实际验证", "按已经确定的方案实现新关卡页", "build implement coding 开发 实现"),
    "fix": ("已经有审查报告或明确缺陷", "问题对应修复及回归检查", "按上轮 P0/P1 清单修复并回归", "bug repair defects 修复"),
    "verify": ("需要验收已实现的内容", "测试矩阵、真实证据、通过/阻塞情况", "回归测试所有页面并报告未验证项", "test regression acceptance QA 验收 测试"),
    "visual-review": ("页面不够精美，想先做只读视觉审查", "排版、配色、美术、层级问题及截图证据", "独立审查首页视觉品质，不修改代码", "beauty layout colors screenshot visual 美化 视觉"),
    "usability-review": ("玩家不知道该点哪里，操作不顺", "用户任务走查、阻塞点、交互改进建议", "从新玩家角度测试如何移动和攻击，不改代码", "touch flow navigation interaction UX 操作 易用性 手势"),
    "game-feel": ("输入、动画、音效或反馈缺乏手感", "反馈延迟/节奏/动效/音效问题及改进方案", "提升按钮、拖动、命中反馈的手感", "feel haptics audio animation responsiveness 手感 动画 音效"),
    "screenshot-rebuild": ("已有参考截图，要在项目里真实还原", "实际界面实现、适配、交互及视觉对照", "根据参考截图还原 SwiftUI 主页面", "reference image rebuild screenshot 临摹 截图 还原"),
    "component-polish": ("只想深度打磨一个组件", "组件全部状态、交互、适配和 QA", "打磨开始按钮的所有状态和动画", "button card component detail 组件 按钮"),
    "mini-game-scene": ("小游戏棋盘、操作区或结算场景有问题", "场景任务流程、可玩性和布局审查/改进", "优化小游戏棋盘、控制区与结算反馈", "board playfield scene minigame 棋盘 场景"),
    "effects": ("需要有目的地提升视觉反馈与特效", "动效方案、性能预算和验证项", "优化攻击时的命中特效和粒子", "particles motion vfx effects 粒子 特效"),
    "dashboard": ("需要优化数据密集的工具界面", "数据层级、表格/卡片布局与交互审查", "改进统计页信息布局和图表交互", "charts admin statistics data 报告 图表 仪表盘"),
    "art-3d": ("涉及角色、场景或 3D 资产制作", "资产要求、管线、落地与验收计划", "制定 3D 角色资产制作与集成计划", "art character asset model 3d 美术 角色"),
    "review-tl": ("需要独立代码架构与技术风险审查", "技术缺陷、严重性及代码证据（只读）", "请 Tech Lead 独立审查实现与性能", "architecture code technical 技术 架构 代码"),
    "review-pm": ("需要独立判断范围、价值和产品流程", "产品目标、价值、优先级与风险（只读）", "请 PM 独立审查新手引导和核心流程", "product scope priority 产品 需求"),
    "review-user": ("想知道新用户是否能独立完成任务", "真实任务走查、卡点和证据（只读）", "请用户视角不看提示玩完第一关", "first-time player user onboarding 新手 用户"),
    "review-triad": ("需要 TL、PM、用户三种视角独立评审", "分离的评审任务、报告与分歧（只读）", "分别做 TL、PM、用户独立评审，不能改代码", "three reviewers independent 独立 三方 评审"),
    "review-loop": ("想把独立审查、修复与复审串成闭环", "分轮问题、代码修复、实测与重审结论", "独立评审→修复→回归→重审，最多三轮", "iteration fix review cycle loop 循环 闭环 迭代"),
}


def workflow_mode(stage):
    if stage in WORKFLOW_WRITE_STAGES:
        return "MAY EDIT / 可修改"
    if stage in WORKFLOW_FLEX_STAGES:
        return "AS REQUESTED / 按需"
    return "REVIEW ONLY / 只审查"


def workflow_category(stage):
    for i, (_, names) in enumerate(WORKFLOW_GROUPS):
        if stage in names:
            return WORKFLOW_CATEGORIES[i], WORKFLOW_GROUPS[i][0]
    fail(f"Unknown workflow: {stage}")


def workflow_entries(*, category=None, search=None, beginner=False):
    if category and category not in WORKFLOW_CATEGORIES:
        fail(f"Unknown category {category!r}. Choose: {', '.join(WORKFLOW_CATEGORIES)}")
    query = (search or "").strip().casefold()
    entries = []
    for group, names in WORKFLOW_GROUPS:
        for name in names:
            slug, _ = workflow_category(name)
            if category and slug != category:
                continue
            if beginner and name not in WORKFLOW_BEGINNER:
                continue
            when, output, example, keywords = WORKFLOW_GUIDE[name]
            haystack = " ".join((name, group, WORKFLOW_STAGES[name], when, output, example, keywords)).casefold()
            if query and query not in haystack:
                continue
            entries.append({"name": name, "group": group, "category": slug,
                            "description": WORKFLOW_STAGES[name], "mode": workflow_mode(name),
                            "when": when, "output": output, "example": example})
    return entries


def show_workflow_menu(*, json_format=False, category=None, search=None, beginner=False):
    entries = workflow_entries(category=category, search=search, beginner=beginner)
    if json_format:
        print(json.dumps({"skill": "drui", "version": VERSION, "count": len(entries),
                          "total_count": len(WORKFLOW_STAGES), "filters": {"category": category,
                          "search": search, "beginner": beginner}, "workflows": entries},
                         ensure_ascii=False, indent=2))
        return
    print(f"DRUI v{VERSION} — {len(WORKFLOW_STAGES)} workflows" + (f" ({len(entries)} shown)" if len(entries) != len(WORKFLOW_STAGES) else ""))
    if category or search or beginner:
        filters = ([f"category={category}"] if category else []) + ([f"search={search!r}"] if search else []) + (["beginner"] if beginner else [])
        print("Filters: " + ", ".join(filters))
    else:
        print("新手先选: usability-review (操作难用) | visual-review (画面不好看) | review-loop (审查并修复)")
        print("想从头完整改进? full    想只让三方评审? review-triad")
    if not entries:
        print("没有匹配的工作流。试试: drui list --category review 或 drui list --search 操作")
        return
    names = {entry['name'] for entry in entries}
    for group, members in WORKFLOW_GROUPS:
        selected = [name for name in members if name in names]
        if not selected:
            continue
        print(f"\n[{group}]")
        for name in selected:
            mode = "只读" if workflow_mode(name).startswith("REVIEW") else "可修改" if workflow_mode(name).startswith("MAY") else "按需"
            print(f"  {name:20} {WORKFLOW_STAGES[name]} [{mode}]")
    print("\n下一步: drui help <workflow> 了解适用场景；drui prompt <workflow> 生成可复制的 Agent 指令")
    print("分类: drui list --category core|ui|specialty|review  |  搜索: drui list --search 操作")
    print("注意: 终端只打印 Prompt，不运行 Agent；在 Agent 对话中说 'Use drui, stage review-loop, on this project.'")


def show_workflow_help(stage):
    if stage not in WORKFLOW_STAGES:
        fail(f"Unknown workflow: {stage}. Run drui list for valid names.")
    slug, group = workflow_category(stage)
    when, output, example, _ = WORKFLOW_GUIDE[stage]
    print(f"DRUI / {stage} — {WORKFLOW_STAGES[stage]}")
    print(f"分类 / Category: {slug} ({group})")
    print(f"权限 / Mode: {workflow_mode(stage)}")
    print(f"适用场景 / When: {when}")
    print(f"预期交付 / Output: {output}")
    print(f"\nAgent 对话示例 (会请求 Agent 执行):\n  Use the drui skill, stage {stage}, on this project. {example}。")
    print(f"\n终端命令 (只打印指令，不运行 Agent):\n  drui prompt {stage} --project /path/to/game")
    print(f"参考工作流 / Source: prompts/drui/stages/{stage}.md")
    if stage in ('review-triad', 'review-loop'):
        print("独立性: TL / PM / User 需要隔离上下文与实际测试证据；做不到时必须标记 PROVISIONAL/BLOCKED。")
    print("更多工作流: drui list --beginner | drui list --category " + slug)


def cmd_workflow(args):
    root = Path(args.root).expanduser().resolve()
    if args.action == "list":
        show_workflow_menu(json_format=getattr(args, 'json', False), category=getattr(args, 'category', None), search=getattr(args, 'search', None), beginner=getattr(args, 'beginner', False))
        return
    if args.action != "prompt":
        fail("Choose workflow list or workflow prompt")
    stage = args.stage
    path = root / "prompts" / "drui" / "stages" / f"{stage}.md"
    if not path.is_file():
        fail(f"Stage prompt not installed: {path}. Upgrade GameAgentKit to V1.4 first.")
    if args.project:
        project = Path(args.project).expanduser().resolve()
        check_project_safety(project)
        target = str(project)
        profile = project / ".game-agent-kit" / "PROFILE.md"
        profile_text = f"Read project profile: {profile}\n" if profile.is_file() else "No GameAgentKit project profile; inspect existing project instructions.\n"
    else:
        target = "the currently opened project / repository"
        profile_text = "Read AGENTS.md, CLAUDE.md, README, and .game-agent-kit/PROFILE.md if present.\n"
    requested_ui_source = getattr(args, "ui_source", "auto")
    selected_ui_source, selected_skill_path, available_ui_sources = select_ui_source(
        root, requested_ui_source, agent=getattr(args, "agent", "all"), project=getattr(args, "project", None))
    dependency_status = 'BUNDLED / KIT-MANAGED'
    if selected_ui_source in ('pro', 'oil-ui'):
        _, dependency_status = depguard.is_approved_source(
            root, DRUI_UI_SKILLS[selected_ui_source], selected_skill_path,
            agent=getattr(args, 'agent', 'all'))
    selection_text = (
        "UI method priority: oil-ui-pro (official, installed only) > "
        "oil-ui-plus (our original Pro-like approximation) > oil-ui (open-source) > DRUI fallback.\n"
        f"Requested UI source: {requested_ui_source}. Primary selected source in CLI environment: "
        f"{DRUI_UI_SKILLS[selected_ui_source]} at {selected_skill_path}.\n"
        f"External dependency status: {dependency_status}.\n"
        "In your actual Agent environment, VERIFY this SKILL.md is readable and read it before execution. "
        "In auto mode, fallback to the next accessible source if necessary and disclose reason; "
        "if a source was explicitly requested, FAIL visibly instead of switching. "
        "DRUI remains the stage orchestrator; never confuse Oil UI Plus with the official paid Pro.\n"
        "Before using an external Oil UI Skill, run `drui deps check --agent <actual-agent>` when locked. "
        "If the upstream Skill changed, do not run its new instructions until separately reviewed and approved; "
        "auto mode falls back to the next trusted source (normally our oil-ui-plus). "
        "An untracked dependency is NOT equivalent to compatibility approval. "
        "Never auto-update third-party Skills during a DRUI task.\n"
        "Report: requested_source, selected_source, actual_skill_read, fallback_reason, external_dependency_status.\n"
    )
    result = (
        f"Activate the globally installed `drui` skill.\n"
        + selection_text
        + f"Work on: {target}\n"
        f"Run ONLY stage `{stage}` (or all applicable stages if `full`). Do not silently widen scope.\n"
        f"{profile_text}"
        f"Reference: {root / 'docs' / 'OIL_UI_REVIEW_RUBRIC.md'}\n\n"
        + path.read_text(encoding="utf-8")
    )
    if args.output:
        output = Path(args.output).expanduser().resolve()
        if output.exists() and not args.force:
            fail(f"Output already exists: {output}; choose a fresh file or pass --force")
        if output == path or output == root / "gamekit.py":
            fail("Refusing to overwrite a kit source file")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        print(f"Wrote stage '{stage}' prompt to: {output}")
    else:
        print(result)



# This CLI validates review REPORT COMPLETENESS only, not the truth of human observations.
# Three separate agents/sessions are required for an independent release approval.
REVIEW_ROLES = {
    "tech-lead": ("architecture", "correctness", "performance", "maintainability", "integration"),
    "product-manager": ("user_value", "onboarding", "flow", "scope", "retention"),
    "end-user": ("clarity", "touch", "feedback", "confidence", "enjoyment"),
}


def cmd_review(args):
    if args.action == "prepare":
        root = Path(args.root).expanduser().resolve()
        target = Path(args.output).expanduser().resolve()
        if target.exists():
            fail(f"Review directory already exists; no overwrite permitted: {target}")
        if args.project:
            project = Path(args.project).expanduser().resolve()
            check_project_safety(project)
            project_note = str(project)
        else:
            project_note = "currently opened repository"
        originals = {}
        for role in REVIEW_ROLES:
            filename = root / "prompts" / "drui" / "reviewers" / f"{role}.md"
            if not filename.is_file():
                fail(f"Missing role instructions: {filename}")
            originals[role] = filename.read_text(encoding="utf-8")
        print(f"{'WOULD PREPARE' if args.dry_run else 'PREPARE'} independent reviews under {target}")
        if args.dry_run:
            return
        target.mkdir(parents=True)
        (target / "evidence").mkdir()
        for role, content in originals.items():
            instructions = (f"# DRUI independent reviewer: {role}\n\n"
                            f"Project: {project_note}\n"
                            f"Output report: {target / (role + '.json')}\n"
                            "Open a NEW independent agent session for this role; do not show other reviewers' notes.\n"
                            "Treat pre-filled JSON as BLANK, not evidence.\n\n" + content)
            (target / f"PROMPT_{role}.md").write_text(instructions, encoding="utf-8")
            blank = {"reviewer": role, "session_id": "", "independence": "single-session",
                     "scope": "", "screens_examined": [], "evidence_files": [],
                     "tasks_tested": [], "observations": [],
                     "scores": {axis: None for axis in REVIEW_ROLES[role]},
                     "findings": [], "limitations": ["NOT RUN"], "source_changes": False}
            (target / f"{role}.json").write_text(json.dumps(blank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (target / "RUN_ME_FIRST.md").write_text(
            "# DRUI three-reviewer handoff\n\n"
            "1. Use three distinct fresh agent contexts for Tech Lead, PM, and User. \n"
            "2. Give each context ONLY its matching PROMPT_*.md, project files, and its own runtime evidence; hide the other reports.\n"
            "3. The review is READ-ONLY. Save genuine screenshots/logs under evidence/.\n"
            "4. Fill each <role>.json; blank template is NOT a completed review.\n"
            "5. Run `python3 ~/GameAgentKit/gamekit.py review evaluate --dir <this-folder>`.\n"
            "6. If failing: fix P0/P1 in a separate implementation context; gather NEW evidence; ask reviewers to retest.\n"
            "7. A single chat role-play of three reviewers is PROVISIONAL, never independent sign-off.\n",
            encoding="utf-8")
        print("Prepared read-only role prompts and blank evidence/report templates (no review executed).")
    elif args.action == "evaluate":
        folder = Path(args.dir).expanduser().resolve()
        if not folder.is_dir():
            fail(f"Review folder does not exist: {folder}")
        problems = []
        verdicts = {}
        session_ids = []
        for role, axes in REVIEW_ROLES.items():
            report = folder / f"{role}.json"
            if not report.is_file():
                problems.append(f"{role}: missing report")
                continue
            try:
                data = json.loads(report.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeError) as exc:
                problems.append(f"{role}: invalid JSON ({exc})")
                continue
            if not isinstance(data, dict) or data.get("reviewer") != role:
                problems.append(f"{role}: reviewer identity does not match")
                continue
            if data.get("source_changes") is not False:
                problems.append(f"{role}: reviewer must be read-only")
            session = data.get("session_id")
            if not isinstance(session, str) or not session.strip():
                problems.append(f"{role}: no session_id; separate contexts cannot be assessed")
            else:
                session_ids.append(session.strip())
            if data.get("independence") != "isolated-session":
                problems.append(f"{role}: review is not marked isolated-session (provisional only)")
            if not isinstance(data.get("scope"), str) or not data.get("scope", "").strip():
                problems.append(f"{role}: missing scope")
            for field in ("screens_examined", "tasks_tested", "observations", "evidence_files"):
                items = data.get(field)
                if not isinstance(items, list) or not items:
                    problems.append(f"{role}: {field} missing or empty")
            if isinstance(data.get("observations"), list) and len(data["observations"]) < 3:
                problems.append(f"{role}: fewer than 3 concrete observations")
            files = data.get("evidence_files", [])
            if isinstance(files, list):
                # Logs are valuable but cannot, by themselves, establish visual/UI review.
                if files and not any(isinstance(f, str) and Path(f).suffix.lower() in
                                     (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov") for f in files):
                    problems.append(f"{role}: visual screenshot/video evidence required (logs alone insufficient)")
                for filename in files:
                    if not isinstance(filename, str) or not filename.strip():
                        problems.append(f"{role}: malformed evidence path")
                        continue
                    resolved = (folder / filename).resolve() if not Path(filename).is_absolute() else Path(filename).resolve()
                    if not resolved.is_file():
                        problems.append(f"{role}: missing evidence file: {filename}")
            scores = data.get("scores", {})
            if not isinstance(scores, dict) or set(scores) != set(axes):
                problems.append(f"{role}: incomplete rubric axes: expected {', '.join(axes)}")
                continue
            if any(isinstance(scores[a], bool) or not isinstance(scores[a], (int,float)) or not (0 <= scores[a] <= 10) for a in axes):
                problems.append(f"{role}: scores must be actual 0..10 numbers, no null/booleans")
                continue
            avg = sum(scores.values()) / len(scores)
            verdicts[role] = round(avg, 2)
            if avg < 9 or min(scores.values()) < 8:
                problems.append(f"{role}: score gate failed (mean {avg:.2f} < 9 or any axis < 8)")
            findings = data.get("findings")
            if not isinstance(findings, list):
                problems.append(f"{role}: findings must be an array")
                continue
            for i, finding in enumerate(findings):
                if not isinstance(finding, dict):
                    problems.append(f"{role}: findings[{i}] must be an object")
                    continue
                for k in ("id", "severity", "screen", "evidence", "repro_steps", "expected", "actual", "recommendation", "acceptance_test", "status"):
                    if not finding.get(k):
                        problems.append(f"{role}: findings[{i}] missing {k}")
                if finding.get("severity") not in ("P0", "P1", "P2", "P3"):
                    problems.append(f"{role}: findings[{i}] severity invalid")
                if finding.get("status") not in ("open", "fixed-unverified", "verified"):
                    problems.append(f"{role}: findings[{i}] status invalid")
                if finding.get("severity") in ("P0", "P1") and finding.get("status") != "verified":
                    problems.append(f"{role}: unresolved {finding.get('severity')} {finding.get('id', i)}")
            limitations = data.get("limitations", [])
            if not isinstance(limitations, list):
                problems.append(f"{role}: limitations must be a list")
            elif any(str(item).upper().startswith(("BLOCKED", "NOT RUN", "UNVERIFIED")) for item in limitations):
                problems.append(f"{role}: blocked/unverified checks")
        if len(session_ids) == 3 and len(set(session_ids)) != 3:
            problems.append("Reviewers share a session_id; independent contexts not established")
        if len(verdicts) == 3:
            print("Scores: " + ", ".join(f"{k}={v:.2f}" for k,v in verdicts.items()))
        else:
            print("Scores: INCOMPLETE")
        status = "NOT APPROVED" if problems else "REPORT GATES PASSED (evidence authenticity requires human inspection)"
        print(f"DRUI triad status: {status}")
        for item in problems:
            print("  - " + item)
        if problems:
            fail(f"{len(problems)} issue(s); do not claim independent 9/10 acceptance")
        print("This validates report structure and linked evidence existence; it does not prove screenshots or reviewer independence are genuine.")
    else:
        fail("Choose review prepare or review evaluate")


def cmd_online_update(args):
    from scripts.github_update import update
    return update(root=Path(args.root).expanduser().absolute(), repo=args.repo,
                  check=args.check, dry_run=args.dry_run, yes=args.yes)



def cmd_dependencies(args):
    root = Path(args.root).expanduser().resolve()
    agents = args_agents(args.agent)
    project = getattr(args, 'project', None)
    if project and not Path(project).expanduser().is_dir():
        fail(f'Project directory not found: {project}')
    current = depguard.enumerate_external(root, Path.home(), agents, AGENT_PATHS, project=project)
    old = depguard.read_lock(root)
    if args.action in ('list', 'conflicts'):
        if args.action == 'conflicts':
            collisions = report_skill_conflicts(root, agents, project=project)
            if not collisions:
                print('No same-name collisions detected in scanned global/project Skill directories.')
            print('Scanning these paths cannot prove which Skill an Agent actually loaded.')
            return
        print(f"External third-party Skills and User-owned Skills (kit-owned links excluded; same-name copies INCLUDED): {len(current)} slots")
        for k, v in current.items():
            print(f"  {k} -> {v['source']} ({v['sha256'][:12]})")
        print('No external Skills are updated by `drui update`.')
        return
    if args.action == 'lock':
        if old is not None:
            fail('Dependency lock exists; use `drui deps check` and `drui deps approve` to accept individual changes.')
        if args.dry_run:
            print(f'WOULD create {depguard.lock_path(root)} with {len(current)} installed external Skill slots')
            return
        depguard.save_lock(root, depguard.fresh_doc(current), backup=False)
        print(f"BASELINE CREATED: {len(current)} external Skill slots. Initial lock is a snapshot, NOT a compatibility test.")
        return
    if args.action == 'check':
        if old is None:
            fail('No dependency baseline exists. First inspect with `drui deps list`, then `drui deps lock`.')
        # Evaluate only the requested agent scope; other approved agents are unaffected.
        scoped = dict(old, approved={k:v for k,v in old['approved'].items() if v.get('agent') in agents})
        status = depguard.compare(current, scoped)
        for k, state in sorted(status.items()):
            print(f'{state:9} {k}')
        pending = {k: v for k, v in status.items() if v != 'OK'}
        if pending:
            fail(f'{len(pending)} external dependency change(s) require review. Do not blindly accept upgrades.')
        print(f'PASS: {len(status)} external Skill slots unchanged from approved fingerprints.')
        return
    if args.action == 'approve':
        if old is None:
            fail('Create a baseline first: drui deps lock')
        evidence = Path(args.evidence).expanduser().resolve()
        if not evidence.is_file() or not evidence.read_text(encoding='utf-8').strip():
            fail('Approval requires a non-empty written review evidence file.')
        selected = {k:v for k,v in current.items() if v['name'] == args.name}
        if not selected:
            fail(f'No installed external Skill named {args.name!r} found for specified agent scope.')
        print(f"{'WOULD ' if args.dry_run else ''}APPROVE {args.name}: {len(selected)} slot(s), manual evidence {evidence}")
        if not args.dry_run:
            updated = dict(old['approved'])
            for k,v in selected.items():
                updated[k] = dict(v, reviewed_at=datetime.now(timezone.utc).isoformat(), evidence=str(evidence))
            depguard.save_lock(root, depguard.fresh_doc(updated))
            print('Approved new fingerprint snapshots. This does not prove safety; run actual Agent compatibility and QA tests.')
        return
    fail('Unknown dependencies subcommand')

def build_parser():
    p = argparse.ArgumentParser(description="One shared skills hub for many games and agents")
    p.add_argument("--version", action="version", version=VERSION)
    sp = p.add_subparsers(dest="command", required=True)
    install = sp.add_parser("install", help="Link Skills and CLI from a local GitHub source checkout")
    install.add_argument("--root", default="~/GameAgentKit")
    install.add_argument("--agents", default="all")
    install.add_argument("--copy", action="store_true", help="Copy skills if symlinks unsupported (updates require relinking)")
    install.add_argument("--dry-run", action="store_true")
    install.set_defaults(func=cmd_install)
    link = sp.add_parser("link", help="Link shared skills into additional global agent paths")
    link.add_argument("--root", default="~/GameAgentKit")
    link.add_argument("--agents", default="all")
    link.add_argument("--copy", action="store_true")
    link.add_argument("--dry-run", action="store_true")
    link.set_defaults(func=cmd_link)
    unlink = sp.add_parser("unlink", help="Remove only owned global symlinks (keep central root and project files)")
    unlink.add_argument("--root", default="~/GameAgentKit")
    unlink.add_argument("--agents", default="all")
    unlink.add_argument("--dry-run", action="store_true")
    unlink.set_defaults(func=cmd_unlink)
    migration = sp.add_parser("migrate-drui", help="Safely retire the V1.2 UI Skill name and its owned links, preserving backups")
    migration.add_argument("--root", default="~/GameAgentKit")
    migration.add_argument("--dry-run", action="store_true")
    migration.add_argument("--project", action="append", default=[], help="Optional project path(s): refresh only old kit-managed AGENTS.md/CLAUDE.md blocks")
    migration.set_defaults(func=cmd_migrate_drui)
    attach = sp.add_parser("attach", help="Optionally add tiny per-game profile, without copying skills")
    attach.add_argument("--project", required=True)
    attach.add_argument("--profile", choices=PROFILES, default="generic")
    attach.add_argument("--name")
    attach.add_argument("--root", default="~/GameAgentKit")
    attach.add_argument("--dry-run", action="store_true")
    attach.set_defaults(func=cmd_attach)
    verify = sp.add_parser("verify", help="Read-only: list actual Skill links, bundled versions, missing paths and collisions")
    verify.add_argument("--root", default="~/GameAgentKit")
    verify.add_argument("--agents", default="codex,claude,antigravity,cursor",
                        help="Agents to inspect; default all four, unlike legacy --agents all")
    verify.add_argument("--json", action="store_true", help="Machine-readable verification report")
    verify.add_argument("--compact", action="store_true", help="One-line summary, at most three failure details")
    verify.add_argument("--project", help="Warn about possible project-local same-name Skill shadows")
    verify.set_defaults(func=cmd_verify)
    doc = sp.add_parser("doctor", help="Check global skill paths and optional project configuration")
    doc.add_argument("--root", default="~/GameAgentKit")
    doc.add_argument("--agents", default="all")
    doc.add_argument("--project")
    doc.set_defaults(func=cmd_doctor)
    deps = sp.add_parser("deps", help="Audit external Skill versions; never update them automatically")
    dsub = deps.add_subparsers(dest="action", required=True)
    for act in ("list", "conflicts", "lock", "check", "approve"):
        dc = dsub.add_parser(act)
        dc.add_argument("--root", default="~/GameAgentKit")
        dc.add_argument("--agent", default="all", help="codex, claude, antigravity, cursor, or all")
        dc.add_argument("--project", help="Also inspect project-local Skill directories (optional)")
        if act == 'approve':
            dc.add_argument('--name', required=True)
            dc.add_argument('--evidence', required=True, help='Written compatibility review evidence file')
        if act in ('lock','approve'):
            dc.add_argument('--dry-run', action='store_true')
        dc.set_defaults(func=cmd_dependencies)
    online = sp.add_parser("update", help="Check or apply a verified GitHub Release update")
    online.add_argument("--root", default="~/GameAgentKit")
    online.add_argument("--repo", help="GitHub owner/repo; initially inferred from clone, or provided explicitly")
    online.add_argument("--check", action="store_true", help="Read latest stable release metadata only")
    online.add_argument("--dry-run", action="store_true", help="Preview the available release without downloading it")
    online.add_argument("--yes", action="store_true", help="Approve installation of the checksum-verified release")
    online.set_defaults(func=cmd_online_update)
    upgrade = sp.add_parser("upgrade", help="Internal file-tree upgrade utility (prefer tagged GitHub source: drui update)")
    upgrade.add_argument("--from", dest="source", required=True)
    upgrade.add_argument("--root", default="~/GameAgentKit")
    upgrade.add_argument("--dry-run", action="store_true")
    upgrade.set_defaults(func=cmd_upgrade)
    for command, callback in [("register-external", cmd_register_external),
                              ("unregister-external", cmd_unregister_external)]:
        reg = sp.add_parser(command, help="Safely share an existing user-owned SKILL.md folder without copying")
        reg.add_argument("--name", required=True, help="Skill name, e.g. oil-ui")
        reg.add_argument("--source", required=True, help="Existing skill folder containing SKILL.md")
        reg.add_argument("--agents", default="all")
        reg.add_argument("--dry-run", action="store_true")
        reg.set_defaults(func=callback)
    workflow = sp.add_parser("workflow", help="List workflows or print a standalone agent-ready DRUI prompt")
    workflow_sub = workflow.add_subparsers(dest="action", required=True)
    wl = workflow_sub.add_parser("list", help="List independently invokable review and implementation stages")
    wl.add_argument("--root", default="~/GameAgentKit")
    wl.add_argument("--json", action="store_true", help="Machine-readable DRUI workflow list")
    wl.add_argument("--beginner", action="store_true", help="Show six beginner-friendly starting points")
    wl.add_argument("--category", choices=WORKFLOW_CATEGORIES, help="Filter: core, ui, specialty, review")
    wl.add_argument("--search", help="Search names, descriptions and use cases (Chinese/English)")
    wl.set_defaults(func=cmd_workflow)
    wp = workflow_sub.add_parser("prompt", help="Print an agent-ready prompt for one stage or the full workflow")
    wp.add_argument("--stage", choices=list(WORKFLOW_STAGES), required=True)
    wp.add_argument("--project", help="Optional absolute/relative path to an existing game repository")
    wp.add_argument("--ui-source", choices=DRUI_UI_SOURCE_CHOICES, default="auto", help="Choose UI method source; auto prefers official Pro > bundled Plus > Oil UI > DRUI")
    wp.add_argument("--agent", default="all", help="Check UI source availability for one agent: codex, claude, antigravity, cursor, or all")
    wp.add_argument("--root", default="~/GameAgentKit")
    wp.add_argument("--output", help="Optionally save the prompt to a text/Markdown file")
    wp.add_argument("--force", action="store_true", help="Allow overwriting an existing output file")
    wp.set_defaults(func=cmd_workflow)
    sources = sp.add_parser("ui-sources", help="Inspect installed UI method source priority and availability")
    sources.add_argument("--root", default="~/GameAgentKit")
    sources.add_argument("--agent", default="all", help="Scope checks to codex, claude, antigravity, cursor, or all")
    sources.set_defaults(func=cmd_ui_sources)
    ext = sp.add_parser("extend-oil-ui", help="Opt-in append-only extension to a real existing oil-ui SKILL.md, with backup")
    ext.add_argument("--source", required=True, help="Original user-owned Oil UI folder with SKILL.md")
    ext.add_argument("--root", default="~/GameAgentKit")
    ext.add_argument("--dry-run", action="store_true")
    ext.add_argument("--refresh", action="store_true", help="Refresh only the previously managed Oil UI extension block with drui references")
    ext.set_defaults(func=cmd_extend_oil_ui)
    review = sp.add_parser("review", help="Prepare independent TL/PM/User reviews or evaluate structured evidence")
    rsub = review.add_subparsers(dest="action", required=True)
    rp = rsub.add_parser("prepare", help="Create three separate read-only reviewer assignments and blank reports")
    rp.add_argument("--root", default="~/GameAgentKit")
    rp.add_argument("--project", help="Existing game repository; otherwise currently opened repository")
    rp.add_argument("--output", required=True, help="New destination folder, must not already exist")
    rp.add_argument("--dry-run", action="store_true")
    rp.set_defaults(func=cmd_review)
    reval = rsub.add_parser("evaluate", help="Validate triad reports, evidence paths and stringent release gates")
    reval.add_argument("--dir", required=True)
    reval.set_defaults(func=cmd_review)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
