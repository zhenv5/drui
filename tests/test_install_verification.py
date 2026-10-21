"""Installation verification audits files, not actual Agent runtime loading."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class InstallVerificationTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix='drui-verify-')
        self.addCleanup(self.workspace.cleanup)
        self.home = Path(self.workspace.name) / 'home'
        self.home.mkdir()
        self.root = self.home / 'GameAgentKit'
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE='1')

    def run_drui(self, *args, expected=0):
        cmd = [sys.executable, str(self.root / 'scripts' / 'drui'), *args]
        proc = subprocess.run(cmd, env=self.env, capture_output=True, text=True, timeout=35)
        self.assertEqual(proc.returncode, expected, proc.stderr + '\n' + proc.stdout)
        return proc

    def install(self, *agents, expected=0):
        agent_names = ','.join(agents) if agents else 'codex,claude,antigravity,cursor'
        proc = subprocess.run([sys.executable, str(SOURCE / 'gamekit.py'), 'install',
                               '--root', str(self.root), '--agents', agent_names],
                              env=self.env, text=True, capture_output=True, timeout=45)
        self.assertEqual(proc.returncode, expected, proc.stdout + proc.stderr)
        return proc

    def test_install_prints_auto_verification_and_explicit_skill_names(self):
        output = self.install('codex', 'claude').stdout
        self.assertIn('DRUI v', output)
        self.assertIn('PASS | 2 agents | 24/24 Skill links', output)
        self.assertIn('runtime untested', output)
        self.assertNotIn('[codex] 12/12 installed slots', output)
        data = json.loads(self.run_drui('verify', '--agents', 'codex,claude', '--json').stdout)
        self.assertEqual(data['summary'], {'installed': 24, 'expected': 24, 'complete': True})
        self.assertEqual(data['version'], (SOURCE / 'VERSION').read_text().strip())
        self.assertEqual(len(data['agents']), 2)
        self.assertTrue(all(x['status'] == 'OK' for a in data['agents'] for x in a['skills']))
        self.assertTrue(all(x['version_source'].startswith('GameAgentKit bundle') for a in data['agents'] for x in a['skills']))

    def test_all_alias_installs_and_verifies_the_same_four_agents(self):
        installation = self.install('all')
        self.assertIn('PASS | 4 agents | 60/60 Skill links', installation.stdout)
        result = self.run_drui('verify')
        self.assertIn('PASS | 4 agents | 60/60 Skill links', result.stdout)
        self.assertEqual(len(result.stdout.strip().splitlines()), 1)

    def test_compact_cli_is_one_line_and_preserves_verbose_and_json(self):
        self.install('codex')
        clean = self.run_drui('verify', '--agents', 'codex').stdout.strip().splitlines()
        self.assertEqual(len(clean), 1, clean)
        self.assertIn('PASS | 1 agent | 12/12 Skill links', clean[0])
        self.assertIn('runtime untested', clean[0])
        verbose = self.run_drui('verify', '--agents', 'codex', '--verbose').stdout
        self.assertIn('[codex] 12/12 installed slots', verbose)
        self.assertIn('oil-ui-plus', verbose)
        assert self.run_drui('verify', '--agents', 'codex', '--json').stdout.startswith('{')

        # Missing links trigger nonzero exit and at most three failure entries.
        broken = self.home / '.agents' / 'skills' / 'game-audio'
        broken.unlink()
        bad = self.run_drui('verify', '--agents', 'codex', expected=1)
        self.assertIn('FAIL', bad.stdout)
        self.assertIn('game-audio:MISSING', bad.stdout)
        self.assertLessEqual(len(bad.stdout.strip().splitlines()), 2)
        self.assertFalse(broken.exists())


    def test_missing_and_broken_links_fail_and_do_not_repair(self):
        self.install('codex')
        missing = self.home / '.agents' / 'skills' / 'game-audio'
        missing.unlink()
        linked = self.home / '.agents' / 'skills' / 'gameplay-design'
        linked.unlink()
        linked.symlink_to(self.home / 'no-such-skill', target_is_directory=True)
        check = self.run_drui('verify', '--agents', 'codex', '--json', expected=1)
        report = json.loads(check.stdout)
        statuses = {x['name']: x['status'] for x in report['agents'][0]['skills']}
        self.assertEqual(statuses['game-audio'], 'MISSING')
        self.assertEqual(statuses['gameplay-design'], 'BROKEN')
        self.assertFalse(report['summary']['complete'])
        self.assertFalse(missing.exists())
        self.assertTrue(linked.is_symlink())

    def test_user_owned_same_name_collides_and_is_preserved(self):
        target = self.home / '.claude' / 'skills' / 'oil-ui-plus'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('custom user version')
        install_result = self.install('claude', expected=1)
        self.assertIn('FAIL', install_result.stdout)
        report = json.loads(self.run_drui('verify', '--agents', 'claude', '--json', expected=1).stdout)
        row = next(x for x in report['agents'][0]['skills'] if x['name'] == 'oil-ui-plus')
        self.assertEqual(row['status'], 'COLLISION')
        self.assertEqual((target / 'SKILL.md').read_text(), 'custom user version')

    def test_extra_user_skills_report_declared_version_or_unknown(self):
        self.install('cursor')
        root = self.home / '.cursor' / 'skills'
        own = root / 'third-party-review'
        own.mkdir()
        (own / 'SKILL.md').write_text('---\nname: third-party-review\nversion: 2.3.4\n---\nRead-only\n')
        other = root / 'my-local-skill'
        other.mkdir()
        (other / 'SKILL.md').write_text('---\nname: my-local-skill\n---\n')
        report = json.loads(self.run_drui('verify', '--agents', 'cursor', '--json').stdout)
        versions = {x['name']: x['version'] for x in report['agents'][0]['external']}
        self.assertEqual(versions['third-party-review'], '2.3.4')
        self.assertIsNone(versions['my-local-skill'])
        self.assertTrue(report['summary']['complete'])

    def test_project_local_shadow_warns_without_claiming_agent_load(self):
        self.install('codex')
        project = Path(self.workspace.name) / 'project'
        shadow = project / '.agents' / 'skills' / 'game-qa-review'
        shadow.mkdir(parents=True)
        (shadow / 'SKILL.md').write_text('user override')
        report = json.loads(self.run_drui('verify', '--agents', 'codex', '--project', str(project), '--json').stdout)
        self.assertTrue(report['warnings'])
        self.assertIn('may shadow', ' '.join(report['warnings']))
        self.assertIn('NOT TESTED', report['verification'])

    def test_rejects_symlinked_agent_parent_without_outside_writes(self):
        outside = Path(self.workspace.name) / 'outside-skills'
        outside.mkdir()
        agent_root = self.home / '.agents'
        agent_root.symlink_to(outside, target_is_directory=True)
        proc = self.install('codex', expected=1)
        self.assertIn('Unsafe symlinked Skill destination parent', proc.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertTrue(agent_root.is_symlink())
        self.assertFalse((outside / 'skills').exists())

    def test_copy_option_fails_before_any_install_or_link_writes(self):
        proc = subprocess.run([sys.executable, str(SOURCE / 'gamekit.py'),
                               'install', '--root', str(self.root), '--agents', 'codex',
                               '--copy'], env=self.env, text=True,
                              capture_output=True, timeout=15)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('--copy is unsupported', proc.stderr)
        self.assertFalse(self.root.exists())
        self.assertFalse((self.home / '.agents').exists())
        # Existing healthy install remains unaffected by a rejected link --copy.
        self.install('codex')
        link = self.home / '.agents' / 'skills' / 'drui'
        before = link.readlink()
        proc = subprocess.run([sys.executable, str(self.root / 'gamekit.py'),
                               'link', '--root', str(self.root), '--agents', 'codex', '--copy'],
                              env=self.env, text=True, capture_output=True, timeout=15)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(link.readlink(), before)

    def test_dry_run_never_provisions_or_claims_success(self):
        proc = subprocess.run([sys.executable, str(SOURCE / 'gamekit.py'), 'install', '--root', str(self.root),
                               '--agents', 'cursor', '--dry-run'], capture_output=True,
                              env=self.env, text=True, timeout=20)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn('DRUI Skill verification', proc.stdout)
        self.assertFalse(self.root.exists())
        self.assertFalse((self.home / '.cursor').exists())

    def test_cli_conflict_is_reported_even_when_skills_linked(self):
        cli = self.home / '.local' / 'bin' / 'drui'
        cli.parent.mkdir(parents=True)
        cli.write_text('existing command')
        install_result = self.install('codex', expected=1)
        self.assertIn('FAIL', install_result.stdout)
        report = json.loads(self.run_drui('verify', '--agents', 'codex', '--json', expected=1).stdout)
        self.assertEqual(report['cli']['status'], 'COLLISION')
        self.assertEqual(report['summary']['installed'], 12)
        self.assertFalse(report['summary']['complete'])
        self.assertEqual(cli.read_text(), 'existing command')


if __name__ == '__main__':
    unittest.main()
