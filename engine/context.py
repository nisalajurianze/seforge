from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import atomic_write_text, load_json
from .routing import select_task_skills
from .state import command_registry_path, engineering_dir, skill_manifest_path
from .tasks import load_task, save_task

DEFAULT_BUDGETS = {
    "small": 4000,
    "normal": 8000,
    "complex": 16000,
}

def _words(text: str) -> int:
    return len(text.split())

def _trim(text: str, budget: int) -> str:
    words = text.split()
    if len(words) <= budget:
        return text
    return " ".join(words[:budget]) + f"\n\n...[trimmed to {budget} words]"

def build_task_context(project_root: Path, pack_root: Path, task_id: str,
                       budget_name: str = "normal", max_skills: int = 8) -> dict[str, Any]:
    budget = DEFAULT_BUDGETS.get(budget_name, DEFAULT_BUDGETS["normal"])
    task = load_task(project_root, task_id)
    eng = engineering_dir(project_root)
    context = load_json(eng / "project-context.json", {})
    facts = load_json(eng / "reports" / "project-facts.json", {})
    manifest = load_json(skill_manifest_path(project_root), {"skills": []})
    commands = load_json(command_registry_path(project_root), {"commands": []})
    plan_text = ""
    if task.get("plan_path"):
        candidate = project_root / task["plan_path"]
        if candidate.exists():
            plan_text = candidate.read_text(encoding="utf-8")

    selected_ids = select_task_skills(task, manifest, max_skills=max_skills)
    task["skill_ids"] = selected_ids
    save_task(project_root, task)

    manifest_by_id = {int(s["id"]): s for s in manifest.get("skills", [])}
    skill_sections = []
    loaded_paths = []

    workflow = task.get("workflow_skill", "wf-feature-delivery")
    workflow_path = pack_root / "agent-skills" / workflow / "SKILL.md"
    if workflow_path.exists():
        workflow_text = workflow_path.read_text(encoding="utf-8")
        skill_sections.append(f"## Workflow Skill — {workflow}\n\n{workflow_text}")
        loaded_paths.append(workflow_path.relative_to(pack_root).as_posix())

    for sid in selected_ids:
        item = manifest_by_id.get(sid)
        if not item:
            continue
        skill_path = pack_root / item["skill_path"]
        if not skill_path.exists():
            continue
        skill_sections.append(f"## Engineering Skill — SE-{sid:02d}\n\n{skill_path.read_text(encoding='utf-8')}")
        loaded_paths.append(skill_path.relative_to(pack_root).as_posix())

    command_summary = [
        {
            "id": c["id"],
            "category": c["category"],
            "rendered": c["rendered"],
            "trust": c["trust"],
            "risk": c["risk"],
            "available": c.get("available"),
        }
        for c in commands.get("commands", [])
    ]

    header = f"""# Task Context Bundle

## Task

```json
{json.dumps(task, indent=2, ensure_ascii=False)}
```

## Project facts

```json
{json.dumps(facts, indent=2, ensure_ascii=False)}
```

## Project context

```json
{json.dumps(context, indent=2, ensure_ascii=False)}
```

## Discovered verification commands

```json
{json.dumps(command_summary, indent=2, ensure_ascii=False)}
```

## Approved or draft plan

{plan_text or "No task ExecPlan exists yet."}

"""
    remaining = max(1000, budget - _words(header))
    skills_text = "\n\n".join(skill_sections)
    content = header + "\n" + _trim(skills_text, remaining)
    pretrim_words = _words(content)
    if pretrim_words > budget:
        content = _trim(content, budget)
    bundle_path = eng / "tasks" / f"{task_id}.context.md"
    atomic_write_text(bundle_path, content)

    result = {
        "task_id": task_id,
        "bundle_path": bundle_path.relative_to(project_root).as_posix(),
        "budget_words": budget,
        "actual_words": _words(content),
        "selected_skill_ids": selected_ids,
        "loaded_skill_paths": loaded_paths,
        "trimmed": _words(skills_text) > remaining or pretrim_words > budget,
    }
    return result
