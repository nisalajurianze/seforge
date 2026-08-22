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
from engine.commands import discover_commands
from engine.routing import route_skills
from engine.state import ensure_layout

class DiscoveryRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("# Billing API\n\nCustomer billing and payment API.", encoding="utf-8")
        (self.root / "package.json").write_text(json.dumps({
            "name":"billing-api",
            "description":"Payment API",
            "scripts":{"test":"node --test","build":"echo ok"}
        }), encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src" / "payment.js").write_text("export const pay = true;", encoding="utf-8")
        (self.root / "tests").mkdir()
        (self.root / "tests" / "payment.test.js").write_text("// test", encoding="utf-8")
        ensure_layout(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_discovery_finds_stack_domain_and_tests(self):
        facts = discover(self.root)
        self.assertIn("node", facts["stacks"])
        self.assertIn("payments", facts["domains"])
        self.assertTrue(facts["signals"]["tests_present"])

    def test_routing_activates_payment_profile(self):
        facts = discover(self.root)
        manifest = route_skills(self.root, PACK_ROOT, facts, {"impact_level":"L3"})
        active = {s["id"] for s in manifest["skills"] if s["status"] == "active"}
        self.assertIn(78, active)
        self.assertIn(37, active)
        self.assertIn(49, active)

    def test_command_discovery(self):
        registry = discover_commands(self.root)
        ids = {c["id"] for c in registry["commands"]}
        self.assertIn("node:test", ids)
        self.assertIn("node:build", ids)
        node_test = next(c for c in registry["commands"] if c["id"] == "node:test")
        self.assertEqual("project_defined", node_test["trust"])

if __name__ == "__main__":
    unittest.main()


class TaskRoutingPrecisionTests(unittest.TestCase):
    def test_standard_library_does_not_activate_interoperability_skill(self):
        from engine.routing import select_task_skills
        manifest = {
            "skills": [
                {"id": 2, "status": "active"},
                {"id": 8, "status": "active"},
                {"id": 17, "status": "active"},
                {"id": 22, "status": "active"},
                {"id": 31, "status": "active"},
            ]
        }
        task = {
            "name": "Run standard-library tests",
            "description": "Use Python standard-library unittest discovery.",
            "acceptance_criteria": [],
            "files": ["tests/test_basic.py"],
            "tags": [],
            "skill_ids": [],
        }
        selected = select_task_skills(task, manifest)
        self.assertNotIn(31, selected)
