from __future__ import annotations

import json
import os
import subprocess
import uuid
from pathlib import Path
from typing import Any

from .common import (
    ProjectLock, append_jsonl, atomic_write_json, canonical_json_bytes, environment_summary,
    load_json, safe_relative, sha256_bytes, sha256_file, utc_now
)
from .state import ensure_layout, engineering_dir, evidence_ledger_path

def _git_metadata(project_root: Path) -> dict[str, Any]:
    def run(args: list[str]) -> str | None:
        try:
            p = subprocess.run(args, cwd=project_root, capture_output=True, text=True, timeout=10)
            return p.stdout.strip() if p.returncode == 0 else None
        except Exception:
            return None
    return {
        "commit": run(["git", "rev-parse", "HEAD"]),
        "branch": run(["git", "branch", "--show-current"]),
        "dirty": bool(run(["git", "status", "--porcelain"])),
    }

def _last_hash(ledger: Path) -> str | None:
    if not ledger.exists():
        return None
    last = None
    with ledger.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                last = json.loads(line)
    return last.get("record_hash") if last else None

def record_command_evidence(project_root: Path, command_result: dict[str, Any],
                            *, task_id: str | None = None,
                            skill_ids: list[int] | None = None) -> dict[str, Any]:
    eng = ensure_layout(project_root)
    evidence_id = f"EV-{uuid.uuid4().hex[:16]}"
    output_path = eng / "evidence" / "output" / f"{evidence_id}.json"

    output_payload = {
        "schema_version": 2,
        "evidence_id": evidence_id,
        "created_at": utc_now(),
        "task_id": task_id,
        "skill_ids": skill_ids or [],
        "command_result": command_result,
    }
    atomic_write_json(output_path, output_payload)
    output_hash = sha256_file(output_path)

    ledger = evidence_ledger_path(project_root)
    with ProjectLock(eng):
        record = {
            "schema_version": 2,
            "evidence_id": evidence_id,
            "type": "command_execution",
            "created_at": utc_now(),
            "task_id": task_id,
            "skill_ids": skill_ids or [],
            "claim": f"Command {command_result.get('command_id')} returned {command_result.get('result')}",
            "result": command_result.get("result"),
            "command_id": command_result.get("command_id"),
            "exit_code": command_result.get("exit_code"),
            "duration_seconds": command_result.get("duration_seconds"),
            "output_file": safe_relative(output_path, project_root),
            "output_sha256": output_hash,
            "environment": environment_summary(),
            "git": _git_metadata(project_root),
            "previous_hash": _last_hash(ledger),
        }
        record["record_hash"] = sha256_bytes(canonical_json_bytes(record))
        append_jsonl(ledger, record)

        record_path = eng / "evidence" / "records" / f"{evidence_id}.json"
        atomic_write_json(record_path, record)
    return {
        "evidence_id": evidence_id,
        "record_file": safe_relative(record_path, project_root),
        "output_file": safe_relative(output_path, project_root),
        "record_hash": record["record_hash"],
        "output_sha256": output_hash,
    }

def record_manual_evidence(project_root: Path, *, claim: str, result: str,
                           method: str, source_path: str = "", owner: str = "",
                           task_id: str | None = None,
                           skill_ids: list[int] | None = None,
                           notes: str = "") -> dict[str, Any]:
    eng = ensure_layout(project_root)
    evidence_id = f"EV-{uuid.uuid4().hex[:16]}"
    ledger = evidence_ledger_path(project_root)
    source_hash = None
    if source_path:
        candidate = (project_root / source_path).resolve()
        try:
            relative_source = candidate.relative_to(project_root.resolve())
        except ValueError as exc:
            raise ValueError("Evidence source_path must remain inside the project root.") from exc
        if not candidate.is_file():
            raise FileNotFoundError(f"Evidence source file does not exist: {relative_source.as_posix()}")
        source_path = relative_source.as_posix()
        source_hash = sha256_file(candidate)

    with ProjectLock(eng):
        record = {
            "schema_version": 2,
            "evidence_id": evidence_id,
            "type": "manual_or_external",
            "created_at": utc_now(),
            "task_id": task_id,
            "skill_ids": skill_ids or [],
            "claim": claim,
            "result": result,
            "method": method,
            "source_path": source_path,
            "source_sha256": source_hash,
            "owner": owner,
            "notes": notes,
            "environment": environment_summary(),
            "git": _git_metadata(project_root),
            "previous_hash": _last_hash(ledger),
        }
        record["record_hash"] = sha256_bytes(canonical_json_bytes(record))
        append_jsonl(ledger, record)
        record_path = eng / "evidence" / "records" / f"{evidence_id}.json"
        atomic_write_json(record_path, record)
    return record

def verify_evidence(project_root: Path) -> dict[str, Any]:
    ledger = evidence_ledger_path(project_root)
    findings: list[dict[str, Any]] = []
    count = 0
    previous = None
    seen_ids: set[str] = set()
    records_dir = engineering_dir(project_root) / "evidence" / "records"

    if not ledger.exists():
        return {"valid": False, "count": 0, "findings": [{"code": "NO_LEDGER", "message": "Evidence ledger does not exist."}]}

    with ledger.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                findings.append({"code": "INVALID_JSON", "line": line_number, "message": str(exc)})
                continue

            stored_hash = record.get("record_hash")
            payload = dict(record)
            payload.pop("record_hash", None)
            calculated = sha256_bytes(canonical_json_bytes(payload))
            if stored_hash != calculated:
                findings.append({"code": "RECORD_HASH_MISMATCH", "line": line_number, "evidence_id": record.get("evidence_id")})
            if record.get("previous_hash") != previous:
                findings.append({"code": "CHAIN_MISMATCH", "line": line_number, "evidence_id": record.get("evidence_id")})

            evidence_id = record.get("evidence_id")
            if not evidence_id:
                findings.append({"code": "MISSING_EVIDENCE_ID", "line": line_number})
            elif evidence_id in seen_ids:
                findings.append({"code": "DUPLICATE_EVIDENCE_ID", "line": line_number, "evidence_id": evidence_id})
            else:
                seen_ids.add(evidence_id)

            if evidence_id:
                record_file = records_dir / f"{evidence_id}.json"
                if not record_file.exists():
                    findings.append({"code": "MISSING_RECORD_FILE", "line": line_number, "evidence_id": evidence_id})
                else:
                    try:
                        record_copy = json.loads(record_file.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError) as exc:
                        findings.append({"code": "INVALID_RECORD_FILE", "line": line_number, "evidence_id": evidence_id, "message": str(exc)})
                    else:
                        if canonical_json_bytes(record_copy) != canonical_json_bytes(record):
                            findings.append({"code": "RECORD_FILE_MISMATCH", "line": line_number, "evidence_id": evidence_id})

            output_file = record.get("output_file")
            output_hash = record.get("output_sha256")
            if output_file and output_hash:
                output_path = (project_root / output_file).resolve()
                try:
                    output_path.relative_to(project_root.resolve())
                except ValueError:
                    findings.append({"code": "OUTPUT_PATH_ESCAPE", "line": line_number})
                else:
                    if not output_path.exists():
                        findings.append({"code": "MISSING_OUTPUT", "line": line_number, "path": output_file})
                    elif sha256_file(output_path) != output_hash:
                        findings.append({"code": "OUTPUT_HASH_MISMATCH", "line": line_number, "path": output_file})

            source_path = record.get("source_path")
            source_hash = record.get("source_sha256")
            if source_path and source_hash:
                candidate = (project_root / source_path).resolve()
                try:
                    candidate.relative_to(project_root.resolve())
                except ValueError:
                    findings.append({"code": "SOURCE_PATH_ESCAPE", "line": line_number, "path": source_path})
                else:
                    if not candidate.exists() or not candidate.is_file():
                        findings.append({"code": "MISSING_SOURCE", "line": line_number, "path": source_path})
                    elif sha256_file(candidate) != source_hash:
                        findings.append({"code": "SOURCE_CHANGED", "line": line_number, "path": source_path})

            previous = stored_hash

    return {"valid": not findings, "count": count, "findings": findings}
