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

from engine.discovery import discover

class ProviderDiscoveryIsolationTests(unittest.TestCase):
    def test_installed_provider_skills_do_not_change_project_domain_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Greeting Service\n\nA simple greeting utility.", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='greeting'\nversion='0.1.0'\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "greeting.py").write_text("def greet(): return 'hi'\n", encoding="utf-8")
            before = discover(root)

            install = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                "--target", str(root), "--providers", "all", "--skip-quickstart"
            ], capture_output=True, text=True, timeout=180)
            self.assertEqual(0, install.returncode, install.stderr)

            after = discover(root)
            self.assertEqual(before["domains"], after["domains"])
            self.assertEqual(before["stacks"], after["stacks"])
            self.assertEqual(before["platforms"], after["platforms"])

if __name__ == "__main__":
    unittest.main()
