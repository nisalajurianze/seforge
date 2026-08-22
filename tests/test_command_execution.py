from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK_ROOT))

from engine.commands import execute_command
from engine.evidence import verify_evidence
from engine.state import ensure_layout


class CommandExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ensure_layout(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_project_defined_command_requires_review_and_per_invocation_trust(self):
        command = {
            "id": "test:python",
            "category": "unit",
            "argv": [sys.executable, "-c", "print('ok')"],
            "rendered": "python -c print-ok",
            "cwd": ".",
            "source": "test",
            "source_path": None,
            "source_sha256": None,
            "definition_hash": "definition-hash",
            "reviewed_definition_hash": None,
            "reviewed_source_sha256": None,
            "trust": "project_defined",
            "network": False,
            "risk": "R2",
            "risk_reasons": ["executes project-controlled code without an OS sandbox"],
            "execution_isolation": "process_only_no_os_sandbox",
            "enabled": True,
            "available": True,
            "reviewed": False,
        }
        with self.assertRaises(PermissionError):
            execute_command(self.root, command, trust_project_scripts=True)

        command["reviewed"] = True
        command["reviewed_definition_hash"] = command["definition_hash"]
        with self.assertRaises(PermissionError):
            execute_command(self.root, command)

        result = execute_command(self.root, command, trust_project_scripts=True)
        self.assertEqual(0, result["exit_code"])
        self.assertEqual("process_only_no_os_sandbox", result["execution_isolation"])
        self.assertTrue(verify_evidence(self.root)["valid"])
        self.assertFalse(list(self.root.rglob("__pycache__")))
        self.assertFalse(list(self.root.rglob("*.pyc")))


if __name__ == "__main__":
    unittest.main()
