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

from engine.state import ensure_layout
from engine.common import load_json

class StateMigrationTests(unittest.TestCase):
    def test_v1_state_migrates_without_deleting_legacy_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / ".engineering" / "plan"
            old.mkdir(parents=True)
            (old / "PROJECT-STRATEGY.md").write_text("legacy plan", encoding="utf-8")
            (root / ".engineering" / "state.json").write_text(json.dumps({
                "state_version":1,"pack_version":"1.3.0","migrations":[]
            }), encoding="utf-8")
            ensure_layout(root)
            state = load_json(root / ".engineering" / "state.json")
            self.assertEqual(2, state["state_version"])
            self.assertTrue((root / ".engineering" / "plans" / "PROJECT-STRATEGY.md").exists())
            self.assertTrue((root / ".engineering" / "plan" / "PROJECT-STRATEGY.md").exists())

if __name__ == "__main__":
    unittest.main()
