from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .common import (
    PACK_VERSION, STATE_VERSION, ProjectLock, atomic_write_json, load_json, utc_now
)

STATE_DIRS = [
    "artifacts",
    "backups",
    "changes",
    "checkpoints",
    "commands",
    "conversation",
    "decisions",
    "evidence/records",
    "evidence/output",
    "plans",
    "reports",
    "risks",
    "snapshots",
    "tasks",
]

def engineering_dir(project_root: Path) -> Path:
    return project_root / ".engineering"

def ensure_layout(project_root: Path) -> Path:
    eng = engineering_dir(project_root)
    eng.mkdir(parents=True, exist_ok=True)
    for item in STATE_DIRS:
        (eng / item).mkdir(parents=True, exist_ok=True)
    migrate_state(project_root)
    return eng

def migrate_state(project_root: Path) -> None:
    eng = engineering_dir(project_root)
    state_path = eng / "state.json"
    state = load_json(state_path, {})
    old_version = int(state.get("state_version", 1 if state else 0))
    migrations: list[dict[str, Any]] = state.get("migrations", [])

    if old_version < 1:
        state = {
            "state_version": 1,
            "pack_version": PACK_VERSION,
            "initialized_at": utc_now(),
            "migrations": [],
        }
        old_version = 1

    if old_version < 2:
        # Preserve v1 directories while normalizing names used by v2.
        legacy_plan = eng / "plan"
        current_plans = eng / "plans"
        if legacy_plan.exists() and not any(current_plans.iterdir()):
            for child in legacy_plan.iterdir():
                destination = current_plans / child.name
                if child.is_dir():
                    shutil.copytree(child, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(child, destination)
        migrations.append({
            "from": old_version,
            "to": 2,
            "at": utc_now(),
            "notes": "Added v2 plans, command registry, evidence chain, snapshots, and task context state.",
        })
        state["state_version"] = 2

    state["pack_version"] = PACK_VERSION
    state["updated_at"] = utc_now()
    state["migrations"] = migrations
    atomic_write_json(state_path, state)

def project_context_path(project_root: Path) -> Path:
    return engineering_dir(project_root) / "project-context.json"

def skill_manifest_path(project_root: Path) -> Path:
    return engineering_dir(project_root) / "skill-manifest.json"

def command_registry_path(project_root: Path) -> Path:
    return engineering_dir(project_root) / "commands" / "registry.json"

def evidence_ledger_path(project_root: Path) -> Path:
    return engineering_dir(project_root) / "evidence" / "ledger.jsonl"

def task_path(project_root: Path, task_id: str) -> Path:
    return engineering_dir(project_root) / "tasks" / f"{task_id}.json"

def plan_status_path(project_root: Path) -> Path:
    return engineering_dir(project_root) / "plans" / "status.json"
