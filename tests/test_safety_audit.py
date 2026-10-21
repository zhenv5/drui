"""Safety regression cases found during the DRUI public-release audit."""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from gamekit import cmd_upgrade
from scripts.dependency_guard import digest_skill


class SafetyAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='drui-safety-audit-')
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_release_source_update_has_no_zip_download(self):
        import inspect
        from scripts import github_update
        source = inspect.getsource(github_update)
        self.assertNotIn('zipfile', source)
        self.assertIn("'checkout'", source)
        self.assertIn("'fetch'", source)

    def test_nested_linked_asset_directory_is_not_silently_ignored(self):
        skill = self.base / 'custom-skill'
        skill.mkdir()
        (skill / 'SKILL.md').write_text('---\nname: custom-skill\n---\nhello')
        outside = self.base / 'assets'
        outside.mkdir()
        (outside / 'required.png').write_bytes(b'one')
        (skill / 'assets').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, 'linked directory'):
            digest_skill(skill)

    def fixture_upgrade(self):
        installed = self.base / 'old'
        incoming = self.base / 'new'
        installed.mkdir()
        incoming.mkdir()
        for name in ('gamekit.py', 'install.sh', 'VERSION', 'CHANGELOG.md'):
            (installed / name).write_text('old-' + name)
            (incoming / name).write_text('new-' + name)
        return installed, incoming

    def test_upgrade_updates_release_docs(self):
        root, src = self.fixture_upgrade()
        cmd_upgrade(SimpleNamespace(root=str(root), source=str(src), dry_run=False))
        self.assertEqual((root / 'CHANGELOG.md').read_text(), 'new-CHANGELOG.md')
        self.assertEqual((root / 'VERSION').read_text(), 'new-VERSION')
        backups = list((root / '.backups').rglob('CHANGELOG.md'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'old-CHANGELOG.md')

    def test_upgrade_does_not_modify_anything_if_preflight_fails(self):
        root, src = self.fixture_upgrade()
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'drui').write_text('unrelated')
        (root / 'scripts').symlink_to(outside, target_is_directory=True)
        (src / 'scripts').mkdir()
        (src / 'scripts' / 'drui').write_text('release')
        with self.assertRaisesRegex(RuntimeError, 'Unsafe linked'):
            cmd_upgrade(SimpleNamespace(root=str(root), source=str(src), dry_run=False))
        self.assertEqual((root / 'gamekit.py').read_text(), 'old-gamekit.py')
        self.assertEqual((outside / 'drui').read_text(), 'unrelated')

    def test_upgrade_rolls_back_on_normal_write_failure(self):
        root, src = self.fixture_upgrade()
        real = shutil.copyfileobj
        calls = [0]
        def fail_second(fin, fout, *args, **kwargs):
            calls[0] += 1
            if calls[0] == 2:
                raise OSError('simulated disk error')
            return real(fin, fout, *args, **kwargs)
        with patch('shutil.copyfileobj', side_effect=fail_second):
            with self.assertRaisesRegex(RuntimeError, 'changed files restored'):
                cmd_upgrade(SimpleNamespace(root=str(root), source=str(src), dry_run=False))
        for name in ('gamekit.py', 'install.sh', 'VERSION', 'CHANGELOG.md'):
            self.assertEqual((root / name).read_text(), 'old-' + name)
        self.assertFalse(list(root.rglob('*.gamekit-tmp')))


if __name__ == '__main__':
    unittest.main()
