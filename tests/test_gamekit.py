import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


class GameAgentKitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gamekit-test-")
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.root = self.home / "GameAgentKit"
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")

    def tearDown(self):
        self.temp.cleanup()

    def call(self, script, *args, ok=True):
        proc = subprocess.run([sys.executable, str(script), *[str(v) for v in args]], env=self.env,
                              text=True, capture_output=True, timeout=30)
        if ok and proc.returncode:
            self.fail(f"Command failed: {proc.args}\nstdout={proc.stdout}\nstderr={proc.stderr}")
        return proc

    def install(self, agents="all"):
        return self.call(SOURCE / "gamekit.py", "install", "--root", self.root, "--agents", agents)

    def test_dry_run_install_writes_nothing(self):
        r = self.call(SOURCE / "gamekit.py", "install", "--root", self.root, "--agents", "all", "--dry-run")
        self.assertIn(str(self.root / "skills" / "game-qa-review"), r.stdout)
        self.assertFalse(self.root.exists())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_links_one_canonical_root(self):
        self.install()
        sources = [self.home / ".cursor/skills/game-qa-review",
                   self.home / ".agents/skills/game-qa-review",
                   self.home / ".claude/skills/game-qa-review",
                   self.home / ".gemini/config/skills/game-qa-review",
                   self.home / ".gemini/antigravity-cli/skills/game-qa-review"]
        for target in sources:
            self.assertTrue(target.is_symlink(), target)
            self.assertEqual(target.resolve(), self.root / "skills" / "game-qa-review")
        self.assertEqual(len(list((self.root / 'skills').iterdir())), 12)
        self.call(self.root / "gamekit.py", "doctor", "--root", self.root)

    def test_multi_project_profiles_do_not_duplicate_skills(self):
        self.install()
        p1, p2 = self.base / "game1", self.base / "game2"
        p1.mkdir(); p2.mkdir()
        self.call(self.root / "gamekit.py", "attach", "--root", self.root, "--project", p1,
                  "--name", "Space Puzzles", "--profile", "ios-swiftui")
        self.call(self.root / "gamekit.py", "attach", "--root", self.root, "--project", p2,
                  "--name", "Action Browser", "--profile", "web-game")
        self.assertIn("Space Puzzles", (p1 / ".game-agent-kit/PROFILE.md").read_text())
        self.assertIn("Browser game", (p2 / ".game-agent-kit/PROFILE.md").read_text())
        self.assertFalse((p1 / ".agents").exists())
        self.assertFalse((p2 / ".claude").exists())
        self.assertTrue((p1 / "AGENTS.md").exists())
        self.call(self.root / "gamekit.py", "doctor", "--root", self.root, "--project", p1)
        self.call(self.root / "gamekit.py", "doctor", "--root", self.root, "--project", p2)

    def test_existing_agent_instructions_preserved(self):
        self.install("codex")
        p = self.base / "existing_game"; p.mkdir()
        (p / "AGENTS.md").write_text("# My existing project rules\n")
        (p / "CLAUDE.md").write_text("# My existing Claude instructions\n")
        self.call(self.root / "gamekit.py", "attach", "--root", self.root, "--project", p)
        self.assertEqual((p / "AGENTS.md").read_text(), "# My existing project rules\n")
        self.assertEqual((p / "CLAUDE.md").read_text(), "# My existing Claude instructions\n")
        self.assertTrue((p / ".game-agent-kit/PROFILE.md").is_file())

    def test_link_conflict_preserved(self):
        existing = self.home / ".claude/skills/game-qa-review"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("# Custom skill")
        result = self.call(SOURCE / "gamekit.py", "install", "--root", self.root, "--agents", "claude", ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)
        self.assertEqual((existing / "SKILL.md").read_text(), "# Custom skill")

    def test_unlink_only_kit_owned_symlinks(self):
        self.install("codex,claude")
        personal = self.home / ".claude/skills/personal-skill"
        personal.mkdir(); (personal / "SKILL.md").write_text("my private skill")
        self.call(self.root / "gamekit.py", "unlink", "--root", self.root, "--agents", "all")
        self.assertTrue(self.root.is_dir())
        self.assertTrue(personal.exists())
        self.assertFalse((self.home / ".claude/skills/game-feel-polish").exists())
        self.assertFalse((self.home / ".agents/skills/game-feel-polish").exists())

    def test_upgrade_backups_and_custom_files(self):
        self.install("codex")
        (self.root / "README.md").write_text("user changes")
        custom = self.root / "skills/custom-quality/SKILL.md"
        custom.parent.mkdir(); custom.write_text("---\nname: custom-quality\ndescription: custom\n---\n")
        incoming = self.base / "incoming"
        shutil.copytree(SOURCE, incoming)
        (incoming / "README.md").write_text("v-next readme")
        dry = self.call(self.root / "gamekit.py", "upgrade", "--from", incoming, "--root", self.root, "--dry-run")
        self.assertIn("WOULD UPDATE", dry.stdout)
        self.assertEqual((self.root / "README.md").read_text(), "user changes")
        self.call(self.root / "gamekit.py", "upgrade", "--from", incoming, "--root", self.root)
        self.assertTrue(custom.exists())
        self.assertEqual((self.root / "README.md").read_text(), "v-next readme")
        self.assertTrue(any(f.read_text() == "user changes" for f in (self.root / ".backups").rglob("README.md")))

    def test_attach_existing_config_not_overwritten(self):
        self.install('codex')
        p = self.base / 'game'; p.mkdir()
        self.call(self.root / 'gamekit.py', 'attach', '--root', self.root, '--project', p, '--profile', 'puzzle')
        second = self.call(self.root / 'gamekit.py', 'attach', '--root', self.root, '--project', p, '--profile', 'generic', ok=False)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn('puzzle', (p / '.game-agent-kit/config.json').read_text())

    def test_custom_skill_global_relink(self):
        self.install('all')
        ext = self.root / 'skills/my-arcade-procedure'
        ext.mkdir()
        (ext / 'SKILL.md').write_text('---\nname: my-arcade-procedure\ndescription: custom\n---\n')
        self.call(self.root / 'gamekit.py', 'link', '--agents', 'all', '--root', self.root)
        self.assertTrue((self.home / '.agents/skills/my-arcade-procedure').is_symlink())
        self.assertTrue((self.home / '.gemini/config/skills/my-arcade-procedure').is_symlink())

    def make_external_oil(self):
        source = self.base / "existing_oil_ui"
        source.mkdir(exist_ok=True)
        (source / "SKILL.md").write_text("---\nname: oil-ui\ndescription: user's already owned UI skill\n---\n# Oil UI\n")
        return source

    def test_register_external_dry_run_leaves_original_and_targets_untouched(self):
        self.install('codex')
        source = self.make_external_oil()
        before = (source / "SKILL.md").read_bytes()
        self.call(self.root / "gamekit.py", "register-external", "--name", "oil-ui", "--source", source,
                  "--agents", "all", "--dry-run")
        self.assertFalse((self.home / ".agents/skills/oil-ui").exists())
        self.assertEqual((source / "SKILL.md").read_bytes(), before)

    def test_register_external_shares_one_existing_skill_to_all_agents(self):
        self.install()
        source = self.make_external_oil()
        self.call(self.root / "gamekit.py", "register-external", "--name", "oil-ui", "--source", source,
                  "--agents", "all")
        for folder in [".agents/skills", ".claude/skills", ".gemini/config/skills", ".gemini/antigravity-cli/skills"]:
            target = self.home / folder / "oil-ui"
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), source.resolve())
        self.assertTrue((self.home / '.agents/skills/drui/SKILL.md').is_file())
        self.call(self.root / "gamekit.py", "doctor", "--root", self.root, "--agents", "all")

    def test_register_external_preserves_preexisting_conflict(self):
        self.install('codex,claude')
        source = self.make_external_oil()
        original = self.home / ".claude/skills/oil-ui"
        original.mkdir(parents=True)
        (original / "SKILL.md").write_text("personal copy")
        result = self.call(self.root / "gamekit.py", "register-external", "--name", "oil-ui", "--source", source,
                           "--agents", "codex,claude")
        self.assertIn("conflicts kept intact", result.stdout)
        self.assertTrue((self.home / ".agents/skills/oil-ui").is_symlink())
        self.assertEqual((original / "SKILL.md").read_text(), "personal copy")

    def test_unregister_external_only_removes_matching_links(self):
        self.install('all')
        source = self.make_external_oil()
        self.call(self.root / "gamekit.py", "register-external", "--name", "oil-ui", "--source", source)
        other = self.base / "another_oil_ui"; other.mkdir()
        (other / "SKILL.md").write_text("---\nname: oil-ui\ndescription: an alternate\n---\n")
        result = self.call(self.root / "gamekit.py", "unregister-external", "--name", "oil-ui", "--source", other)
        self.assertIn("Removed/previewed 0", result.stdout)
        self.assertTrue((self.home / ".agents/skills/oil-ui").is_symlink())
        self.call(self.root / "gamekit.py", "unregister-external", "--name", "oil-ui", "--source", source)
        self.assertFalse((self.home / ".agents/skills/oil-ui").exists())
        self.assertTrue((source / "SKILL.md").exists())

    def test_register_external_rejects_bad_skill_without_modifying_anything(self):
        self.install('codex')
        bad = self.base / "bad"; bad.mkdir()
        (bad / "SKILL.md").write_text("---\nname: something-else\ndescription: fake\n---\n")
        failed = self.call(self.root / "gamekit.py", "register-external", "--name", "oil-ui", "--source", bad, ok=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertFalse((self.home / ".agents/skills/oil-ui").exists())

    def test_upgrade_includes_oil_ui_prompts_examples_and_skill(self):
        self.install('codex')
        src = self.base / "source-new"
        shutil.copytree(SOURCE, src)
        self.call(self.root / "gamekit.py", "upgrade", "--from", src, "--root", self.root)
        self.assertTrue((self.root / "prompts/drui/MINIGAME_SCENE_QA.md").is_file())
        self.assertTrue((self.root / "examples/OilUICardGallery.swift").is_file())
        self.assertTrue((self.root / "skills/drui/SKILL.md").is_file())

    def test_extend_oil_ui_opt_in_preserves_existing_text_and_backups(self):
        self.install('codex')
        source = self.make_external_oil()
        original = (source / 'SKILL.md').read_text()
        self.call(self.root / 'gamekit.py', 'extend-oil-ui', '--source', source,
                  '--root', self.root, '--dry-run')
        self.assertEqual((source / 'SKILL.md').read_text(), original)
        self.assertFalse(list(source.glob('SKILL.md.gamekit-backup-*')))
        self.call(self.root / 'gamekit.py', 'extend-oil-ui', '--source', source,
                  '--root', self.root)
        extended = (source / 'SKILL.md').read_text()
        self.assertTrue(extended.startswith(original))
        self.assertIn('OIL_UI_REVIEW_RUBRIC.md', extended)
        backups = list(source.glob('SKILL.md.gamekit-backup-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), original)
        self.call(self.root / 'gamekit.py', 'extend-oil-ui', '--source', source,
                  '--root', self.root)
        self.assertEqual((source / 'SKILL.md').read_text(), extended)
        self.assertEqual(len(list(source.glob('SKILL.md.gamekit-backup-*'))), 1)

    def test_oil_ui_original_prompts_and_19_card_library_present(self):
        prompt = SOURCE / 'prompts/OIL_UI_ENHANCED_WORKFLOW.md'
        patterns = SOURCE / 'references/OIL_UI_19_ORIGINAL_CARD_PATTERNS.md'
        self.assertTrue(prompt.is_file())
        self.assertTrue((SOURCE / 'examples/OilUICardGallery.swift').is_file())
        self.assertTrue((SOURCE / 'examples/OilUIEffectsGallery.swift').is_file())
        import re
        ids = re.findall(r'^\| (\d{2}) \|', patterns.read_text(), re.M)
        self.assertEqual(len(ids), 19)
        self.assertEqual(ids[0], '01')
        self.assertEqual(ids[-1], '19')

    def test_workflow_list_has_all_individual_stages(self):
        output = self.call(SOURCE / 'gamekit.py', 'workflow', 'list').stdout
        for stage in ('full', 'discover', 'plan', 'implement', 'visual-review',
                      'usability-review', 'game-feel', 'fix', 'verify',
                      'screenshot-rebuild', 'component-polish', 'mini-game-scene',
                      'effects', 'dashboard', 'art-3d', 'review-tl', 'review-pm', 'review-user', 'review-triad', 'review-loop'):
            self.assertIn(stage, output)
        self.assertFalse(self.root.exists())  # no install or mutations needed

    def test_workflow_each_prompt_contains_scope_and_output_contract(self):
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location('gamekit', SOURCE / 'gamekit.py')
        gamekit = module_from_spec(spec)
        spec.loader.exec_module(gamekit)
        for stage in gamekit.WORKFLOW_STAGES:
            out = self.call(SOURCE / 'gamekit.py', 'workflow', 'prompt',
                            '--stage', stage, '--root', SOURCE).stdout
            self.assertIn('drui', out)
            self.assertIn(f'Stage: {stage}', out)
            self.assertIn('Output contract', out)
            self.assertIn('NOT RUN', out)

    def test_workflow_prompt_is_read_only_by_default_and_project_aware(self):
        project = self.base / 'new game'; project.mkdir()
        output = self.call(SOURCE / 'gamekit.py', 'workflow', 'prompt',
                           '--stage', 'visual-review', '--project', project,
                           '--root', SOURCE).stdout
        self.assertIn(str(project), output)
        self.assertIn('READ-ONLY', output)
        self.assertIn('BLOCKED', output)
        self.assertEqual(list(project.iterdir()), [])

    def test_workflow_prompt_output_protects_existing_file(self):
        target = self.base / 'stage.md'
        target.write_text('user content', encoding='utf-8')
        blocked = self.call(SOURCE / 'gamekit.py', 'workflow', 'prompt',
                            '--stage', 'mini-game-scene', '--output', target,
                            '--root', SOURCE, ok=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(target.read_text(), 'user content')
        self.call(SOURCE / 'gamekit.py', 'workflow', 'prompt', '--stage',
                  'mini-game-scene', '--output', target, '--root', SOURCE, '--force')
        self.assertIn('mini-game-scene', target.read_text())

    def test_upgrade_from_v11_includes_new_stage_prompts(self):
        # Simulate a v1.1 CLI upgrading an existing install from v1.3 staging;
        # directory parent 'prompts' was already whitelisted by the old upgrader.
        old_script = Path('/mnt/data/GameAgentKit_oilui_work/GameAgentKit/gamekit.py')
        if not old_script.is_file():
            self.skipTest('Source v1.1 archive not available in test environment')
        old_root = self.base / 'legacy'
        shutil.copytree(old_script.parent, old_root, ignore=shutil.ignore_patterns('__pycache__'))
        self.call(old_script, 'upgrade', '--from', SOURCE, '--root', old_root)
        self.assertTrue((old_root / 'prompts/drui/stages/visual-review.md').is_file())
        self.assertIn('1.4.0', (old_root / 'VERSION').read_text())
        out = self.call(old_root / 'gamekit.py', 'workflow', 'list').stdout
        self.assertIn('visual-review', out)

    def test_drui_skill_is_single_container_with_fifteen_independent_stages(self):
        skill = SOURCE / 'skills/drui/SKILL.md'
        self.assertIn('name: drui', skill.read_text())
        self.assertFalse((SOURCE / 'skills/oil-ui-enhanced-review').exists())
        self.assertEqual(len(list((SOURCE / 'prompts/drui/stages').glob('*.md'))), 20)
        self.assertIn('DRUI', self.call(SOURCE / 'gamekit.py', 'workflow', 'list').stdout)

    def make_legacy(self):
        """Simulate v1.2 canonical skill plus its links on an already v1.3 kit."""
        legacy = self.root / 'skills/oil-ui-enhanced-review'
        legacy.mkdir()
        (legacy / 'SKILL.md').write_text('---\nname: oil-ui-enhanced-review\ndescription: old shared skill\n---\n', encoding='utf-8')
        for rel in ('.agents/skills', '.claude/skills', '.gemini/config/skills',
                    '.gemini/antigravity-cli/skills', '.cursor/skills'):
            dest = self.home / rel / 'oil-ui-enhanced-review'
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(legacy, target_is_directory=True)
        return legacy

    def test_migrate_drui_dry_run_and_real_idempotent(self):
        self.install()
        legacy = self.make_legacy()
        own_file = legacy / 'user-note.txt'
        own_file.write_text('keep me')
        oil = self.make_external_oil()
        self.call(self.root / 'gamekit.py', 'register-external', '--name', 'oil-ui', '--source', oil,
                  '--agents', 'all')
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root, '--dry-run')
        self.assertTrue(legacy.exists())
        self.assertTrue((self.home / '.agents/skills/oil-ui-enhanced-review').is_symlink())
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root)
        self.assertFalse(legacy.exists())
        for rel in ('.agents/skills', '.claude/skills', '.gemini/config/skills',
                    '.gemini/antigravity-cli/skills', '.cursor/skills'):
            self.assertFalse((self.home / rel / 'oil-ui-enhanced-review').is_symlink())
        self.assertTrue(any(f.read_text() == 'keep me' for f in (self.root / '.backups').rglob('user-note.txt')))
        self.assertTrue((self.home / '.agents/skills/drui/SKILL.md').exists())
        self.assertTrue((self.home / '.agents/skills/oil-ui/SKILL.md').exists())
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root)

    def test_migrate_drui_preserves_foreign_skill_and_user_copy(self):
        self.install('codex')
        legacy = self.root / 'skills/oil-ui-enhanced-review'; legacy.mkdir()
        (legacy / 'SKILL.md').write_text('---\nname: my-private-skill\n---\n')
        other = self.home / '.agents/skills/oil-ui-enhanced-review'; other.mkdir(parents=True)
        (other / 'SKILL.md').write_text('my custom')
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root)
        self.assertTrue(legacy.exists())
        self.assertEqual((other / 'SKILL.md').read_text(), 'my custom')

    def test_migrate_drui_refreshes_only_managed_project_blocks(self):
        self.install('codex')
        project = self.base / 'Game'; project.mkdir()
        old_block = '<!-- GameAgentKit: begin (managed) -->\nUse oil-ui-enhanced-review.\n<!-- GameAgentKit: end (managed) -->'
        before = '# My own rules\n' + old_block + '\nOther content must be preserved\n'
        for f in ['AGENTS.md', 'CLAUDE.md']:
            (project / f).write_text(before)
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root, '--project', project, '--dry-run')
        self.assertEqual((project / 'AGENTS.md').read_text(), before)
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root, '--project', project)
        for f in ['AGENTS.md', 'CLAUDE.md']:
            text = (project / f).read_text()
            self.assertIn('Use drui.', text)
            self.assertIn('My own rules', text)
            self.assertIn('Other content must be preserved', text)
            self.assertEqual((project / (f + '.drui-pre-migration.bak')).read_text(), before)
        self.call(self.root / 'gamekit.py', 'migrate-drui', '--root', self.root, '--project', project)

    def test_extend_oil_ui_refresh_updates_managed_legacy_block_only(self):
        self.install('codex')
        source = self.make_external_oil()
        path = source / 'SKILL.md'
        original = path.read_text()
        old = ('\n<!-- GameAgentKit Oil UI extension: BEGIN -->\n'
               'Use oil-ui-enhanced-review from the old kit\n'
               '<!-- GameAgentKit Oil UI extension: END -->\n')
        path.write_text(original + old)
        self.call(self.root / 'gamekit.py', 'extend-oil-ui', '--source', source,
                  '--root', self.root, '--dry-run', '--refresh')
        self.assertEqual(path.read_text(), original + old)
        self.call(self.root / 'gamekit.py', 'extend-oil-ui', '--source', source,
                  '--root', self.root, '--refresh')
        revised = path.read_text()
        self.assertIn('load the globally shared `drui`', revised)
        self.assertNotIn('oil-ui-enhanced-review', revised)
        self.assertTrue(revised.startswith(original))
        self.assertTrue(any(f.read_text() == original + old for f in source.glob('SKILL.md.gamekit-backup-*')))

    def test_skill_doc_names_trigger_and_stage_rules(self):
        text = (SOURCE / 'skills/drui/SKILL.md').read_text()
        self.assertIn('Stage: visual-review', text)
        self.assertIn('automatic activation', text)
        self.assertIn('not universal', text)
        for path in ('QUICKSTART.md', 'README.md', 'docs/DRUI_USAGE.md'):
            self.assertIn('git clone',
                          (SOURCE / path).read_text())


    def test_new_strict_reviewer_stages_are_independently_callable(self):
        for name in ('review-tl', 'review-pm', 'review-user', 'review-triad', 'review-loop'):
            output = self.call(SOURCE / 'gamekit.py', 'workflow', 'prompt', '--stage', name, '--root', SOURCE).stdout
            self.assertIn('Stage: ' + name, output)
            self.assertIn('drui', output)
        for name in ('review-tl', 'review-pm', 'review-user'):
            self.assertIn('READ-ONLY', (SOURCE / 'prompts/drui/stages' / (name + '.md')).read_text())

    def test_review_prepare_is_isolated_non_overwrite_and_dry_run_safe(self):
        p = self.base / 'Game'; p.mkdir()
        dest = self.base / 'review-r1'
        self.call(SOURCE / 'gamekit.py', 'review', 'prepare', '--project', p, '--output', dest,
                  '--root', SOURCE, '--dry-run')
        self.assertFalse(dest.exists())
        self.call(SOURCE / 'gamekit.py', 'review', 'prepare', '--project', p, '--output', dest,
                  '--root', SOURCE)
        self.assertTrue((dest / 'PROMPT_tech-lead.md').is_file())
        self.assertTrue((dest / 'PROMPT_product-manager.md').is_file())
        self.assertTrue((dest / 'PROMPT_end-user.md').is_file())
        self.assertIn(str(p), (dest / 'PROMPT_tech-lead.md').read_text())
        r = self.call(SOURCE / 'gamekit.py', 'review', 'prepare', '--output', dest, '--root', SOURCE, ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('already exists', r.stderr)

    def make_triads(self, *, high=True, blocked=False, shared_session=False, critical=False):
        import json
        out = self.base / 'review'
        self.call(SOURCE / 'gamekit.py', 'review', 'prepare', '--output', out, '--root', SOURCE)
        (out / 'evidence' / 'real-app.png').write_bytes(b'fixture: not an actual capture')
        (out / 'evidence' / 'run.log').write_text('fixture task result', encoding='utf-8')
        roles = ['tech-lead', 'product-manager', 'end-user']
        for role in roles:
            doc = out / f'{role}.json'
            report = json.loads(doc.read_text())
            report.update(session_id='same' if shared_session else role + '-fresh',
                          independence='isolated-session', scope='build 100, iPhone portrait',
                          screens_examined=['Home', 'Gameplay', 'Result'],
                          tasks_tested=['From Home start level, finish and restart'],
                          observations=['Clear primary call to action', 'Next level accessible', 'Back button visible'],
                          evidence_files=['evidence/real-app.png', 'evidence/run.log'],
                          scores={k: 9.2 if high else 7.5 for k in report['scores']},
                          limitations=['NOT RUN: simulator not available'] if blocked else [],
                          findings=[])
            if critical and role == 'tech-lead':
                report['findings'] = [{
                    'id':'TL-1', 'severity':'P1', 'screen':'Gameplay', 'evidence':'evidence/run.log',
                    'repro_steps':'tap start', 'expected':'game begins', 'actual':'stuck',
                    'recommendation':'fix transition', 'acceptance_test':'start in 1 tap',
                    'status':'open'}]
            doc.write_text(json.dumps(report), encoding='utf-8')
        return out

    def test_review_evaluate_rejects_blank_reports(self):
        out = self.base / 'blank'
        self.call(SOURCE / 'gamekit.py', 'review', 'prepare', '--output', out, '--root', SOURCE)
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('NOT APPROVED', result.stdout)

    def test_review_evaluate_rejects_higher_scores_with_open_critical_issue(self):
        out = self.make_triads(critical=True)
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('unresolved P1', result.stdout)
        self.assertNotEqual(result.returncode, 0)

    def test_review_evaluate_rejects_duplicate_contexts(self):
        out = self.make_triads(shared_session=True)
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('share a session_id', result.stdout)

    def test_review_evaluate_rejects_blocked_runtime(self):
        out = self.make_triads(blocked=True)
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('blocked/unverified checks', result.stdout)

    def test_review_evaluate_rejects_missing_screenshot(self):
        out = self.make_triads()
        (out / 'evidence' / 'real-app.png').unlink()
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('missing evidence file', result.stdout)

    def test_review_evaluate_report_gate_passes_valid_fixture_only(self):
        out = self.make_triads()
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out)
        self.assertIn('REPORT GATES PASSED', result.stdout)
        self.assertIn('does not prove screenshots', result.stdout)

    def test_review_evaluate_rejects_only_log_no_visual_capture(self):
        import json
        out = self.make_triads()
        for role in ('tech-lead', 'product-manager', 'end-user'):
            file = out / f'{role}.json'
            data = json.loads(file.read_text())
            data['evidence_files'] = ['evidence/run.log']
            file.write_text(json.dumps(data))
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('logs alone insufficient', result.stdout)

    def test_review_evaluate_rejects_sequential_single_agent(self):
        import json
        out = self.make_triads()
        data_file = out / 'end-user.json'
        d = json.loads(data_file.read_text()); d['independence'] = 'single-session'
        data_file.write_text(json.dumps(d))
        result = self.call(SOURCE / 'gamekit.py', 'review', 'evaluate', '--dir', out, ok=False)
        self.assertIn('provisional only', result.stdout)


    def test_drui_cli_menu_matches_canonical_stage_registry(self):
        import json
        script = SOURCE / 'scripts/drui'
        menu = self.call(script, 'list').stdout
        data = json.loads(self.call(script, 'list', '--json').stdout)
        self.assertEqual(data['skill'], 'drui')
        self.assertEqual(data['count'], 20)
        self.assertEqual(len({item['name'] for item in data['workflows']}), 20)
        self.assertIn('20 workflows', menu)
        self.assertIn('严苛独立评审', menu)
        self.assertIn('review-triad', menu)
        self.assertIn('review-loop', menu)
        for item in data['workflows']:
            self.assertIn(item['name'], menu)
            self.assertTrue((SOURCE / 'prompts/drui/stages' / (item['name'] + '.md')).is_file())
        self.assertFalse(self.root.exists())

    def test_drui_cli_help_and_prompt_shorthand(self):
        script = SOURCE / 'scripts/drui'
        helper = self.call(script, 'help', 'review-tl').stdout
        self.assertIn('REVIEW ONLY', helper)
        self.assertIn('drui prompt review-tl', helper)
        p = self.call(script, 'prompt', 'review-tl').stdout
        shorthand = self.call(script, 'review-tl').stdout
        self.assertEqual(p, shorthand)
        self.assertIn('Stage: review-tl', p)
        self.assertIn('READ-ONLY', p)
        self.assertFalse(self.root.exists())

    def test_drui_cli_prompt_project_is_readonly_unless_output_requested(self):
        script = SOURCE / 'scripts/drui'
        project = self.base / 'Game Folder'
        project.mkdir()
        result = self.call(script, 'prompt', 'review-user', '--project', project).stdout
        self.assertIn(str(project), result)
        self.assertEqual(list(project.iterdir()), [])
        output = self.base / 'task.md'
        self.call(script, 'prompt', 'review-loop', '--output', output)
        self.assertIn('Stage: review-loop', output.read_text())
        self.assertNotEqual(self.call(script, 'prompt', 'review-loop', '--output', output, ok=False).returncode, 0)
        self.call(script, 'prompt', 'review-loop', '--output', output, '--force')

    def test_drui_cli_install_creates_safe_global_symlink(self):
        self.install()
        link = self.home / '.local/bin/drui'
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), self.root / 'scripts/drui')
        direct = self.call(link, 'list').stdout
        self.assertIn('20 workflows', direct)
        self.call(self.root / 'gamekit.py', 'doctor', '--root', self.root)
        self.call(self.root / 'gamekit.py', 'link', '--agents', 'all', '--root', self.root)
        self.assertEqual(link.resolve(), self.root / 'scripts/drui')

    def test_drui_cli_install_does_not_overwrite_existing_name(self):
        existing = self.home / '.local/bin/drui'
        existing.parent.mkdir(parents=True)
        existing.write_text('my existing command\n')
        result = self.call(SOURCE / 'gamekit.py', 'install', '--root', self.root, '--agents', 'all', ok=False)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn('Existing drui command preserved', output)
        self.assertIn('FAIL', output)
        self.assertEqual(existing.read_text(), 'my existing command\n')
        attempted = self.call(self.root / 'gamekit.py', 'link', '--root', self.root, '--agents', 'all', ok=False)
        self.assertNotEqual(attempted.returncode, 0)
        self.assertEqual(existing.read_text(), 'my existing command\n')
        self.call(self.root / 'gamekit.py', 'unlink', '--root', self.root, '--agents', 'all')
        self.assertTrue(existing.is_file())

    def test_drui_cli_dry_run_and_safe_unlink(self):
        self.call(SOURCE / 'gamekit.py', 'install', '--root', self.root, '--dry-run')
        self.assertFalse((self.home / '.local').exists())
        self.install('codex')
        link = self.home / '.local/bin/drui'
        self.assertTrue(link.is_symlink())
        self.call(self.root / 'gamekit.py', 'unlink', '--root', self.root, '--agents', 'all', '--dry-run')
        self.assertTrue(link.is_symlink())
        self.call(self.root / 'gamekit.py', 'unlink', '--root', self.root, '--agents', 'all')
        self.assertFalse(link.exists())
        self.assertTrue((self.root / 'scripts/drui').exists())

    def test_drui_v14_upgrade_adds_missing_bin_entry(self):
        self.install('codex')
        old_bin = self.root / 'scripts/drui'
        old_bin.unlink()  # Simulates a real pre-1.5 installed kit
        self.assertFalse(old_bin.exists())
        self.call(self.root / 'gamekit.py', 'upgrade', '--root', self.root, '--from', SOURCE)
        self.assertTrue(old_bin.is_file())
        self.call(self.root / 'gamekit.py', 'link', '--root', self.root, '--agents', 'codex')
        link = self.home / '.local/bin/drui'
        self.assertTrue(link.is_symlink())
        self.assertIn('20 workflows', self.call(link, 'list').stdout)

    def test_drui_cli_unknown_commands_fail_without_side_effects(self):
        script = SOURCE / 'scripts/drui'
        result = self.call(script, 'nonexistent-workflow', ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('drui list', result.stderr)
        self.assertFalse(self.root.exists())

    def test_drui_chat_menu_and_docs_are_present(self):
        skill = (SOURCE / 'skills/drui/SKILL.md').read_text(encoding='utf-8')
        doc = (SOURCE / 'docs/DRUI_COMMANDS_ZH.md').read_text(encoding='utf-8')
        for command in ('drui list', 'drui help', 'drui review-tl', 'drui prompt'):
            self.assertIn(command, skill + doc)
        for stage in ('full', 'review-triad', 'review-loop', 'visual-review'):
            self.assertIn(stage, doc)
        self.assertIn('NOT RUN', doc)
        self.assertIn('DRUI CLI', (SOURCE / 'docs/CHANGELOG_v1.5.md').read_text())


class OilUIPlusRoutingTests(unittest.TestCase):
    setUp = GameAgentKitTests.setUp
    tearDown = GameAgentKitTests.tearDown
    call = GameAgentKitTests.call
    install = GameAgentKitTests.install
    make_external_oil = GameAgentKitTests.make_external_oil

    """Adversarial UI source resolution + cross-agent CLI registration."""

    def test_kit_installs_real_standalone_plus_skill(self):
        self.install('all')
        original = self.root / 'skills/oil-ui-plus/SKILL.md'
        self.assertTrue(original.is_file())
        self.assertIn('name: oil-ui-plus', original.read_text())
        for loc in ('.agents/skills', '.claude/skills', '.gemini/config/skills', '.gemini/antigravity-cli/skills'):
            target = self.home / loc / 'oil-ui-plus'
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), original.parent)

    def test_default_ui_source_is_plus_when_pro_missing_even_with_oil_ui(self):
        self.install('codex')
        source = self.make_external_oil()
        self.call(self.root/'gamekit.py', 'register-external', '--name','oil-ui','--source',source,'--agents','codex')
        r = self.call(self.root/'scripts/drui', 'sources', '--agent','codex')
        self.assertIn('selected automatically: oil-ui-plus', r.stdout)
        prompt = self.call(self.root/'scripts/drui','prompt','review-loop','--agent','codex')
        self.assertIn('Primary selected source in CLI environment: oil-ui-plus',prompt.stdout)

    def test_real_external_pro_when_installed_takes_priority(self):
        self.install('all')
        pro = self.base/'licensed-pro'; pro.mkdir()
        (pro/'SKILL.md').write_text('---\nname: oil-ui-pro\ndescription: external owned pro\n---\n')
        self.call(self.root/'gamekit.py','register-external','--name','oil-ui-pro','--source',pro,'--agents','claude')
        self.assertIn('selected automatically: oil-ui-pro',
                      self.call(self.root/'scripts/drui','sources','--agent','claude').stdout)
        self.assertIn('selected automatically: oil-ui-plus',
                      self.call(self.root/'scripts/drui','sources','--agent','codex').stdout)
        auto = self.call(self.root/'scripts/drui','prompt','full','--agent','claude').stdout
        self.assertIn('Primary selected source in CLI environment: oil-ui-pro',auto)

    def test_forced_missing_pro_fails_and_never_silently_substitutes_plus(self):
        self.install('codex')
        result=self.call(self.root/'scripts/drui','prompt','full','--ui-source','pro','--agent','codex',ok=False)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('No fallback was performed',result.stderr)

    def test_explicit_plus_ignores_pro_and_prints_clear_provenance(self):
        self.install('codex')
        pro = self.base/'pro'; pro.mkdir()
        (pro/'SKILL.md').write_text('---\nname: oil-ui-pro\ndescription: external\n---\n')
        self.call(self.root/'gamekit.py','register-external','--name','oil-ui-pro','--source',pro,'--agents','codex')
        prompt = self.call(self.root/'scripts/drui','plus','--agent','codex').stdout
        self.assertIn('Requested UI source: plus.',prompt)
        self.assertIn('Primary selected source in CLI environment: oil-ui-plus',prompt)
        self.assertIn('never confuse Oil UI Plus with the official paid Pro',prompt)

    def test_forced_open_oil_ui_requires_installation_and_can_be_selected(self):
        self.install('codex')
        nope = self.call(self.root/'scripts/drui','prompt','visual-review','--ui-source','oil-ui',ok=False)
        self.assertIn('No fallback was performed',nope.stderr)
        source=self.make_external_oil()
        self.call(self.root/'gamekit.py','register-external','--name','oil-ui','--source',source,'--agents','codex')
        prompt=self.call(self.root/'scripts/drui','prompt','visual-review','--ui-source','oil-ui').stdout
        self.assertIn('Primary selected source in CLI environment: oil-ui at ',prompt)

    def test_forced_generic_drui_works_even_with_plus_installed(self):
        self.install('codex')
        prompt=self.call(self.root/'scripts/drui','prompt','review-tl','--ui-source','drui').stdout
        self.assertIn('Primary selected source in CLI environment: drui at ',prompt)
        self.assertIn('UI method priority: oil-ui-pro',prompt)

    def test_source_router_stage_docs_and_no_proprietary_claims(self):
        source = (SOURCE/'skills/oil-ui-plus/SKILL.md').read_text()
        self.assertIn('NOT the official paid',source)
        assert_files=[SOURCE/'skills/drui/SKILL.md',SOURCE/'docs/UI_SOURCE_ROUTING.md',SOURCE/'prompts/OIL_UI_ENHANCED_WORKFLOW.md']
        assert_files += list((SOURCE/'prompts/drui/stages').glob('*.md'))
        self.assertEqual(len(list((SOURCE/'prompts/drui/stages').glob('*.md'))),20)
        for file in assert_files:
            data=file.read_text()
            for name in ('oil-ui-pro','oil-ui-plus','oil-ui'):
                self.assertIn(name,data,str(file))



if __name__ == '__main__':
    unittest.main(verbosity=2)
