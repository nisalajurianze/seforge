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
from engine.evidence import record_manual_evidence, verify_evidence

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ensure_layout(self.root)
        (self.root / "report.txt").write_text("passed", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_evidence_chain_valid_then_detects_tamper(self):
        first = record_manual_evidence(
            self.root, claim="A passed", result="pass", method="test",
            source_path="report.txt", owner="tester", task_id="TSK-1", skill_ids=[8]
        )
        second = record_manual_evidence(
            self.root, claim="B passed", result="pass", method="review",
            owner="reviewer", task_id="TSK-1", skill_ids=[22]
        )
        result = verify_evidence(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(2, result["count"])

        ledger = self.root / ".engineering" / "evidence" / "ledger.jsonl"
        lines = ledger.read_text(encoding="utf-8").splitlines()
        record = json.loads(lines[0])
        record["claim"] = "tampered"
        lines[0] = json.dumps(record, sort_keys=True)
        ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        tampered = verify_evidence(self.root)
        self.assertFalse(tampered["valid"])
        self.assertTrue(any(f["code"] == "RECORD_HASH_MISMATCH" for f in tampered["findings"]))

if __name__ == "__main__":
    unittest.main()

class EvidenceAttachmentIntegrityTests(unittest.TestCase):
    def test_record_file_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_layout(root)
            record = record_manual_evidence(root, claim="Review passed", result="pass", method="review", owner="reviewer")
            record_file = root / ".engineering" / "evidence" / "records" / f"{record['evidence_id']}.json"
            changed = json.loads(record_file.read_text(encoding="utf-8"))
            changed["claim"] = "tampered copy"
            record_file.write_text(json.dumps(changed), encoding="utf-8")
            result = verify_evidence(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any(f["code"] == "RECORD_FILE_MISMATCH" for f in result["findings"]))

    def test_missing_manual_source_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_layout(root)
            source = root / "report.txt"
            source.write_text("passed", encoding="utf-8")
            record_manual_evidence(root, claim="Report passed", result="pass", method="report", source_path="report.txt")
            source.unlink()
            result = verify_evidence(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any(f["code"] == "MISSING_SOURCE" for f in result["findings"]))

    def test_external_or_missing_source_path_is_rejected_at_record_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_layout(root)
            with self.assertRaises(FileNotFoundError):
                record_manual_evidence(root, claim="Missing", result="pass", method="review", source_path="missing.txt")
            with self.assertRaises(ValueError):
                record_manual_evidence(root, claim="Escape", result="pass", method="review", source_path="../outside.txt")
