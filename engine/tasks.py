from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

from .common import atomic_write_json, load_json, utc_now
from .policy import RISK_LEVELS
from .state import ensure_layout, engineering_dir, task_path

WORKFLOW_RULES = [
    ("wf-security-review", ["security", "auth", "permission", "vulnerability", "secret", "mcp", "agent"]),
    ("wf-data-migration", ["migration", "schema", "database", "data move", "cutover"]),
    ("wf-bugfix", ["bug", "fix", "regression", "failing", "incorrect", "defect"]),
    ("wf-performance-investigation", ["performance", "slow", "latency", "throughput", "capacity"]),
    ("wf-architecture-review", ["architecture", "redesign", "decompose", "platform change"]),
    ("wf-release-readiness", ["release", "deploy", "production", "rollout"]),
    ("wf-incident-response", ["incident", "outage", "breach", "corruption"]),
    ("wf-dependency-update", ["dependency", "upgrade", "runtime update", "framework update"]),
    ("wf-project-retirement", ["retire", "decommission", "shutdown product"]),
]

HIGH_IMPACT_SIGNALS = [
    "production", "delete", "drop", "destroy", "payment", "money", "credential",
    "secret", "private key", "patient", "medical", "safety", "firmware", "identity",
]
MATERIAL_SIGNALS = [
    "architecture", "migration", "schema", "dependency", "authentication",
    "authorization", "encryption", "external service", "public api", "breaking change",
]

def classify_task_risk(name: str, description: str, files: list[str] | None = None) -> tuple[str, list[str]]:
    text = " ".join([name, description, " ".join(files or [])]).lower()
    reasons = []
    risk = "R1"
    for signal in MATERIAL_SIGNALS:
        if signal in text:
            risk = "R2"
            reasons.append(f"material signal: {signal}")
    for signal in HIGH_IMPACT_SIGNALS:
        if signal in text:
            risk = "R3"
            reasons.append(f"high-impact signal: {signal}")
    if not reasons:
        reasons.append("local reversible task by current evidence")
    return risk, reasons

def choose_workflow(name: str, description: str) -> str:
    text = f"{name} {description}".lower()
    for workflow, signals in WORKFLOW_RULES:
        if any(signal in text for signal in signals):
            return workflow
    return "wf-feature-delivery"

def create_task(project_root: Path, *, name: str, description: str,
                files: list[str] | None = None, tags: list[str] | None = None,
                owner: str = "unassigned", acceptance_criteria: list[str] | None = None,
                task_type: str | None = None) -> dict[str, Any]:
    ensure_layout(project_root)
    task_id = f"TSK-{uuid.uuid4().hex[:12]}"
    risk, reasons = classify_task_risk(name, description, files)
    workflow = task_type or choose_workflow(name, description)
    task = {
        "schema_version": 2,
        "id": task_id,
        "name": name,
        "description": description,
        "status": "planned",
        "owner": owner,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "workflow_skill": workflow,
        "risk": risk,
        "risk_reasons": reasons,
        "requires_explicit_approval": RISK_LEVELS[risk] >= RISK_LEVELS["R3"],
        "files": files or [],
        "tags": tags or [],
        "skill_ids": [],
        "acceptance_criteria": acceptance_criteria or [],
        "acceptance_evidence": {},
        "non_goals": [],
        "assumptions": [],
        "questions": [],
        "decisions": [],
        "plan_path": None,
        "verification_command_ids": [],
        "evidence_ids": [],
        "findings": [],
        "residual_risks": [],
        "rollback": "",
        "user_visible_outcome": "",
        "completion_statement": "",
    }
    atomic_write_json(task_path(project_root, task_id), task)
    return task

def load_task(project_root: Path, task_id: str) -> dict[str, Any]:
    path = task_path(project_root, task_id)
    task = load_json(path)
    if not task:
        raise FileNotFoundError(f"Task not found: {task_id}")
    return task

def save_task(project_root: Path, task: dict[str, Any]) -> None:
    task["updated_at"] = utc_now()
    atomic_write_json(task_path(project_root, task["id"]), task)

def list_tasks(project_root: Path) -> list[dict[str, Any]]:
    eng = engineering_dir(project_root)
    result = []
    for path in sorted((eng / "tasks").glob("*.json")):
        task = load_json(path, {})
        if task:
            result.append(task)
    return result

def generate_exec_plan(project_root: Path, task: dict[str, Any]) -> Path:
    ensure_layout(project_root)
    plan_path = engineering_dir(project_root) / "plans" / f"{task['id']}.md"
    acceptance = task.get("acceptance_criteria") or ["Define measurable acceptance criteria before implementation."]
    lines = [
        f"# ExecPlan — {task['name']}",
        "",
        f"- Task: `{task['id']}`",
        f"- Risk: `{task['risk']}`",
        f"- Owner: `{task.get('owner','unassigned')}`",
        f"- Workflow: `{task.get('workflow_skill')}`",
        "",
        "## Purpose and user-visible outcome",
        "",
        task.get("description", ""),
        "",
        "## Current state",
        "",
        "Inspect and update this section with the relevant architecture, files, behavior, tests, and constraints.",
        "",
        "## Scope",
        "",
        "- In scope:",
        *[f"  - {x}" for x in (task.get("files") or ["Determine affected files during inspection."])],
        "- Non-goals:",
        *[f"  - {x}" for x in (task.get("non_goals") or ["No unrelated refactoring."])],
        "",
        "## Acceptance criteria",
        "",
        *[f"- [ ] {x}" for x in acceptance],
        "",
        "## Decisions and assumptions",
        "",
        *([f"- {x}" for x in task.get("assumptions", [])] or ["- Record facts, inferences, defaults, alternatives, and approvals here."]),
        "",
        "## Security, privacy, data, operational, and migration impact",
        "",
        "Complete only applicable impacts; do not silently omit material effects.",
        "",
        "## Milestones",
        "",
        "### Milestone 1 — Inspect and baseline",
        "- Outcome: current behavior and affected components are understood.",
        "- Validation: run discovery and focused baseline checks.",
        "- Evidence: repository facts and command results.",
        "",
        "### Milestone 2 — Implement smallest coherent change",
        "- Outcome: requested behavior is implemented with scoped diffs.",
        "- Validation: focused tests and static checks.",
        "- Evidence: changed files and command records.",
        "",
        "### Milestone 3 — Validate and close",
        "- Outcome: acceptance criteria, affected regressions, documentation, and rollback are complete.",
        "- Validation: project-native verification and gate check.",
        "- Evidence: evidence ledger and final progress card.",
        "",
        "## Progress",
        "",
        "- [ ] Plan reviewed for current task facts.",
        "- [ ] Baseline captured.",
        "- [ ] Implementation complete.",
        "- [ ] Verification complete.",
        "- [ ] Documentation and evidence complete.",
        "",
        "## Discoveries",
        "",
        "Add timestamped discoveries that change the plan.",
        "",
        "## Validation commands",
        "",
        "Populate from `.engineering/commands/registry.json`; do not invent commands.",
        "",
        "## Final outcome",
        "",
        "Summarize delivered behavior, evidence, limitations, residual risks, and follow-up work.",
    ]
    plan_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    task["plan_path"] = plan_path.relative_to(project_root).as_posix()
    save_task(project_root, task)
    return plan_path
