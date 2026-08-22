from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import atomic_write_json, iter_files, safe_relative, sha256_file, utc_now

INTEGRITY_FILE = "PACK-INTEGRITY.json"
EXCLUDED_PARTS = {"__pycache__", ".git"}
EXCLUDED_FILES = {INTEGRITY_FILE}

def generate_pack_integrity(pack_root: Path) -> dict[str, Any]:
    files = []
    for path in iter_files(pack_root, exclude_parts=EXCLUDED_PARTS):
        rel = safe_relative(path, pack_root)
        if rel in EXCLUDED_FILES or rel.endswith(".pyc") or rel.endswith(".zip"):
            continue
        files.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
        })
    manifest = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "algorithm": "sha256",
        "file_count": len(files),
        "files": files,
        "note": "This manifest detects modification or incomplete distribution. It is not a cryptographic signature.",
    }
    atomic_write_json(pack_root / INTEGRITY_FILE, manifest)
    return manifest

def verify_pack_integrity(pack_root: Path) -> dict[str, Any]:
    path = pack_root / INTEGRITY_FILE
    if not path.exists():
        return {"valid": False, "findings": [{"code": "MISSING_INTEGRITY_MANIFEST"}]}
    manifest = json.loads(path.read_text(encoding="utf-8"))
    findings = []
    expected_paths = set()
    for item in manifest.get("files", []):
        rel = item["path"]
        expected_paths.add(rel)
        candidate = pack_root / rel
        if not candidate.exists():
            findings.append({"code": "MISSING_FILE", "path": rel})
            continue
        if candidate.stat().st_size != item.get("size"):
            findings.append({"code": "SIZE_MISMATCH", "path": rel})
        if sha256_file(candidate) != item.get("sha256"):
            findings.append({"code": "HASH_MISMATCH", "path": rel})

    actual_paths = set()
    for candidate in iter_files(pack_root, exclude_parts=EXCLUDED_PARTS):
        rel = safe_relative(candidate, pack_root)
        if rel in EXCLUDED_FILES or rel.endswith(".pyc") or rel.endswith(".zip"):
            continue
        actual_paths.add(rel)
    for rel in sorted(actual_paths - expected_paths):
        findings.append({"code": "UNTRACKED_FILE", "path": rel})

    return {
        "valid": not findings,
        "expected_file_count": manifest.get("file_count"),
        "actual_file_count": len(actual_paths),
        "findings": findings,
    }
