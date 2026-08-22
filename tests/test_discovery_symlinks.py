from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(PACK_ROOT))

from engine.discovery import discover


class DiscoverySymlinkBoundaryTests(unittest.TestCase):
    def test_external_file_symlink_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as project_tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(project_tmp)
            outside = Path(outside_tmp)
            (project / "README.md").write_text("# Safe utility\n", encoding="utf-8")
            external = outside / "payment-secret.py"
            external.write_text("# payment wallet patient medical\n", encoding="utf-8")
            link = project / "payment-secret.py"
            try:
                link.symlink_to(external)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks are unavailable on this platform")

            facts = discover(project)
            self.assertEqual({}, facts["domains"])
            self.assertEqual(1, facts["counts"]["files_scanned"])


if __name__ == "__main__":
    unittest.main()
