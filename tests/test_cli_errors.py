from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]


class CliErrorHandlingTests(unittest.TestCase):
    def test_missing_task_is_concise_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "-S",
                    str(PACK_ROOT / "sepack.py"),
                    "task",
                    "show",
                    "--target",
                    tmp,
                    "TSK-missing",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("Task not found", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_debug_mode_preserves_traceback_for_maintainers(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(__import__("os").environ)
            env["SEPACK_DEBUG"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    "-S",
                    str(PACK_ROOT / "sepack.py"),
                    "task",
                    "show",
                    "--target",
                    tmp,
                    "TSK-missing",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
