from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK_ROOT))

from engine.commands import discover_commands, execute_command
from engine.state import ensure_layout


class PythonCommandIsolationTests(unittest.TestCase):
    def test_syntax_check_ignores_installed_tooling_and_creates_no_bytecode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\nversion='0.1.0'\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "ok.py").write_text("x = 1\n", encoding="utf-8")
            bad_tool = root / ".engineering" / "skill-pack" / "bad.py"
            bad_tool.parent.mkdir(parents=True)
            bad_tool.write_text("this is not valid python !!!", encoding="utf-8")
            ensure_layout(root)
            registry = discover_commands(root)
            command = next(c for c in registry["commands"] if c["id"] == "python:compile")
            result = execute_command(root, command)
            self.assertEqual(0, result["exit_code"], result["stderr"])
            self.assertFalse(list(root.rglob("*.pyc")))
            self.assertFalse(list(root.rglob("__pycache__")))

    def test_unittest_is_selected_when_pytest_is_not_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\nversion='0.1.0'\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_x.py").write_text("import unittest\n", encoding="utf-8")
            ensure_layout(root)
            ids = {c["id"] for c in discover_commands(root)["commands"]}
            self.assertIn("python:unittest", ids)
            self.assertNotIn("python:pytest", ids)


if __name__ == "__main__":
    unittest.main()
