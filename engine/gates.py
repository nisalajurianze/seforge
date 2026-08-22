from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import load_json, utc_now
from .evidence import verify_evidence
from .state import engineering_dir, plan_status_path, task_path
from .tasks import list_tasks, load_task

def _result(name: str, status: str, message: str, evidence: list[str] | None = None) -> dict[str, Any]:
    return {"name": name, "status": status, "message": message, "evidence": evidence or []}

def task_gate(project_root: Path, task_id: str) -> dict[str, Any]:
    task = load_task(project_root, task_id)
    checks = []

    checks.append(_result(
        "acceptance_criteria",
        "pass" if task.get("acceptance_criteria") else "block",
        "Acceptance criteria are defined." if task.get("acceptance_criteria") else "Acceptance criteria are missing.",
    ))
    checks.append(_result(
        "task_skills",
        "pass" if task.get("skill_ids") else "block",
        "Task-specific skills selected." if task.get("skill_ids") else "Task-specific skills were not selected.",
    ))

    plan_required = task.get("risk") in {"R2", "R3", "R4"}
    plan_exists = bool(task.get("plan_path") and (project_root / task["plan_path"]).exists())
    checks.append(_result(
        "exec_plan",
        "pass" if (not plan_required or plan_exists) else "block",
        "ExecPlan available." if plan_exists else ("ExecPlan not required for current risk." if not plan_required else "ExecPlan required."),
    ))

    evidence = _task_evidence(project_root, task_id)
    evidence_by_id = {e.get("evidence_id"): e for e in evidence}
    passing = [e for e in evidence if e.get("result") == "pass"]
    failing = [e for e in evidence if e.get("result") == "fail"]
    checks.append(_result(
        "verification_evidence",
        "block" if failing or not passing else "pass",
        f"{len(passing)} passing and {len(failing)} failing evidence records.",
        [e.get("evidence_id") for e in evidence],
    ))

    criteria = task.get("acceptance_criteria", [])
    mapping = task.get("acceptance_evidence", {})
    uncovered = []
    criterion_evidence = []
    for index, criterion in enumerate(criteria):
        linked_ids = list(dict.fromkeys(mapping.get(str(index), [])))
        linked_pass = [
            evidence_id for evidence_id in linked_ids
            if evidence_by_id.get(evidence_id, {}).get("result") == "pass"
        ]
        criterion_evidence.extend(linked_ids)
        if not linked_pass:
            uncovered.append({"index": index, "criterion": criterion, "linked_evidence": linked_ids})
    checks.append(_result(
        "acceptance_evidence_coverage",
        "pass" if criteria and not uncovered else "block",
        "Every acceptance criterion has linked passing evidence." if criteria and not uncovered
        else ("Acceptance criteria are missing." if not criteria else f"{len(uncovered)} acceptance criteria lack linked passing evidence."),
        list(dict.fromkeys(criterion_evidence)),
    ))

    unresolved = task.get("findings", []) + task.get("residual_risks", [])
    blocking = [x for x in unresolved if isinstance(x, dict) and x.get("severity") in {"high", "critical"} and not x.get("disposition")]
    checks.append(_result(
        "risk_disposition",
        "pass" if not blocking else "block",
        "No undisposed high/critical task risks." if not blocking else f"{len(blocking)} high/critical risks lack disposition.",
    ))

    integrity = verify_evidence(project_root)
    checks.append(_result(
        "evidence_integrity",
        "pass" if integrity.get("valid") else "block",
        "Evidence ledger integrity verified." if integrity.get("valid") else "Evidence ledger integrity failed.",
    ))

    ready = all(c["status"] in {"pass", "not-applicable"} for c in checks)
    return {"gate": "task", "task_id": task_id, "generated_at": utc_now(), "ready": ready, "checks": checks}

def release_gate(project_root: Path) -> dict[str, Any]:
    eng = engineering_dir(project_root)
    checks = []

    facts_exists = (eng / "reports" / "project-facts.json").exists()
    manifest_exists = (eng / "skill-manifest.json").exists()
    commands_exists = (eng / "commands" / "registry.json").exists()
    checks.append(_result("project_state", "pass" if facts_exists and manifest_exists and commands_exists else "block",
                          "Project facts, skill manifest, and command registry exist." if facts_exists and manifest_exists and commands_exists else "Required project state is incomplete."))

    tasks = list_tasks(project_root)
    open_tasks = [t for t in tasks if t.get("status") not in {"complete", "closed", "cancelled"}]
    checks.append(_result("open_tasks", "pass" if not open_tasks else "block",
                          "No open tasks." if not open_tasks else f"{len(open_tasks)} tasks remain open.",
                          [t["id"] for t in open_tasks]))

    completed = [t for t in tasks if t.get("status") in {"complete", "closed"}]
    checks.append(_result("completed_scope", "pass" if completed else "block",
                          f"{len(completed)} completed task(s)." if completed else "No completed task proves release scope."))

    failed_task_gates = []
    for task in completed:
        gate = task_gate(project_root, task["id"])
        if not gate.get("ready"):
            failed_task_gates.append({"task_id": task["id"], "checks": gate.get("checks", [])})
    checks.append(_result(
        "completed_task_gates",
        "pass" if completed and not failed_task_gates else "block",
        "Every completed task still satisfies its task gate." if completed and not failed_task_gates
        else ("No completed tasks are available." if not completed else f"{len(failed_task_gates)} completed task(s) fail their task gate."),
        [item["task_id"] for item in failed_task_gates],
    ))

    evidence = verify_evidence(project_root)
    checks.append(_result("evidence_integrity", "pass" if evidence.get("valid") and evidence.get("count", 0) else "block",
                          f"{evidence.get('count',0)} evidence records verified." if evidence.get("valid") else "Evidence integrity failed or no evidence exists."))

    plan_status = load_json(plan_status_path(project_root), {})
    strategy = plan_status.get("strategy")
    checks.append(_result("plan_approval", "pass" if strategy in {"approved", "approved_with_changes", "approved_by_delegation"} else "block",
                          f"Plan status: {strategy or 'missing'}."))

    # Structural operational readiness. These are explicitly not claims of behavior.
    for name, rel in [
        ("rollback", "artifacts/rollback.md"),
        ("operations", "artifacts/operations.md"),
        ("release_notes", "artifacts/release-notes.md"),
    ]:
        exists = (eng / rel).exists()
        checks.append(_result(name, "pass" if exists else "not-proven",
                              f"{rel} exists." if exists else f"{rel} is not present; determine applicability."))

    ready = all(c["status"] in {"pass", "not-applicable"} for c in checks)
    return {"gate": "release", "generated_at": utc_now(), "ready": ready, "checks": checks}

def _task_evidence(project_root: Path, task_id: str) -> list[dict[str, Any]]:
    records = []
    records_dir = engineering_dir(project_root) / "evidence" / "records"
    for path in records_dir.glob("*.json"):
        record = load_json(path, {})
        if record.get("task_id") == task_id:
            records.append(record)
    return records
