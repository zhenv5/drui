"""DRUI installation and update prompts must be copyable, stable and harmless."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "drui"
README = (ROOT / "README.md").read_text(encoding="utf-8")


class AgentSetupPromptTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="drui-agent-setup-")
        self.home = Path(self.folder.name)
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")

    def tearDown(self):
        self.folder.cleanup()

    def cli(self, *args, env=None):
        return subprocess.run([sys.executable, str(CLI), *args], capture_output=True,
                              text=True, env=env or self.env, timeout=10)

    def test_first_install_requires_no_drui_and_docs_match_exact_prompt(self):
        for action in ("install", "update"):
            prompt = (ROOT / "prompts" / "agent-setup" / f"{action}.txt").read_text()
            result = self.cli("agent", action)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, prompt)
            self.assertIn(f"```text\n{prompt.rstrip()}\n```", README)
            self.assertEqual(self.cli("agent-prompt", action).stdout, prompt)
            self.assertIn("github.com/zhenv5/drui", prompt)
            self.assertIn("SHA-256", prompt)
            self.assertIn("Skills", prompt)
        self.assertFalse(list(self.home.iterdir()))

    def test_clipboard_success_is_explicit_and_does_not_install(self):
        bindir = self.home / "bin"
        bindir.mkdir()
        paste = bindir / "pbcopy"
        marker = self.home / "clipboard.txt"
        # pbcopy stub is isolated under PATH; no system clipboard is touched.
        paste.write_text(f"#!/bin/sh\ncat > '{marker}'\n", encoding="utf-8")
        paste.chmod(0o755)
        env = dict(self.env, PATH=str(bindir) + ":/usr/bin:/bin")
        result = self.cli("copy", "update", env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Copied DRUI update Agent prompt", result.stdout)
        self.assertEqual(marker.read_text(), (ROOT / "prompts/agent-setup/update.txt").read_text())
        result = self.cli("agent", "install", "--copy", env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(marker.read_text(), (ROOT / "prompts/agent-setup/install.txt").read_text())
        self.assertFalse((self.home / "GameAgentKit").exists())

    def test_clipboard_absence_is_not_false_success(self):
        result = self.cli("copy", "update", env=dict(self.env, PATH="/no-such-tools"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Clipboard tool unavailable", result.stderr)
        self.assertIn("zhenv5/drui", result.stdout)

    def test_invalid_action_does_not_touch_files(self):
        result = self.cli("copy", "uninstall")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(list(self.home.iterdir()))
        for request in (("help",), ("help", "commands"), ("start",)):
            value = self.cli(*request)
            self.assertEqual(value.returncode, 0)
            self.assertTrue(("drui copy update" in value.stdout or "drui copy install" in value.stdout))


if __name__ == "__main__":
    unittest.main()
