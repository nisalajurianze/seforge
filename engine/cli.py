from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

from .commands import discover_commands, execute_command
from .common import (
    PACK_VERSION, ProjectLock, atomic_write_json, atomic_write_text,
    load_json, safe_relative, utc_now
)
from .context import build_task_context
from .discovery import discover
from .doctor import run_doctor, SEVERITY_RANK
from .evidence import record_manual_evidence, verify_evidence
from .gates import release_gate, task_gate
from .integrity import generate_pack_integrity, verify_pack_integrity
from .policy import assess_command, scan_untrusted_text
from .routing import route_skills
from .state import (
    command_registry_path, engineering_dir, ensure_layout, plan_status_path,
    project_context_path, skill_manifest_path
)
from .tasks import (
    create_task, generate_exec_plan, list_tasks, load_task, save_task
)

PACK_ROOT = Path(__file__).resolve().parents[1]

def _root(value: str) -> Path:
    return Path(value).expanduser().resolve()

def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))

def _write_report(project_root: Path, name: str, value: Any) -> Path:
    path = engineering_dir(project_root) / "reports" / name
    atomic_write_json(path, value)
    return path

def _initial_context(project_root: Path, facts: dict[str, Any], args) -> dict[str, Any]:
    goal = getattr(args, "goal", None) or facts.get("description") or ""
    mode = getattr(args, "mode", None) or "guide_and_build"
    autonomy = getattr(args, "autonomy", None) or "ask_before_material_decisions"
    impact = getattr(args, "impact", None) or _infer_impact(facts)
    data_sensitivity = "unresolved"

    provenance = {
        "project_name": {"source": "repository", "confidence": "high"},
        "platforms": {"source": "repository", "confidence": facts.get("confidence", {}).get("platforms", "medium")},
        "goal": {"source": "user" if getattr(args, "goal", None) else "repository_or_default", "confidence": "high" if getattr(args, "goal", None) else "medium"},
        "impact_level": {"source": "user" if getattr(args, "impact", None) else "inference", "confidence": "medium"},
        "data_sensitivity": {"source": "unresolved", "confidence": "none"},
    }
    return {
        "schema_version": 2,
        "updated_at": utc_now(),
        "project_name": facts.get("project_name", project_root.name),
        "goal": goal,
        "mode": mode,
        "autonomy": autonomy,
        "communication": "material_updates_only",
        "impact_level": impact,
        "data_sensitivity": data_sensitivity,
        "users": [],
        "stakeholders": [],
        "quality_priorities": ["security", "reliability", "maintainability", "usability", "delivery"],
        "platforms": facts.get("platforms", []),
        "domains": sorted(facts.get("domains", {}).keys()),
        "constraints": [],
        "assumptions": [
            {
                "id": "A-001",
                "statement": "Existing project conventions are preferred when safe and maintainable.",
                "status": "active",
                "source": "pack-default",
                "review_trigger": "A convention conflicts with security, maintainability, or the requested outcome.",
            }
        ],
        "provenance": provenance,
        "unresolved": _material_questions(facts, goal, data_sensitivity, impact),
    }

def _infer_impact(facts: dict[str, Any]) -> str:
    domains = set(facts.get("domains", {}).keys())
    if domains & {"healthcare", "payments"}:
        return "L3"
    if facts.get("signals", {}).get("existing_code"):
        return "L2"
    return "L1"

def _material_questions(facts: dict[str, Any], goal: str, data_sensitivity: str, impact: str) -> list[dict[str, Any]]:
    questions = []
    if not goal:
        questions.append({
            "id": "Q-GOAL",
            "question": "What result should this project deliver?",
            "why": "The outcome controls scope and acceptance criteria.",
            "recommended": "Improve the existing project without changing unrelated behavior.",
            "materiality": "high",
        })
    if data_sensitivity == "unresolved":
        questions.append({
            "id": "Q-DATA",
            "question": "Does the project handle personal, financial, health, location, credential, or other sensitive data?",
            "why": "This changes security, privacy, logging, retention, and release controls.",
            "recommended": "Treat data conservatively until a data inventory proves otherwise.",
            "materiality": "high",
        })
    if impact in {"L3", "L4"}:
        questions.append({
            "id": "Q-IMPACT",
            "question": "Could a failure cause major financial, legal, safety, or irreversible harm?",
            "why": "High impact requires stronger review and evidence.",
            "recommended": f"Keep the current {impact} baseline until confirmed.",
            "materiality": "high",
        })
    if not facts.get("signals", {}).get("tests_present"):
        questions.append({
            "id": "Q-TESTS",
            "question": "Is there an external or undocumented test process the repository does not show?",
            "why": "No tests were detected, so release evidence may be incomplete.",
            "recommended": "Create a minimal automated regression baseline.",
            "materiality": "medium",
        })
    return questions[:3]

def _create_strategy(project_root: Path, context: dict[str, Any], facts: dict[str, Any],
                     manifest: dict[str, Any], safe_work_authorized: bool = False) -> tuple[Path, dict[str, Any]]:
    eng = engineering_dir(project_root)
    active = [s for s in manifest.get("skills", []) if s.get("status") == "active"]
    lines = [
        f"# Project Strategy — {context.get('project_name')}",
        "",
        f"- Goal: {context.get('goal') or 'Pending confirmation'}",
        f"- Mode: `{context.get('mode')}`",
        f"- Autonomy: `{context.get('autonomy')}`",
        f"- Impact: `{context.get('impact_level')}`",
        f"- Safe reversible work authorized: `{safe_work_authorized}`",
        "",
        "## Observed project facts",
        "",
        f"- Platforms: {', '.join(facts.get('platforms', [])) or 'unknown'}",
        f"- Stacks: {', '.join(facts.get('stacks', [])) or 'unknown'}",
        f"- Source files: {facts.get('counts', {}).get('source_files', 0)}",
        f"- Tests detected: {facts.get('signals', {}).get('tests_present')}",
        f"- CI detected: {facts.get('signals', {}).get('ci_present')}",
        f"- Migrations detected: {facts.get('signals', {}).get('migrations_present')}",
        "",
        "## Strategy",
        "",
        "1. Preserve existing correct behavior and inspect before changing.",
        "2. Work in small reviewable tasks with explicit acceptance criteria.",
        "3. Use project-native verification commands after review.",
        "4. Load only task-relevant workflow and engineering skills.",
        "5. Record decisions, risks, and tamper-evident evidence.",
        "6. Ask the user only for material, costly, sensitive, destructive, or irreversible decisions.",
        "",
        "## Active engineering areas",
        "",
        *[f"- SE-{int(s['id']):02d} — {s['name']} ({s['confidence']})" for s in active],
        "",
        "## Unresolved material questions",
        "",
        *([f"- {q['question']} Recommended default: {q['recommended']}" for q in context.get("unresolved", [])] or ["- None at this time."]),
        "",
        "## Approval model",
        "",
        "- R0 read-only work may proceed.",
        "- R1 reversible local work may proceed when safe work is authorized.",
        "- R2 material work requires a recorded project decision or approved ExecPlan.",
        "- R3 high-impact work requires explicit user/authority approval and recovery.",
        "- R4 prohibited work must stop.",
    ]
    strategy_path = eng / "plans" / "PROJECT-STRATEGY.md"
    atomic_write_text(strategy_path, "\n".join(lines) + "\n")
    status = {
        "schema_version": 2,
        "updated_at": utc_now(),
        "strategy": "provisional",
        "safe_work_authorized": safe_work_authorized,
        "approved_risk_levels": ["R0", "R1"] if safe_work_authorized else ["R0"],
        "approval_records": [],
        "unresolved_material_questions": [q["id"] for q in context.get("unresolved", []) if q.get("materiality") == "high"],
    }
    atomic_write_json(plan_status_path(project_root), status)
    return strategy_path, status

def cmd_init(args) -> int:
    project_root = _root(args.target)
    project_root.mkdir(parents=True, exist_ok=True)
    eng = ensure_layout(project_root)
    with ProjectLock(eng):
        facts = discover(project_root)
        atomic_write_json(eng / "reports" / "project-facts.json", facts)
        context = _initial_context(project_root, facts, args)
        atomic_write_json(project_context_path(project_root), context)
        manifest = route_skills(project_root, PACK_ROOT, facts, context)
        registry = discover_commands(project_root, facts)
        strategy_path, status = _create_strategy(
            project_root, context, facts, manifest,
            safe_work_authorized=bool(getattr(args, "delegate_safe_work", False)),
        )
    result = {
        "initialized": True,
        "pack_version": PACK_VERSION,
        "project": context["project_name"],
        "facts_path": safe_relative(eng / "reports" / "project-facts.json", project_root),
        "context_path": safe_relative(project_context_path(project_root), project_root),
        "manifest_path": safe_relative(skill_manifest_path(project_root), project_root),
        "command_count": len(registry.get("commands", [])),
        "strategy_path": safe_relative(strategy_path, project_root),
        "material_questions": context.get("unresolved", [])[:3],
    }
    _print_json(result if args.json else _brief_from_state(project_root))
    return 0

def cmd_quickstart(args) -> int:
    return cmd_init(args)

def cmd_route(args) -> int:
    project_root = _root(args.target)
    eng = ensure_layout(project_root)
    with ProjectLock(eng):
        facts = discover(project_root)
        atomic_write_json(eng / "reports" / "project-facts.json", facts)
        context = load_json(project_context_path(project_root), {})
        manifest = route_skills(project_root, PACK_ROOT, facts, context)
    _print_json(manifest if args.json else {
        "active": len([s for s in manifest["skills"] if s["status"] == "active"]),
        "recommended": len([s for s in manifest["skills"] if s["status"] == "recommended"]),
        "profiles": manifest["matched_profiles"],
    })
    return 0

def cmd_commands_discover(args) -> int:
    project_root = _root(args.target)
    facts = load_json(engineering_dir(project_root) / "reports" / "project-facts.json", None)
    registry = discover_commands(project_root, facts)
    _print_json(registry if args.json else {
        "count": len(registry["commands"]),
        "commands": [{
            "id": c["id"], "category": c["category"], "risk": c["risk"],
            "trust": c["trust"], "available": c["available"], "rendered": c["rendered"]
        } for c in registry["commands"]],
    })
    return 0

def cmd_commands_review(args) -> int:
    project_root = _root(args.target)
    path = command_registry_path(project_root)
    registry = load_json(path, {"commands": []})
    found = False
    for command in registry["commands"]:
        if command["id"] == args.command_id:
            command["reviewed"] = True
            command["reviewed_by"] = args.reviewer
            command["reviewed_at"] = utc_now()
            command["reviewed_definition_hash"] = command.get("definition_hash")
            command["reviewed_source_sha256"] = command.get("source_sha256")
            found = True
            break
    if not found:
        print(f"Unknown command: {args.command_id}", file=sys.stderr)
        return 2
    atomic_write_json(path, registry)
    print(f"Reviewed {args.command_id}")
    return 0

def _link_task_evidence(project_root: Path, task_id: str, evidence_id: str, criterion_indexes: list[int] | None = None) -> None:
    task = load_task(project_root, task_id)
    if evidence_id not in task.setdefault("evidence_ids", []):
        task["evidence_ids"].append(evidence_id)
    criteria = task.get("acceptance_criteria", [])
    mapping = task.setdefault("acceptance_evidence", {})
    for index in criterion_indexes or []:
        if index < 0 or index >= len(criteria):
            raise ValueError(f"Acceptance criterion index {index} is out of range for task {task_id}.")
        linked = mapping.setdefault(str(index), [])
        if evidence_id not in linked:
            linked.append(evidence_id)
    save_task(project_root, task)


def cmd_verify(args) -> int:
    project_root = _root(args.target)
    registry = load_json(command_registry_path(project_root), {"commands": []})
    by_id = {c["id"]: c for c in registry.get("commands", [])}
    selected = args.command_id or []
    if args.category:
        selected += [c["id"] for c in registry.get("commands", []) if c["category"] in args.category]
    selected = list(dict.fromkeys(selected))
    if not selected:
        _print_json({"commands": registry.get("commands", []), "message": "Select --command-id or --category."})
        return 0

    results = []
    failed = False
    for command_id in selected:
        command = by_id.get(command_id)
        if not command:
            results.append({"command_id": command_id, "error": "not found"})
            failed = True
            continue
        try:
            result = execute_command(
                project_root, command,
                trust_project_scripts=args.trust_project_scripts,
                allow_network=args.allow_network,
                explicit_approval=args.explicit_approval,
                timeout_seconds=args.timeout,
                task_id=args.task_id,
                skill_ids=args.skill_id or [],
            )
            if args.task_id and result.get("evidence"):
                evidence_id = result["evidence"]["evidence_id"]
                _link_task_evidence(project_root, args.task_id, evidence_id, args.criterion_index)
                task = load_task(project_root, args.task_id)
                if command_id not in task.setdefault("verification_command_ids", []):
                    task["verification_command_ids"].append(command_id)
                for sid in args.skill_id or []:
                    if sid not in task.setdefault("skill_ids", []):
                        task["skill_ids"].append(sid)
                save_task(project_root, task)
            results.append(result)
            failed = failed or result["exit_code"] != 0
        except Exception as exc:
            results.append({"command_id": command_id, "error": str(exc)})
            failed = True
            if not args.keep_going:
                break
    _print_json({"results": results})
    return 1 if failed else 0

def cmd_task_create(args) -> int:
    project_root = _root(args.target)
    task = create_task(
        project_root,
        name=args.name,
        description=args.description,
        files=args.file or [],
        tags=args.tag or [],
        owner=args.owner,
        acceptance_criteria=args.acceptance or [],
        task_type=args.workflow,
    )
    if args.plan or task["risk"] in {"R2", "R3", "R4"}:
        plan = generate_exec_plan(project_root, task)
        task = load_task(project_root, task["id"])
    result = build_task_context(project_root, PACK_ROOT, task["id"], budget_name=args.budget)
    _print_json({"task": task, "context": result})
    return 0

def cmd_task_list(args) -> int:
    tasks = list_tasks(_root(args.target))
    _print_json([{
        "id": t["id"], "name": t["name"], "status": t["status"],
        "risk": t["risk"], "workflow": t["workflow_skill"]
    } for t in tasks])
    return 0

def cmd_task_show(args) -> int:
    _print_json(load_task(_root(args.target), args.task_id))
    return 0

def cmd_task_context(args) -> int:
    result = build_task_context(
        _root(args.target), PACK_ROOT, args.task_id,
        budget_name=args.budget, max_skills=args.max_skills,
    )
    _print_json(result)
    return 0

def cmd_task_plan(args) -> int:
    project_root = _root(args.target)
    task = load_task(project_root, args.task_id)
    path = generate_exec_plan(project_root, task)
    print(path)
    return 0

def cmd_task_status(args) -> int:
    project_root = _root(args.target)
    task = load_task(project_root, args.task_id)
    plan_status = load_json(plan_status_path(project_root), {})
    target_status = args.status

    if target_status == "in_progress":
        risk = task.get("risk", "R1")
        approved_levels = set(plan_status.get("approved_risk_levels", []))
        task_approved = bool(task.get("approved_to_start"))
        if risk == "R4":
            print("R4 tasks are prohibited by default and cannot be started.", file=sys.stderr)
            return 1
        if risk == "R1" and not (plan_status.get("safe_work_authorized") or task_approved):
            print("R1 task requires safe-work authorization or task approval.", file=sys.stderr)
            return 1
        if risk == "R2" and not ("R2" in approved_levels or task_approved):
            print("R2 task requires approved strategy or explicit task approval.", file=sys.stderr)
            return 1
        if risk == "R3" and not task_approved:
            print("R3 task requires explicit task-specific approval.", file=sys.stderr)
            return 1

    if target_status in {"complete", "closed"}:
        gate = task_gate(project_root, task["id"])
        if not gate.get("ready") and not args.force:
            _print_json({
                "error": "Task completion gate failed.",
                "gate": gate,
                "instruction": "Resolve blocking checks. Use --force only with an authorized documented exception."
            })
            return 1
        if args.force and not args.force_reason:
            print("--force requires --force-reason.", file=sys.stderr)
            return 1
        if args.force:
            task.setdefault("decisions", []).append({
                "type": "forced_completion_exception",
                "at": utc_now(),
                "reason": args.force_reason,
                "approved_by": args.approved_by or "unrecorded",
            })

    task["status"] = target_status
    if args.completion_statement:
        task["completion_statement"] = args.completion_statement
    save_task(project_root, task)
    _print_json(task)
    return 0

def cmd_evidence_add(args) -> int:
    project_root = _root(args.target)
    record = record_manual_evidence(
        project_root,
        claim=args.claim,
        result=args.result,
        method=args.method,
        source_path=args.path,
        owner=args.owner,
        task_id=args.task_id,
        skill_ids=args.skill_id or [],
        notes=args.notes,
    )
    if args.task_id:
        _link_task_evidence(project_root, args.task_id, record["evidence_id"], args.criterion_index)
        task = load_task(project_root, args.task_id)
        for sid in args.skill_id or []:
            if sid not in task.setdefault("skill_ids", []):
                task["skill_ids"].append(sid)
        save_task(project_root, task)
    _print_json(record)
    return 0

def cmd_evidence_verify(args) -> int:
    result = verify_evidence(_root(args.target))
    _print_json(result)
    return 0 if result["valid"] else 1

def cmd_gate(args) -> int:
    project_root = _root(args.target)
    result = task_gate(project_root, args.task_id) if args.gate == "task" else release_gate(project_root)
    _write_report(project_root, f"gate-{args.gate}{'-'+args.task_id if args.task_id else ''}.json", result)
    _print_json(result)
    return 0 if result["ready"] else 1

def cmd_doctor(args) -> int:
    project_root = _root(args.target)
    result = run_doctor(project_root, PACK_ROOT)
    _write_report(project_root, "doctor.json", result)
    _print_json(result)
    return 0 if result["healthy"] else 1

def cmd_integrity(args) -> int:
    if args.generate:
        if ".engineering" in PACK_ROOT.parts and not args.maintainer:
            print("Refusing to regenerate integrity inside an installed project without --maintainer.", file=sys.stderr)
            return 1
        if not args.maintainer:
            print("Integrity generation is a release-maintainer action. Pass --maintainer.", file=sys.stderr)
            return 1
        result = generate_pack_integrity(PACK_ROOT)
    else:
        result = verify_pack_integrity(PACK_ROOT)
    _print_json(result)
    return 0 if result.get("valid", True) else 1

def cmd_assess(args) -> int:
    _print_json(assess_command(args.command).to_dict())
    return 0

def cmd_scan_text(args) -> int:
    text = Path(args.path).read_text(encoding="utf-8", errors="ignore") if args.path else args.text
    findings = scan_untrusted_text(text)
    _print_json({"findings": findings})
    return 1 if findings else 0

def cmd_brief(args) -> int:
    _print_json(_brief_from_state(_root(args.target)))
    return 0

def cmd_snapshot(args) -> int:
    project_root = _root(args.target)
    eng = ensure_layout(project_root)
    name = args.name or utc_now().replace(":", "").replace("+", "_")
    archive = eng / "snapshots" / f"{name}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in eng.rglob("*"):
            if not path.is_file():
                continue
            if "skill-pack" in path.parts or "snapshots" in path.parts or path.name == ".sepack.lock":
                continue
            zf.write(path, path.relative_to(eng))
    print(archive)
    return 0

def cmd_approve(args) -> int:
    project_root = _root(args.target)
    status_path = plan_status_path(project_root)
    status = load_json(status_path, {
        "schema_version": 2, "strategy": "provisional", "safe_work_authorized": False,
        "approved_risk_levels": ["R0"], "approval_records": []
    })
    record = {
        "at": utc_now(),
        "approver": args.approver,
        "decision": args.decision,
        "scope": args.scope,
        "task_id": args.task_id,
        "notes": args.notes,
    }

    if args.decision == "approve-task":
        if not args.task_id:
            print("approve-task requires --task-id.", file=sys.stderr)
            return 2
        task = load_task(project_root, args.task_id)
        if task.get("risk") == "R4":
            print("R4 task cannot be approved through the normal workflow.", file=sys.stderr)
            return 1
        task["approved_to_start"] = True
        task.setdefault("decisions", []).append({
            "type": "task_start_approval",
            **record,
        })
        save_task(project_root, task)
        _print_json(task)
        return 0

    if args.decision == "accept-task-risk":
        if not args.task_id:
            print("accept-task-risk requires --task-id.", file=sys.stderr)
            return 2
        task = load_task(project_root, args.task_id)
        task.setdefault("decisions", []).append({
            "type": "residual_risk_acceptance",
            **record,
        })
        for risk in task.get("residual_risks", []):
            if isinstance(risk, dict) and not risk.get("disposition"):
                risk["disposition"] = "accepted"
                risk["accepted_by"] = args.approver
                risk["accepted_at"] = utc_now()
        save_task(project_root, task)
        _print_json(task)
        return 0

    if args.decision == "authorize-safe-work":
        status["safe_work_authorized"] = True
        status["approved_risk_levels"] = sorted(set(status.get("approved_risk_levels", []) + ["R0", "R1"]))
    elif args.decision == "approve-strategy":
        status["strategy"] = "approved"
        status["approved_risk_levels"] = sorted(set(status.get("approved_risk_levels", []) + ["R0", "R1", "R2"]))
    elif args.decision == "pause":
        status["strategy"] = "paused"
    status.setdefault("approval_records", []).append(record)
    status["updated_at"] = utc_now()
    atomic_write_json(status_path, status)
    _print_json(status)
    return 0

def _brief_from_state(project_root: Path) -> dict[str, Any]:
    eng = engineering_dir(project_root)
    facts = load_json(eng / "reports" / "project-facts.json", {})
    context = load_json(project_context_path(project_root), {})
    manifest = load_json(skill_manifest_path(project_root), {"skills": []})
    commands = load_json(command_registry_path(project_root), {"commands": []})
    plan = load_json(plan_status_path(project_root), {})
    tasks = list_tasks(project_root)
    open_tasks = [t for t in tasks if t.get("status") not in {"complete", "closed", "cancelled"}]
    evidence = verify_evidence(project_root)
    return {
        "Done": [
            f"Repository inspected: {bool(facts)}",
            f"Project-level skills routed: {len(manifest.get('skills', []))}",
            f"Verification commands discovered: {len(commands.get('commands', []))}",
            f"Evidence records: {evidence.get('count', 0)}",
        ],
        "Current": [
            f"Goal: {context.get('goal') or 'unresolved'}",
            f"Impact: {context.get('impact_level') or 'unresolved'}",
            f"Plan: {plan.get('strategy') or 'missing'}",
            f"Open tasks: {len(open_tasks)}",
        ],
        "Need from you": [
            q["question"] for q in context.get("unresolved", [])[:3]
        ],
        "Risks": [
            "Sensitive data status is unresolved." if context.get("data_sensitivity") == "unresolved" else f"Data sensitivity: {context.get('data_sensitivity')}",
            "Project-defined commands require review before execution.",
        ],
        "Next": [
            "Create the next task and acceptance criteria." if not open_tasks else f"Continue task {open_tasks[0]['id']}.",
            "Authorize only the risk level needed for the next action.",
        ],
    }

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sepack", description="Agent-native professional software engineering pack")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--target", default=".")

    p = sub.add_parser("init")
    add_common(p)
    p.add_argument("--goal")
    p.add_argument("--mode", default="guide_and_build")
    p.add_argument("--autonomy", default="ask_before_material_decisions")
    p.add_argument("--impact", choices=["L1", "L2", "L3", "L4"])
    p.add_argument("--delegate-safe-work", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("quickstart")
    add_common(p)
    p.add_argument("--goal")
    p.add_argument("--mode", default="guide_and_build")
    p.add_argument("--autonomy", default="ask_before_material_decisions")
    p.add_argument("--impact", choices=["L1", "L2", "L3", "L4"])
    p.add_argument("--delegate-safe-work", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_quickstart)

    p = sub.add_parser("route")
    add_common(p); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_route)

    p = sub.add_parser("commands")
    cmdsub = p.add_subparsers(dest="commands_action", required=True)
    q = cmdsub.add_parser("discover"); add_common(q); q.add_argument("--json", action="store_true"); q.set_defaults(func=cmd_commands_discover)
    q = cmdsub.add_parser("review"); add_common(q); q.add_argument("--command-id", required=True); q.add_argument("--reviewer", required=True); q.set_defaults(func=cmd_commands_review)

    p = sub.add_parser("verify")
    add_common(p)
    p.add_argument("--command-id", action="append")
    p.add_argument("--category", action="append", choices=["format","lint","typecheck","unit","integration","e2e","security","build","smoke","other"])
    p.add_argument("--trust-project-scripts", action="store_true")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--explicit-approval", action="store_true")
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--keep-going", action="store_true")
    p.add_argument("--task-id")
    p.add_argument("--skill-id", type=int, action="append")
    p.add_argument("--criterion-index", type=int, action="append", help="Link command evidence to a zero-based acceptance criterion index.")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("task")
    tasksub = p.add_subparsers(dest="task_action", required=True)
    q = tasksub.add_parser("create"); add_common(q)
    q.add_argument("--name", required=True); q.add_argument("--description", required=True)
    q.add_argument("--file", action="append"); q.add_argument("--tag", action="append")
    q.add_argument("--owner", default="unassigned"); q.add_argument("--acceptance", action="append")
    q.add_argument("--workflow"); q.add_argument("--plan", action="store_true")
    q.add_argument("--budget", choices=["small","normal","complex"], default="normal")
    q.set_defaults(func=cmd_task_create)
    q = tasksub.add_parser("list"); add_common(q); q.set_defaults(func=cmd_task_list)
    q = tasksub.add_parser("show"); add_common(q); q.add_argument("task_id"); q.set_defaults(func=cmd_task_show)
    q = tasksub.add_parser("context"); add_common(q); q.add_argument("task_id"); q.add_argument("--budget", choices=["small","normal","complex"], default="normal"); q.add_argument("--max-skills", type=int, default=8); q.set_defaults(func=cmd_task_context)
    q = tasksub.add_parser("plan"); add_common(q); q.add_argument("task_id"); q.set_defaults(func=cmd_task_plan)
    q = tasksub.add_parser("status"); add_common(q); q.add_argument("task_id"); q.add_argument("--status", required=True, choices=["planned","in_progress","blocked","review","complete","closed","cancelled"]); q.add_argument("--completion-statement"); q.add_argument("--force", action="store_true"); q.add_argument("--force-reason"); q.add_argument("--approved-by"); q.set_defaults(func=cmd_task_status)

    p = sub.add_parser("evidence")
    evsub = p.add_subparsers(dest="evidence_action", required=True)
    q = evsub.add_parser("add"); add_common(q)
    q.add_argument("--claim", required=True); q.add_argument("--result", choices=["pass","fail","partial","not-run"], required=True)
    q.add_argument("--method", required=True); q.add_argument("--path", default=""); q.add_argument("--owner", default="")
    q.add_argument("--task-id"); q.add_argument("--skill-id", type=int, action="append"); q.add_argument("--criterion-index", type=int, action="append"); q.add_argument("--notes", default="")
    q.set_defaults(func=cmd_evidence_add)
    q = evsub.add_parser("verify"); add_common(q); q.set_defaults(func=cmd_evidence_verify)

    p = sub.add_parser("gate")
    add_common(p); p.add_argument("gate", choices=["task","release"]); p.add_argument("--task-id"); p.set_defaults(func=cmd_gate)

    p = sub.add_parser("doctor"); add_common(p); p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("brief"); add_common(p); p.set_defaults(func=cmd_brief)

    p = sub.add_parser("integrity")
    p.add_argument("--generate", action="store_true"); p.add_argument("--maintainer", action="store_true"); p.set_defaults(func=cmd_integrity)

    p = sub.add_parser("assess-command")
    p.add_argument("--command", required=True); p.set_defaults(func=cmd_assess)

    p = sub.add_parser("scan-text")
    group = p.add_mutually_exclusive_group(required=True); group.add_argument("--text"); group.add_argument("--path")
    p.set_defaults(func=cmd_scan_text)

    p = sub.add_parser("snapshot"); add_common(p); p.add_argument("--name"); p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("approve")
    add_common(p); p.add_argument("--decision", choices=["authorize-safe-work","approve-strategy","approve-task","accept-task-risk","pause"], required=True)
    p.add_argument("--approver", required=True); p.add_argument("--scope", default="project"); p.add_argument("--task-id"); p.add_argument("--notes", default="")
    p.set_defaults(func=cmd_approve)

    # Compatibility aliases.
    p = sub.add_parser("scan"); add_common(p); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_route)
    p = sub.add_parser("audit"); add_common(p); p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("validate"); add_common(p); p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("release-check"); add_common(p); p.set_defaults(func=lambda a: cmd_gate(argparse.Namespace(target=a.target, gate="release", task_id=None)))
    p = sub.add_parser("status"); add_common(p); p.set_defaults(func=cmd_brief)

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "gate", None) == "task" and not getattr(args, "task_id", None):
        parser.error("gate task requires --task-id")
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, PermissionError, TimeoutError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        if os.environ.get("SEPACK_DEBUG") == "1":
            raise
        print(f"sepack: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
