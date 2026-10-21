"""First-use CLI help/list contracts; all commands tested read-only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "drui"


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="drui-onboarding-")
        self.home = Path(self.tmp.name)
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(CLI), *args], text=True,
                                capture_output=True, env=self.env, timeout=10)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_zero_arg_help_and_start_are_genuinely_useful(self):
        for args in ((), ("help",), ("--help",), ("start",)):
            output = self.run_cli(*args).stdout
            self.assertIn("drui list --beginner", output)
            self.assertIn("drui prompt review-loop", output)
            self.assertIn("只打印", output)
            self.assertIn("Use the drui skill", output)
        self.assertIn("drui deps check", self.run_cli("start").stdout)
        self.assertFalse(list(self.home.iterdir()), "Help should never install anything")

    def test_catalog_has_stable_names_and_permissions(self):
        full = json.loads(self.run_cli("list", "--json").stdout)
        self.assertEqual(full["count"], full["total_count"])
        self.assertEqual(full["count"], 20)
        self.assertEqual(len(set(x["name"] for x in full["workflows"])), 20)
        for entry in full["workflows"]:
            self.assertIn(entry["category"], ("core", "ui", "specialty", "review"))
            self.assertTrue(entry["when"] and entry["output"] and entry["example"])
            self.assertTrue((ROOT / "prompts/drui/stages" / (entry["name"] + ".md")).is_file())

    def test_list_supports_beginner_category_search_and_machine_output(self):
        entries = json.loads(self.run_cli("list", "--beginner", "--json").stdout)
        self.assertEqual(entries["count"], 6)
        self.assertEqual({e["name"] for e in entries["workflows"]},
                         {"full", "visual-review", "usability-review", "game-feel", "review-triad", "review-loop"})
        filtered = json.loads(self.run_cli("list", "--category", "review", "--json").stdout)
        self.assertEqual(filtered["count"], 5)
        self.assertTrue(all(x["category"] == "review" for x in filtered["workflows"]))
        searched = json.loads(self.run_cli("list", "--search", "touch", "--json").stdout)
        self.assertIn("usability-review", {x["name"] for x in searched["workflows"]})
        empty = json.loads(self.run_cli("list", "--search", "no-such-query-xyzz", "--json").stdout)
        self.assertEqual(empty["count"], 0)
        self.assertEqual(empty["total_count"], 20)
        self.assertIn("没有匹配", self.run_cli("list", "--search", "no-such-query-xyzz").stdout)
        self.assertFalse(list(self.home.iterdir()))

    def test_gamekit_workflow_list_parity(self):
        cmd = [sys.executable, str(ROOT / "gamekit.py"), "workflow", "list", "--category", "ui", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, env=self.env, timeout=10, check=True)
        self.assertEqual(json.loads(result.stdout)["count"], 5)

    def test_workflow_help_tells_when_mode_result_and_execution_semantics(self):
        help_text = self.run_cli("help", "review-triad").stdout
        for keyword in ("REVIEW ONLY", "适用场景", "预期交付", "drui prompt review-triad", "PROVISIONAL"):
            self.assertIn(keyword, help_text)
        self.assertIn("MAY EDIT", self.run_cli("help", "review-loop").stdout)
        self.assertIn("不会自己执行", self.run_cli("help", "prompt").stdout)
        self.assertIn("不会静默升级", self.run_cli("help", "deps").stdout)

    def test_typos_are_actionable_and_invalid_filter_rejected(self):
        res = self.run_cli("review-lop", success=False)
        self.assertEqual(res.returncode, 2)
        self.assertIn("review-loop", res.stderr)
        res = self.run_cli("help", "review-lop", success=False)
        self.assertEqual(res.returncode, 2)
        self.assertIn("review-loop", res.stderr)
        self.assertNotEqual(self.run_cli("list", "--category", "random", success=False).returncode, 0)
        self.assertFalse(list(self.home.iterdir()))


if __name__ == "__main__":
    unittest.main()
