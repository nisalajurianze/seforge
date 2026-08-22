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
from engine.state import ensure_layout
from engine.common import atomic_write_json
from engine.tasks import create_task, generate_exec_plan, load_task, save_task
from engine.evidence import record_manual_evidence

class TaskTransitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("# Auth Service", encoding="utf-8")
        (self.root / "package.json").write_text(json.dumps({"name":"auth-service","scripts":{"test":"echo ok"}}), encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src" / "auth.js").write_text("// auth", encoding="utf-8")
        result = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "init",
            "--target", str(self.root), "--goal", "Secure authentication service", "--json"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, result.returncode, result.stderr)

    def tearDown(self):
        self.temp.cleanup()

    def test_r2_start_requires_approval_and_completion_requires_gate(self):
        create = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "task", "create",
            "--target", str(self.root),
            "--name", "Change authorization architecture",
            "--description", "Modify authorization and authentication architecture",
            "--acceptance", "Unauthorized requests are rejected",
            "--plan"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, create.returncode, create.stderr)
        task_id = json.loads(create.stdout)["task"]["id"]

        blocked = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "task", "status",
            "--target", str(self.root), task_id, "--status", "in_progress"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(1, blocked.returncode)

        approved = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "approve",
            "--target", str(self.root), "--decision", "approve-strategy",
            "--approver", "owner"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, approved.returncode, approved.stderr)

        started = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "task", "status",
            "--target", str(self.root), task_id, "--status", "in_progress"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, started.returncode, started.stderr)

        incomplete = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "task", "status",
            "--target", str(self.root), task_id, "--status", "complete"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(1, incomplete.returncode)

        task = load_task(self.root, task_id)
        self.assertTrue(task["skill_ids"])
        added = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "evidence", "add",
            "--target", str(self.root), "--claim", "Authorization behavior verified",
            "--result", "pass", "--method", "integration test", "--task-id", task_id,
            "--criterion-index", "0", "--skill-id", str(task["skill_ids"][0]), "--owner", "reviewer"
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, added.returncode, added.stdout + added.stderr)
        completed = subprocess.run([
            sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "task", "status",
            "--target", str(self.root), task_id, "--status", "complete",
            "--completion-statement", "Acceptance criteria verified."
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

if __name__ == "__main__":
    unittest.main()
