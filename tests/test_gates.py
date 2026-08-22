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
from engine.tasks import create_task, save_task
from engine.evidence import record_manual_evidence
from engine.gates import task_gate

class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ensure_layout(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_task_gate_blocks_without_acceptance_and_evidence_then_passes(self):
        task = create_task(self.root, name="Simple change", description="Change a local message")
        blocked = task_gate(self.root, task["id"])
        self.assertFalse(blocked["ready"])

        task["acceptance_criteria"] = ["Message is updated"]
        task["skill_ids"] = [2,22]
        save_task(self.root, task)
        evidence = record_manual_evidence(
            self.root, claim="Message updated", result="pass", method="review",
            task_id=task["id"], skill_ids=[2,22], owner="reviewer"
        )
        task = __import__("engine.tasks", fromlist=["load_task"]).load_task(self.root, task["id"])
        task["acceptance_evidence"] = {"0": [evidence["evidence_id"]]}
        save_task(self.root, task)
        ready = task_gate(self.root, task["id"])
        self.assertTrue(ready["ready"], ready)

if __name__ == "__main__":
    unittest.main()

class ReleaseTaskGateRegressionTests(unittest.TestCase):
    def test_release_blocks_completed_task_that_no_longer_passes_its_gate(self):
        from engine.gates import release_gate
        from engine.common import atomic_write_json
        from engine.state import plan_status_path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            eng = ensure_layout(root)
            atomic_write_json(eng / "reports" / "project-facts.json", {"project_name":"demo"})
            atomic_write_json(eng / "skill-manifest.json", {"skills":[]})
            atomic_write_json(eng / "commands" / "registry.json", {"commands":[]})
            atomic_write_json(plan_status_path(root), {"strategy":"approved"})
            for rel in ["rollback.md", "operations.md", "release-notes.md"]:
                (eng / "artifacts" / rel).write_text(rel, encoding="utf-8")

            task = create_task(root, name="Forced completion", description="Local task")
            task["status"] = "complete"
            task["acceptance_criteria"] = ["Must be verified"]
            task["skill_ids"] = [2]
            task["decisions"] = [{"type":"forced_completion_exception", "approved_by":"owner"}]
            save_task(root, task)

            # Evidence belongs to another task, so the completed task itself is unproven.
            other = create_task(root, name="Other", description="Other task")
            record_manual_evidence(root, claim="Other passed", result="pass", method="test", task_id=other["id"], skill_ids=[2])
            other["status"] = "cancelled"
            save_task(root, other)

            result = release_gate(root)
            self.assertFalse(result["ready"])
            check = next(c for c in result["checks"] if c["name"] == "completed_task_gates")
            self.assertEqual("block", check["status"])
            self.assertIn(task["id"], check["evidence"])


class AcceptanceEvidenceCoverageTests(unittest.TestCase):
    def test_unlinked_passing_evidence_does_not_prove_acceptance_criterion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_layout(root)
            task = create_task(
                root,
                name="Two outcomes",
                description="Verify both outcomes",
                acceptance_criteria=["Outcome A passes", "Outcome B passes"],
            )
            task["skill_ids"] = [2]
            save_task(root, task)
            evidence = record_manual_evidence(
                root,
                claim="A generic check passed",
                result="pass",
                method="test",
                task_id=task["id"],
                skill_ids=[2],
            )
            task = __import__("engine.tasks", fromlist=["load_task"]).load_task(root, task["id"])
            task["acceptance_evidence"] = {"0": [evidence["evidence_id"]]}
            save_task(root, task)
            result = task_gate(root, task["id"])
            self.assertFalse(result["ready"])
            coverage = next(c for c in result["checks"] if c["name"] == "acceptance_evidence_coverage")
            self.assertEqual("block", coverage["status"])
