"""GitHub-source-only updates, exercised with real local Git commits and tags."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import github_update as u


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


class GitSourceUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / 'repo'
        self.source.mkdir()
        git(self.source, 'init')
        git(self.source, 'config', 'user.name', 'Fixture')
        git(self.source, 'config', 'user.email', 'test@example.com')
        (self.source / 'scripts').mkdir()
        (self.source / 'scripts/drui').write_text('#!/usr/bin/env python3\nprint("DRUI")\n')
        (self.source / '.gitignore').write_text('.state/\n')
        (self.source / 'VERSION').write_text('1.2.1\n')
        git(self.source, 'add', '.')
        git(self.source, 'commit', '-m', 'old version')
        git(self.source, 'tag', 'v1.2.1')
        (self.source / 'VERSION').write_text('1.3.0\n')
        git(self.source, 'add', '.')
        git(self.source, 'commit', '-m', 'new version')
        git(self.source, 'tag', 'v1.3.0')
        self.root = self.base / 'installed'
        subprocess.run(['git', 'clone', '-q', '--branch', 'v1.2.1', str(self.source), str(self.root)], check=True)
        self.old_sha = git(self.root, 'rev-parse', 'HEAD')
        self.run_real = u._run

    def tearDown(self):
        self.tmp.cleanup()

    def local_runner(self, root, *args, **kwargs):
        # The production source transport forbids file:// and local path remotes.
        # Only replace that transport option in the isolated local-Git fixture.
        if args[:2] == ('-c', 'protocol.file.allow=never'):
            args = args[2:]
        return self.run_real(root, *args, **kwargs)

    def wrapped(self, **options):
        with patch.object(u, '_verify_root', return_value=None), \
             patch.object(u, '_latest_tag', return_value='v1.3.0'), \
             patch.object(u, '_run', side_effect=self.local_runner):
            return u.update(root=self.root, **options)

    def test_only_official_repository_allowed(self):
        with self.assertRaisesRegex(RuntimeError, 'official'):
            u.normalize_repo('attacker/drui')
        self.assertEqual(u.normalize_repo('zhenv5/drui'), 'zhenv5/drui')

    def test_reject_non_clone_or_malicious_origin(self):
        with self.assertRaisesRegex(RuntimeError, 'Git checkout'):
            u.update(root=self.base, check=True)
        with self.assertRaisesRegex(RuntimeError, 'Untrusted Git origin'):
            u.update(root=self.root, check=True)

    def test_check_does_not_write_or_fetch(self):
        self.assertEqual(self.wrapped(check=True), 'available')
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)
        self.assertEqual((self.root / 'VERSION').read_text(), '1.2.1\n')
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)

    def test_yes_required(self):
        with self.assertRaisesRegex(RuntimeError, '--yes'):
            self.wrapped()
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)

    def test_real_git_tag_checkout(self):
        self.assertEqual(self.wrapped(yes=True), 'updated')
        self.assertEqual((self.root / 'VERSION').read_text().strip(), '1.3.0')
        self.assertNotEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)
        self.assertEqual(git(self.root, 'status', '--porcelain'), '')

    def test_dirty_checkout_refuses(self):
        (self.root / 'VERSION').write_text('secret local edits\n')
        with self.assertRaisesRegex(RuntimeError, 'local changes'):
            self.wrapped(yes=True)
        self.assertEqual((self.root / 'VERSION').read_text(), 'secret local edits\n')
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)

    def test_untracked_files_refuse_update(self):
        (self.root / 'personal_notes').write_text('do not touch')
        with self.assertRaisesRegex(RuntimeError, 'untracked'):
            self.wrapped(yes=True)
        self.assertTrue((self.root / 'personal_notes').exists())

    def test_local_state_ignored_and_preserved(self):
        (self.root / '.state').mkdir()
        (self.root / '.state/external-skills.lock.json').write_text('{"keep":true}')
        self.assertEqual(self.wrapped(yes=True), 'updated')
        self.assertEqual((self.root / '.state/external-skills.lock.json').read_text(), '{"keep":true}')

    def test_tag_with_bad_version_refuses_checkout(self):
        (self.source / 'VERSION').write_text('9.9.9\n')
        git(self.source, 'add', '.')
        git(self.source, 'commit', '-m', 'mismatch')
        git(self.source, 'tag', 'v1.4.0')
        with patch.object(u, '_verify_root', return_value=None), \
             patch.object(u, '_latest_tag', return_value='v1.4.0'), \
             patch.object(u, '_run', side_effect=self.local_runner):
            with self.assertRaisesRegex(RuntimeError, 'disagree'):
                u.update(root=self.root, yes=True)
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), self.old_sha)


if __name__ == '__main__':
    unittest.main()
