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
from engine.routing import route_skills
from engine.commands import discover_commands
from engine.tasks import create_task, generate_exec_plan, load_task
from engine.context import build_task_context
from engine.state import ensure_layout
from engine.common import atomic_write_json

class ContextBudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("# Auth API", encoding="utf-8")
        (self.root / "package.json").write_text(json.dumps({
            "name":"auth-api","scripts":{"test":"echo ok"}
        }), encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src" / "auth.js").write_text("export const login = true;", encoding="utf-8")
        ensure_layout(self.root)
        facts = discover(self.root)
        atomic_write_json(self.root / ".engineering" / "reports" / "project-facts.json", facts)
        atomic_write_json(self.root / ".engineering" / "project-context.json", {
            "schema_version":2,"project_name":"auth-api","goal":"secure login","mode":"guide_and_build",
            "autonomy":"ask_before_material_decisions","impact_level":"L2","data_sensitivity":"personal",
            "provenance":{},"unresolved":[],"platforms":facts["platforms"],"domains":["identity"]
        })
        route_skills(self.root, PACK_ROOT, facts, {"impact_level":"L2"})
        discover_commands(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_small_context_is_bounded_and_task_specific(self):
        task = create_task(
            self.root, name="Add secure login",
            description="Implement authentication, sessions, authorization, and negative tests.",
            files=["src/auth.js"], acceptance_criteria=["valid login","invalid rejected"]
        )
        generate_exec_plan(self.root, task)
        result = build_task_context(self.root, PACK_ROOT, task["id"], budget_name="small", max_skills=6)
        self.assertLessEqual(result["actual_words"], 4200)
        self.assertLessEqual(len(result["selected_skill_ids"]), 6)
        self.assertIn(49, result["selected_skill_ids"])
        self.assertTrue((self.root / result["bundle_path"]).exists())

if __name__ == "__main__":
    unittest.main()
