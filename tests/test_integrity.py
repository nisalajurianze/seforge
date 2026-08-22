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

from engine.integrity import generate_pack_integrity, verify_pack_integrity

class IntegrityTests(unittest.TestCase):
    def test_generate_verify_and_detect_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("hello", encoding="utf-8")
            (root / "sub").mkdir()
            (root / "sub" / "b.txt").write_text("world", encoding="utf-8")
            generated = generate_pack_integrity(root)
            self.assertEqual(2, generated["file_count"])
            self.assertTrue(verify_pack_integrity(root)["valid"])
            (root / "a.txt").write_text("tampered", encoding="utf-8")
            result = verify_pack_integrity(root)
            self.assertFalse(result["valid"])
            self.assertTrue(any(f["code"] == "HASH_MISMATCH" for f in result["findings"]))

if __name__ == "__main__":
    unittest.main()
