"""GitHub-only installation documentation and shell error-propagation contracts."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("README.md", "QUICKSTART.md", "docs/INSTALL_AND_VERIFY.md")


def installer_snippet(filename):
    text = (ROOT / filename).read_text(encoding="utf-8")
    head = "DRUI_LOG=$(mktemp)"
    assert head in text, filename
    return head + text.split(head, 1)[1].split("\nfi", 1)[0] + "\nfi\n"


class DocsInstallContract(unittest.TestCase):
    def test_docs_point_to_canonical_guide(self):
        for filename in ("README.md", "QUICKSTART.md", "docs/MAINTENANCE.md",
                         "docs/DRUI_USAGE.md", "docs/DRUI_COMMANDS_ZH.md"):
            self.assertIn("INSTALL_AND_VERIFY.md",
                          (ROOT / filename).read_text(encoding="utf-8"), filename)
        guide = (ROOT / "docs/INSTALL_AND_VERIFY.md").read_text(encoding="utf-8")
        for word in ("60/60", "--verbose", "--json", "deps lock", "runtime untested",
                     "git clone", "verify", "COLLISION"):
            self.assertIn(word, guide)
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("Git", security)
        self.assertNotIn("SHA-256 validates that the ZIP", security)

    def test_install_snippets_are_valid_shell(self):
        for filename in DOCS:
            with self.subTest(filename=filename):
                script = installer_snippet(filename)
                result = subprocess.run(["bash", "-n"], input=script,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('"$HOME/GameAgentKit/scripts/drui" verify', script)

    def test_install_snippets_propagate_install_and_verify_errors(self):
        for filename in DOCS:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                root = home / "GameAgentKit"
                (root / "scripts").mkdir(parents=True)
                installer = root / "install.sh"
                installer.write_text('#!/bin/bash\necho "install log"\nexit "$FAKE_INSTALL_EXIT"\n')
                verifier = root / "scripts" / "drui"
                verifier.write_text('#!/bin/bash\necho "DRUI test PASS | 60/60"\nexit "$FAKE_VERIFY_EXIT"\n')
                verifier.chmod(0o755)
                script = installer_snippet(filename)
                env = dict(os.environ, HOME=tmp, TMPDIR=tmp)
                def run(install_status, verify_status):
                    return subprocess.run(["bash", "-c", script],
                                          capture_output=True, text=True, timeout=10,
                                          env=dict(env, FAKE_INSTALL_EXIT=str(install_status),
                                                   FAKE_VERIFY_EXIT=str(verify_status)))
                ok = run(0, 0)
                self.assertEqual(ok.returncode, 0, ok.stderr)
                self.assertEqual(ok.stdout.strip().splitlines(), ["DRUI test PASS | 60/60"])
                failed_install = run(17, 0)
                self.assertNotEqual(failed_install.returncode, 0)
                self.assertNotIn("PASS", failed_install.stdout)
                self.assertIn("install log", failed_install.stderr)
                failed_verify = run(0, 23)
                self.assertNotEqual(failed_verify.returncode, 0)


if __name__ == "__main__":
    unittest.main()
