"""Offline verification of GitHub updater: no requests reach the network."""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts import github_update as u


def bundle(version="1.6.1", bad_name=None, symlink=False):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr("GameAgentKit/VERSION", version + '\n')
        z.writestr("GameAgentKit/gamekit.py", "# safe placeholder\n")
        z.writestr("GameAgentKit/scripts/drui", "#!/usr/bin/env python3\n")
        if bad_name:
            info = zipfile.ZipInfo(bad_name)
            if symlink:
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, b"contents")
    return out.getvalue()


class GitHubReleaseUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='drui-public-test-')
        self.root = Path(self.tmp.name) / 'GameAgentKit'
        self.root.mkdir()
        (self.root / 'VERSION').write_text('1.6.0\n')
        (self.root / 'gamekit.py').write_text('original installer\n')

    def tearDown(self):
        self.tmp.cleanup()

    def test_normalize_repo_rejects_bad_values(self):
        for bad in ('', '../bad', 'x/', 'a/b/c', 'https://github.com/a/b', 'a/b?token=secret'):
            with self.assertRaises(RuntimeError):
                u.normalize_repo(bad)
        self.assertEqual(u.normalize_repo('user/game-agent-kit'), 'user/game-agent-kit')

    def test_validate_archive_rejects_traversal(self):
        with self.assertRaisesRegex(RuntimeError, 'Unsafe ZIP path'):
            u.validate_zip(bundle(bad_name='GameAgentKit/../../.ssh/id_rsa'), 'v1.6.1', self.root)

    def test_validate_archive_rejects_symlink(self):
        with self.assertRaisesRegex(RuntimeError, 'Unsupported ZIP entry'):
            u.validate_zip(bundle(bad_name='GameAgentKit/skills/evil', symlink=True), 'v1.6.1', self.root)

    def test_validate_archive_requires_matching_version(self):
        with self.assertRaisesRegex(RuntimeError, 'VERSION mismatch'):
            u.validate_zip(bundle('0.0.1'), 'v1.6.1', self.root)

    def test_config_is_pinned_and_cannot_switch(self):
        u.save_repo(self.root, 'user/game-agent-kit')
        self.assertEqual(u.configured_repo(self.root), 'user/game-agent-kit')
        u.save_repo(self.root, 'user/game-agent-kit')
        with self.assertRaisesRegex(RuntimeError, 'pinned'):
            u.save_repo(self.root, 'other/game-agent-kit')

    def test_check_only_does_not_download_or_write(self):
        release = {"tag_name": "v1.6.1", "assets": [
            {"name": "GameAgentKit-v1.6.1.zip", "browser_download_url": "https://github.com/user/repo/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip"},
            {"name": "GameAgentKit-v1.6.1.zip.sha256", "browser_download_url": "https://github.com/user/repo/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip.sha256"}]}
        with patch.object(u, '_json', return_value=release), patch.object(u, '_request', side_effect=AssertionError('unexpected download')):
            status = u.update(root=self.root, repo='user/repo', check=True)
        self.assertEqual(status, 'available')
        self.assertFalse(u.source_config_path(self.root).exists())
        self.assertEqual((self.root / 'VERSION').read_text(), '1.6.0\n')

    def test_requires_explicit_yes(self):
        release = {"tag_name": "v1.6.1", "assets": [
            {"name": "GameAgentKit-v1.6.1.zip", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip"},
            {"name": "GameAgentKit-v1.6.1.zip.sha256", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip.sha256"}]}
        with patch.object(u, '_json', return_value=release), patch.object(u, '_request', side_effect=AssertionError('download not permitted')):
            with self.assertRaisesRegex(RuntimeError, '--yes'):
                u.update(root=self.root, repo='a/b')

    def test_verified_update_and_restore_pinned_source(self):
        data = bundle()
        sha = hashlib.sha256(data).hexdigest()
        release = {"tag_name": "v1.6.1", "assets": [
            {"name": "GameAgentKit-v1.6.1.zip", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip"},
            {"name": "GameAgentKit-v1.6.1.zip.sha256", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip.sha256"}]}
        calls=[]
        def fake_request(url, *, limit):
            if url.endswith('.sha256'):
                return f'{sha}  GameAgentKit-v1.6.1.zip\n'.encode()
            if url.endswith('.zip'):
                return data
            self.fail('unexpected URL')
        def callback(args):
            calls.append(args)
            self.assertEqual(Path(args.source, 'VERSION').read_text().strip(), '1.6.1')
            shutil.copy2(Path(args.source, 'VERSION'), self.root / 'VERSION')
        with patch.object(u, '_json', return_value=release), patch.object(u, '_request', side_effect=fake_request):
            result = u.update(root=self.root, repo='a/b', yes=True, upgrade_callback=callback)
        self.assertEqual(result, 'updated')
        self.assertEqual((self.root / 'VERSION').read_text().strip(), '1.6.1')
        self.assertEqual(u.configured_repo(self.root), 'a/b')
        self.assertEqual(len(calls),1)

    def test_bad_sha_blocks_upgrade(self):
        release = {"tag_name": "v1.6.1", "assets": [
            {"name": "GameAgentKit-v1.6.1.zip", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip"},
            {"name": "GameAgentKit-v1.6.1.zip.sha256", "browser_download_url": "https://github.com/a/b/releases/download/v1.6.1/GameAgentKit-v1.6.1.zip.sha256"}]}
        def fake_request(url, *, limit):
            return (b'0' * 64 + b'  GameAgentKit-v1.6.1.zip\n') if url.endswith('.sha256') else bundle()
        with patch.object(u, '_json', return_value=release), patch.object(u, '_request', side_effect=fake_request):
            with self.assertRaisesRegex(RuntimeError, 'SHA-256'):
                u.update(root=self.root, repo='a/b', yes=True, upgrade_callback=lambda _: self.fail('should not upgrade'))
        self.assertEqual((self.root / 'VERSION').read_text(), '1.6.0\n')


if __name__ == '__main__':
    unittest.main()
