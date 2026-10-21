"""First public-release naming and packaging contract."""
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class PublicReleaseTests(unittest.TestCase):
    def test_version_matches_core_and_cli(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "1.4.1")
        from gamekit import VERSION
        self.assertEqual(VERSION, "1.4.1")
        p = subprocess.run([sys.executable, str(ROOT / "scripts/drui"), "version"], capture_output=True, text=True, check=True)
        self.assertIn("DRUI / GameAgentKit v1.4.1", p.stdout)
        self.assertIn("Latest GitHub tag: NOT CHECKED", p.stdout)
    def test_release_pipeline_matches_current_version(self):
        version = (ROOT / "VERSION").read_text().strip()
        pipeline = (ROOT / ".github/workflows" / "publish.yml").read_text()
        self.assertIn(f'test "$(cat VERSION)" = "{version}"', pipeline)
        self.assertNotIn(".zip", pipeline)
        self.assertIn("TAG=\"v$(cat VERSION)\"", pipeline)
    def test_dependency_state_excluded_from_git(self):
        self.assertIn(".state/", (ROOT / ".gitignore").read_text())
    def test_release_has_exact_workflow_skill_counts(self):
        from gamekit import WORKFLOW_STAGES
        self.assertEqual(len(WORKFLOW_STAGES),20)
        self.assertEqual(len(list((ROOT / "skills").glob("*/SKILL.md"))),12)
