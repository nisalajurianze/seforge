from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK_ROOT))

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "AGENTS.md").write_text("# Existing Project Rules\n\nKeep this content.\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_install_upgrade_and_uninstall_preserves_existing_rules(self):
        install_cmd = [
            sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
            "--target", str(self.root), "--providers", "agents", "--skip-quickstart"
        ]
        first = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
        self.assertEqual(0, first.returncode, first.stderr)
        text = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Existing Project Rules", text)
        self.assertIn("SEPACK:BEGIN v2", text)
        self.assertTrue((self.root / ".agents" / "skills").exists())

        second = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
        self.assertEqual(0, second.returncode, second.stderr)
        text2 = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(1, text2.count("SEPACK:BEGIN v2"))

        uninstall = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "scripts" / "uninstall.py"),
            "--target", str(self.root)
        ], capture_output=True, text=True, timeout=120)
        self.assertEqual(0, uninstall.returncode, uninstall.stderr)
        final = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Existing Project Rules", final)
        self.assertNotIn("SEPACK:BEGIN v2", final)

if __name__ == "__main__":
    unittest.main()

class InstallerBaselineRestoreTests(unittest.TestCase):
    def test_upgrade_restore_uses_pre_first_install_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original_rule = root / ".cursor" / "rules" / "software-engineering.mdc"
            original_rule.parent.mkdir(parents=True)
            original_rule.write_text("ORIGINAL CURSOR RULE\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Original AGENTS\n", encoding="utf-8")

            install_cmd = [
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                "--target", str(root), "--providers", "cursor,agents", "--skip-quickstart"
            ]
            first = subprocess.run(install_cmd, capture_output=True, text=True, timeout=180)
            self.assertEqual(0, first.returncode, first.stderr)
            second = subprocess.run(install_cmd, capture_output=True, text=True, timeout=180)
            self.assertEqual(0, second.returncode, second.stderr)

            uninstall = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "uninstall.py"),
                "--target", str(root), "--restore-backups"
            ], capture_output=True, text=True, timeout=180)
            self.assertEqual(0, uninstall.returncode, uninstall.stderr)
            self.assertEqual("ORIGINAL CURSOR RULE\n", original_rule.read_text(encoding="utf-8"))
            self.assertEqual("# Original AGENTS\n", (root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_uninstall_removes_only_skill_pack_claude_hook(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / ".claude" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({
                "hooks": {"Notification": [{"matcher":"", "hooks":[{"type":"command","command":"echo keep"}]}]},
                "permissions": {"allow": ["Read"]}
            }), encoding="utf-8")
            install = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                "--target", str(root), "--providers", "claude", "--enable-claude-hooks", "--skip-quickstart"
            ], capture_output=True, text=True, timeout=180)
            self.assertEqual(0, install.returncode, install.stderr)
            uninstall = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "uninstall.py"),
                "--target", str(root)
            ], capture_output=True, text=True, timeout=180)
            self.assertEqual(0, uninstall.returncode, uninstall.stderr)
            remaining = json.loads(settings.read_text(encoding="utf-8"))
            self.assertIn("Notification", remaining["hooks"])
            self.assertNotIn("PreToolUse", remaining["hooks"])
            self.assertEqual(["Read"], remaining["permissions"]["allow"])

class InstallerSkillCatalogueTests(unittest.TestCase):
    def test_default_installs_only_workflow_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                "--target", str(root), "--providers", "agents", "--skip-quickstart"
            ], capture_output=True, text=True, timeout=180)
            self.assertEqual(0, result.returncode, result.stderr)
            skills = [p.name for p in (root / ".agents" / "skills").iterdir() if p.is_dir()]
            self.assertEqual(12, len(skills))
            self.assertTrue(all(name.startswith("wf-") for name in skills))
            manifest = json.loads((root / ".engineering" / "install-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("workflow", manifest["skill_install_mode"])
            self.assertEqual(12, manifest["installed_provider_skill_count"])

    def test_all_mode_installs_full_catalogue_and_can_prune_back_to_workflows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = [sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                    "--target", str(root), "--providers", "agents", "--skip-quickstart"]
            all_result = subprocess.run(base + ["--skill-install-mode", "all"], capture_output=True, text=True, timeout=240)
            self.assertEqual(0, all_result.returncode, all_result.stderr)
            self.assertEqual(92, len([p for p in (root / ".agents" / "skills").iterdir() if p.is_dir()]))

            workflow_result = subprocess.run(base, capture_output=True, text=True, timeout=240)
            self.assertEqual(0, workflow_result.returncode, workflow_result.stderr)
            remaining = [p.name for p in (root / ".agents" / "skills").iterdir() if p.is_dir()]
            self.assertEqual(12, len(remaining))
            self.assertTrue(all(name.startswith("wf-") for name in remaining))


class InstallerProviderLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "AGENTS.md").write_text("# Existing\n\nKeep root rule.\n", encoding="utf-8")
        (self.root / ".claude").mkdir(parents=True)
        (self.root / ".claude" / "settings.json").write_text(json.dumps({
            "permissions": {"allow": ["Read"]},
            "hooks": {"PreToolUse": [{"matcher": "Read", "hooks": [{"type": "command", "command": "echo user"}]}]},
        }), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def _install(self, *extra):
        return subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
            "--target", str(self.root), "--skip-quickstart", *extra,
        ], capture_output=True, text=True, timeout=240)

    def test_provider_removal_prunes_unmodified_files_and_preserves_user_settings(self):
        first = self._install("--providers", "all", "--enable-claude-hooks")
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertTrue((self.root / ".github" / "skills").exists())
        self.assertTrue((self.root / ".claude" / "skills").exists())

        second = self._install("--providers", "agents")
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertFalse(any((self.root / ".github" / "skills").rglob("SKILL.md")))
        self.assertFalse(any((self.root / ".claude" / "skills").rglob("SKILL.md")))
        self.assertFalse((self.root / "CLAUDE.md").exists())
        settings = json.loads((self.root / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(["Read"], settings["permissions"]["allow"])
        rendered = json.dumps(settings)
        self.assertIn("echo user", rendered)
        self.assertNotIn("claude_pretool.py", rendered)
        manifest = json.loads((self.root / ".engineering" / "install-manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["claude_hooks_enabled"])

    def test_hook_enablement_persists_until_explicitly_disabled(self):
        first = self._install("--providers", "claude", "--enable-claude-hooks")
        self.assertEqual(0, first.returncode, first.stderr)
        second = self._install("--providers", "claude")
        self.assertEqual(0, second.returncode, second.stderr)
        settings = (self.root / ".claude" / "settings.json").read_text(encoding="utf-8")
        self.assertIn("claude_pretool.py", settings)

        third = self._install("--providers", "claude", "--disable-claude-hooks")
        self.assertEqual(0, third.returncode, third.stderr)
        settings = (self.root / ".claude" / "settings.json").read_text(encoding="utf-8")
        self.assertNotIn("claude_pretool.py", settings)
        self.assertIn("echo user", settings)
