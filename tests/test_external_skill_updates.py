"""Change detection, approval and UI source fail-closed behavior for third-party Skills."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'gamekit.py'


class ExternalSkillUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='drui-deps-')
        self.home = Path(self.tmp.name) / 'home'
        self.home.mkdir()
        self.kit = self.home / 'GameAgentKit'
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE='1')
        self.call('install', '--root', self.kit, '--agents', 'all')

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args, ok=True):
        r = subprocess.run([sys.executable, str(CLI), *map(str, args)], env=self.env,
                           text=True, capture_output=True, timeout=45)
        if ok:
            self.assertEqual(r.returncode, 0, (r.stdout, r.stderr))
        return r

    def add_external(self, name='oil-ui', agent='all'):
        path = self.home / 'vendors' / name
        path.mkdir(parents=True)
        (path / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: test\n---\noriginal', encoding='utf8')
        self.call('register-external', '--name', name,
                  '--source', path, '--agents', agent)
        return path

    def deps(self, action, *rest, ok=True):
        return self.call('deps', action, '--root', self.kit, *rest, ok=ok)

    def test_lock_then_modified_content_is_detected_without_updating_lock(self):
        original = self.add_external()
        self.deps('lock')
        baseline = self.kit / '.state/external-skills.lock.json'
        previous = baseline.read_text()
        self.assertIn('PASS', self.deps('check').stdout)
        (original / 'SKILL.md').write_text((original / 'SKILL.md').read_text() + '\nupdate')
        changed = self.deps('check', ok=False)
        self.assertNotEqual(changed.returncode, 0)
        self.assertIn('CHANGED', changed.stdout)
        self.assertEqual(baseline.read_text(), previous)

    def test_new_external_skill_is_unapproved_until_accepted(self):
        self.deps('lock')
        self.add_external('oil-ui-pro', 'codex')
        self.assertIn('NEW', self.deps('check', '--agent', 'codex', ok=False).stdout)
        sources = self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout
        self.assertIn('selected automatically: oil-ui-plus', sources)
        forced = self.call('workflow', 'prompt', '--root', self.kit, '--stage', 'full',
                           '--agent', 'codex', '--ui-source', 'pro', ok=False)
        self.assertIn('CHANGED/UNAPPROVED', forced.stderr)

    def test_approved_pro_is_first_and_changes_fall_back_to_plus(self):
        upstream = self.add_external('oil-ui-pro', 'codex')
        self.deps('lock')
        before = self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout
        self.assertIn('selected automatically: oil-ui-pro', before)
        (upstream / 'reference.md').write_text('Added instructions!')
        after = self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout
        self.assertIn('selected automatically: oil-ui-plus', after)
        doc = self.home / 'evidence.md'
        doc.write_text('Inspected diff, commands, requirements; isolated QA passed; approved.', encoding='utf8')
        self.deps('approve', '--name', 'oil-ui-pro', '--agent', 'codex', '--evidence', doc)
        self.assertIn('PASS', self.deps('check', '--agent', 'codex').stdout)
        approved = self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout
        self.assertIn('selected automatically: oil-ui-pro', approved)
        self.assertTrue(list((self.kit / '.state/backups').glob('*.json')))

    def test_empty_evidence_refused_and_dry_run_does_not_approve(self):
        self.add_external()
        self.deps('lock')
        self.add_external('oil-ui-pro', 'codex')
        bad = self.home / 'bad.md'; bad.write_text('')
        self.assertNotEqual(0, self.deps('approve', '--name', 'oil-ui-pro', '--evidence', bad, ok=False).returncode)
        good = self.home / 'good.md'; good.write_text('reviewed tests and exact changes')
        self.deps('approve', '--name', 'oil-ui-pro', '--evidence', good, '--dry-run')
        self.assertIn('NEW', self.deps('check', '--agent', 'codex', ok=False).stdout)

    def test_agent_scope_only_checks_chosen_agent(self):
        source = self.add_external('oil-ui', 'codex')
        self.deps('lock')
        self.assertIn('PASS', self.deps('check', '--agent', 'codex').stdout)
        self.assertIn('PASS', self.deps('check', '--agent', 'claude').stdout)
        (source / 'SKILL.md').write_text((source / 'SKILL.md').read_text() + '\nv2')
        self.assertNotEqual(0, self.deps('check', '--agent', 'codex', ok=False).returncode)
        self.assertIn('PASS', self.deps('check', '--agent', 'claude').stdout)

    def test_missing_link_is_detected(self):
        self.add_external('oil-ui', 'codex')
        self.deps('lock')
        (self.home / '.agents/skills/oil-ui').unlink()
        res = self.deps('check', '--agent', 'codex', ok=False)
        self.assertIn('MISSING', res.stdout)

    def test_baseline_cannot_be_silently_replaced(self):
        self.deps('lock')
        self.assertNotEqual(0, self.deps('lock', ok=False).returncode)
        self.assertIn('External third-party Skills', self.deps('list').stdout)

    def test_unlocked_warns_and_prompt_still_works_for_backwards_compat(self):
        self.add_external('oil-ui-pro', 'codex')
        self.assertIn('NOT CREATED', self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout)
        r = self.deps('check', ok=False)
        self.assertIn('No dependency baseline', r.stderr)
        prompt = self.call('workflow', 'prompt', '--root', self.kit, '--stage', 'visual-review', '--agent', 'codex').stdout
        self.assertIn('oil-ui-pro', prompt)
        self.assertIn('UNLOCKED', prompt)

    def test_nested_file_symlink_refused(self):
        src = self.add_external('oil-ui', 'codex')
        (src / 'escape.md').symlink_to(self.home / 'outside')
        self.assertNotEqual(0, self.deps('lock', ok=False).returncode)

    def test_user_installed_same_name_is_preserved_and_fingerprinted(self):
        # Simulate an existing global Skill with identical name but different owner.
        dest = self.home / '.agents/skills/game-feel-polish'
        dest.unlink()  # remove ONLY kit-owned test symlink
        dest.mkdir()
        (dest/'SKILL.md').write_text('---\nname: game-feel-polish\ndescription: mine\n---\nuser-version-1')
        self.call('link', '--root', self.kit, '--agents', 'codex')
        self.assertFalse(dest.is_symlink())
        self.assertIn('user-version-1', (dest/'SKILL.md').read_text())
        conflicts = self.deps('conflicts', '--agent', 'codex').stdout
        self.assertIn('COLLISION', conflicts)
        self.assertIn('game-feel-polish', conflicts)
        self.deps('lock')
        self.assertIn('PASS', self.deps('check').stdout)
        (dest/'SKILL.md').write_text((dest/'SKILL.md').read_text() + '\nuser-version-2')
        self.assertIn('CHANGED', self.deps('check', '--agent','codex', ok=False).stdout)
        # The updater cannot rollback or overwrite this directory.
        self.assertIn('user-version-2', (dest/'SKILL.md').read_text())

    def test_same_name_oil_ui_plus_fails_closed_instead_of_claiming_kit_copy(self):
        dest = self.home / '.agents/skills/oil-ui-plus'
        dest.unlink()
        dest.mkdir()
        (dest/'SKILL.md').write_text('---\nname: oil-ui-plus\ndescription: custom\n---\ncustom plus')
        # Auto route may fall back to drui, but must not incorrectly claim kit Plus.
        summary = self.call('ui-sources', '--root', self.kit, '--agent', 'codex').stdout
        self.assertIn('selected automatically: drui', summary)
        forced = self.call('workflow', 'prompt', '--root', self.kit, '--stage', 'full',
                           '--agent', 'codex', '--ui-source', 'plus', ok=False)
        self.assertIn('same-name user copy', forced.stderr)
        self.assertIn('oil-ui-plus', self.deps('conflicts','--agent','codex').stdout)

    def test_project_override_conflict_detected_separately(self):
        project = self.home/'sample-game'
        (project/'.agents/skills/drui').mkdir(parents=True)
        (project/'.agents/skills/drui/SKILL.md').write_text('---\nname: drui\ndescription: local override\n---\n')
        details = self.deps('conflicts', '--agent', 'codex', '--project', project).stdout
        self.assertIn('COLLISION', details)
        self.assertIn('project:', details)
        # Even though global DRUI is installed, cannot promise project Agent loads it.
        failed = self.call('workflow','prompt','--root',self.kit,'--stage','full','--agent','codex',
                           '--project',project, '--ui-source','drui', ok=False)
        self.assertIn('same-name user copy', failed.stderr)

    def test_drui_frontend_dispatches_dependency_subcommands_correctly(self):
        cli = self.kit/'scripts/drui'
        proc = subprocess.run([sys.executable,str(cli),'deps','list','--agent','codex'],
                              text=True,capture_output=True,env=self.env,timeout=15)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertIn('User-owned Skills', proc.stdout)
        help_run = subprocess.run([sys.executable,str(cli),'--help'],text=True,
                                  capture_output=True,env=self.env,timeout=15)
        self.assertIn('drui deps conflicts',help_run.stdout)

    def test_no_hidden_local_pin_in_github_release(self):
        self.deps('lock')
        import zipfile
        from scripts.create_release import create_release
        with tempfile.TemporaryDirectory() as td:
            archive, _ = create_release(Path(td))
            with zipfile.ZipFile(archive) as z:
                self.assertFalse(any('.state/' in n for n in z.namelist()))
                self.assertTrue(any(n.endswith('scripts/dependency_guard.py') for n in z.namelist()))


if __name__ == '__main__':
    unittest.main()
