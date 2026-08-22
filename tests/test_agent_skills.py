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

class AgentSkillFormatTests(unittest.TestCase):
    def test_skill_counts_and_frontmatter(self):
        skill_dirs = [p for p in (PACK_ROOT / "agent-skills").iterdir() if p.is_dir()]
        engineering = [p for p in skill_dirs if p.name.startswith("se-")]
        workflow = [p for p in skill_dirs if p.name.startswith("wf-")]
        self.assertEqual(80, len(engineering))
        self.assertEqual(12, len(workflow))
        self.assertEqual(92, len(skill_dirs))

        names = set()
        for directory in skill_dirs:
            text = (directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), directory.name)
            front = text.split("---", 2)[1]
            match = __import__("re").search(r"^name:\s*(.+)$", front, __import__("re").M)
            desc = __import__("re").search(r"^description:\s*(.+)$", front, __import__("re").M)
            self.assertIsNotNone(match, directory.name)
            self.assertIsNotNone(desc, directory.name)
            name = match.group(1).strip()
            self.assertNotIn(name, names)
            names.add(name)
            self.assertLessEqual(len(name), 64)
            self.assertTrue((directory / "references").exists() or directory.name.startswith("wf-"))

    def test_engineering_skill_references_exist(self):
        for directory in (PACK_ROOT / "agent-skills").iterdir():
            if directory.name.startswith("se-"):
                self.assertTrue((directory / "references" / "detailed-guide.md").is_file())

if __name__ == "__main__":
    unittest.main()
