"""Guard public docs against broken links, stale installation tags and release drift."""
from __future__ import annotations
import posixpath
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = (
    "README.md", "QUICKSTART.md", "docs/INSTALL_AND_VERIFY.md",
    "docs/DRUI_USAGE.md", "docs/DRUI_REVIEW_CHEATSHEET_ZH.md",
)


class DocsConsistencyTests(unittest.TestCase):
    def test_active_clone_examples_match_release_version(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        for filename in ACTIVE:
            text = (ROOT / filename).read_text(encoding="utf-8")
            examples = re.findall(r"git clone[^\n]*?\b(v\d+\.\d+\.\d+)\b", text)
            self.assertTrue(examples, (filename, "no tagged clone example"))
            for tag in examples:
                self.assertEqual(tag, "v" + version, (filename, tag))
        cli = (ROOT / "gamekit.py").read_text(encoding="utf-8")
        self.assertIn(f'VERSION = "{version}"', cli)
        publisher = (ROOT / ".github/workflows/publish.yml").read_text()
        self.assertIn(f'test "$(cat VERSION)" = "{version}"', publisher)

    def test_install_and_verify_agent_scopes_are_consistent(self):
        src = (ROOT / "gamekit.py").read_text()
        self.assertIn('"all": "codex,claude,antigravity,cursor"', src)
        for filename in ACTIVE:
            text = (ROOT / filename).read_text()
            self.assertNotIn("旧别名 `--agents all` 不含 Cursor", text)
            self.assertNotIn("legacy `--agents all`", text)

    def test_internal_changelogs_are_marked_archived(self):
        history = sorted((ROOT / "docs").glob("CHANGELOG_v*.md"))
        self.assertGreaterEqual(len(history), 6)
        for file in history:
            with self.subTest(file=file.name):
                self.assertTrue(file.read_text(encoding="utf-8").startswith("> ARCHIVED"), file)

    def test_all_documentation_local_markdown_links_resolve(self):
        docs = [p for p in ROOT.glob("*.md")] + list((ROOT / "docs").rglob("*.md"))
        self.assertGreater(len(docs), 15)
        errors = []
        for file in docs:
            text = file.read_text(encoding="utf-8")
            for url in re.findall(r"\]\(([^)\s]+)(?:\s+[\"'][^)]*[\"'])?\)", text):
                if url.startswith(("http:", "https:", "mailto:", "#", "data:")):
                    continue
                local = unquote(url.split("#", 1)[0])
                if not local or local.startswith("/"):
                    continue
                # Relative to containing document, not to repository root.
                location = (file.parent / local).resolve()
                if not location.is_relative_to(ROOT.resolve()) or not location.exists():
                    errors.append((str(file.relative_to(ROOT)), url))
        self.assertFalse(errors, "Broken local Markdown links: " + repr(errors))

    def test_source_only_release_no_legacy_zip_publisher(self):
        workflows = ROOT / ".github/workflows"
        self.assertFalse((workflows / "publish-v1.0.0.yml").exists())
        publisher = (workflows / "publish.yml").read_text()
        self.assertIn('TAG="v$(cat VERSION)"', publisher)
        self.assertNotIn("dist/GameAgentKit", publisher)
        self.assertIn("gh release create", publisher)

    def test_contributor_docs_match_automatic_release(self):
        contributor = (ROOT / "CONTRIBUTING.md").read_text()
        self.assertIn("publish.yml", contributor)
        self.assertIn("Do not manually push", contributor)
        self.assertIn("docs/MAINTENANCE.md", contributor)
        security = (ROOT / "SECURITY.md").read_text()
        self.assertIn("Git", security)
        self.assertIn("cannot prove", security.lower() if "cannot prove" in security.lower() else
                      security.lower().replace("it cannot prove", "cannot prove"))
        for filename in ACTIVE:
            self.assertNotIn("git clone --branch v1.3.0", (ROOT / filename).read_text())

if __name__ == "__main__":
    unittest.main()
