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

from engine.commands import discover_commands, execute_command
from engine.state import ensure_layout
from engine.common import load_json, atomic_write_json
from engine.state import command_registry_path

class CommandSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ensure_layout(self.root)
        (self.root / "package.json").write_text(json.dumps({
            "name":"cmd-test",
            "scripts":{"test":"echo token=supersecret"}
        }), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_review_is_bound_to_source_hash(self):
        registry = discover_commands(self.root)
        command = next(c for c in registry["commands"] if c["id"] == "node:test")
        command["reviewed"] = True
        command["reviewed_definition_hash"] = command["definition_hash"]
        command["reviewed_source_sha256"] = command["source_sha256"]

        (self.root / "package.json").write_text(json.dumps({
            "name":"cmd-test",
            "scripts":{"test":"echo changed"}
        }), encoding="utf-8")
        with self.assertRaises(PermissionError):
            execute_command(self.root, command, trust_project_scripts=True)

    def test_output_redacts_common_secret_pattern(self):
        command = {
            "id":"test:redact","category":"unit",
            "argv":[sys.executable,"-c","print('token=supersecret')"],
            "rendered":"python -c print-token","cwd":".","source":"test",
            "source_path":None,"source_sha256":None,
            "definition_hash":"x","reviewed_definition_hash":None,"reviewed_source_sha256":None,
            "trust":"pack_defined","network":False,"risk":"R1",
            "risk_reasons":[],"enabled":True,"available":True,"reviewed":False
        }
        result = execute_command(self.root, command)
        self.assertIn("[REDACTED]", result["stdout"])
        self.assertNotIn("supersecret", result["stdout"])

if __name__ == "__main__":
    unittest.main()
