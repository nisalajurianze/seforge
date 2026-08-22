from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PackImmutabilityTests(unittest.TestCase):
    def test_validator_does_not_create_bytecode(self):
        before = sorted(str(p.relative_to(PACK_ROOT)) for p in PACK_ROOT.rglob("*.pyc"))
        result = subprocess.run([sys.executable, "-S", str(PACK_ROOT / "schemas" / "validate_pack.py")], capture_output=True, text=True, timeout=180)
        self.assertEqual(0, result.returncode, result.stderr)
        after = sorted(str(p.relative_to(PACK_ROOT)) for p in PACK_ROOT.rglob("*.pyc"))
        self.assertEqual(before, after)

    def test_eval_runner_does_not_rewrite_baseline_without_output_flag(self):
        baseline = PACK_ROOT / "evals" / "latest-results.json"
        before = digest(baseline)
        result = subprocess.run([sys.executable, "-S", str(PACK_ROOT / "evals" / "run_evals.py")], capture_output=True, text=True, timeout=300)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, digest(baseline))


if __name__ == "__main__":
    unittest.main()
