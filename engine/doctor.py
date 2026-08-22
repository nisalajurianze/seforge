from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import load_json, safe_relative, utc_now
from .evidence import verify_evidence
from .integrity import verify_pack_integrity
from .state import command_registry_path, engineering_dir, skill_manifest_path

SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

def _finding(severity: str, code: str, message: str, **extra) -> dict[str, Any]:
    return {"severity": severity, "code": code, "message": message, **extra}

def run_doctor(project_root: Path, pack_root: Path) -> dict[str, Any]:
    eng = engineering_dir(project_root)
    findings: list[dict[str, Any]] = []

    if not eng.exists():
        findings.append(_finding("high", "NOT_INITIALIZED", ".engineering state does not exist."))
    for rel in ["project-context.json", "skill-manifest.json", "reports/project-facts.json", "commands/registry.json"]:
        if not (eng / rel).exists():
            findings.append(_finding("high", "MISSING_STATE", f"Missing .engineering/{rel}"))

    manifest = load_json(skill_manifest_path(project_root), {"skills": []})
    active = [s for s in manifest.get("skills", []) if s.get("status") == "active"]
    if not active:
        findings.append(_finding("high", "NO_ACTIVE_SKILLS", "No active engineering skills were routed."))
    unassigned = [s for s in active if s.get("owner") in {None, "", "unassigned"}]
    provisional = [s for s in active if s.get("owner_status") == "provisional"]
    if unassigned:
        findings.append(_finding("medium", "SKILL_OWNER_UNASSIGNED", f"{len(unassigned)} active skills have no owner."))
    if provisional:
        findings.append(_finding("low", "PROVISIONAL_OWNERSHIP", f"{len(provisional)} active skills use the provisional project-team owner. Confirm a real accountable owner before high-impact release."))

    registry = load_json(command_registry_path(project_root), {"commands": []})
    if not registry.get("commands"):
        findings.append(_finding("medium", "NO_COMMANDS", "No project-native verification commands were discovered."))
    else:
        available = [c for c in registry["commands"] if c.get("available")]
        if not available:
            findings.append(_finding("medium", "NO_AVAILABLE_COMMANDS", "Commands were discovered but executables are unavailable."))
        unreviewed = [c["id"] for c in registry["commands"] if c.get("trust") == "project_defined" and not c.get("reviewed")]
        if unreviewed:
            findings.append(_finding("info", "UNREVIEWED_PROJECT_COMMANDS", f"{len(unreviewed)} project-defined commands need review before execution."))

    facts = load_json(eng / "reports" / "project-facts.json", {})
    if facts.get("signals", {}).get("sensitive_file_candidates_present"):
        findings.append(_finding(
            "medium", "SENSITIVE_FILE_CANDIDATES",
            "Potential secret or sensitive files were detected by name. Do not print their contents.",
            paths=facts.get("evidence", {}).get("sensitive_file_candidates", []),
        ))
    if not facts.get("signals", {}).get("tests_present"):
        findings.append(_finding("medium", "NO_TESTS_DETECTED", "No tests were detected."))
    if not facts.get("signals", {}).get("ci_present"):
        findings.append(_finding("low", "NO_CI_DETECTED", "No CI configuration was detected."))

    evidence_result = verify_evidence(project_root)
    if evidence_result.get("count", 0) and not evidence_result.get("valid"):
        findings.append(_finding("high", "EVIDENCE_INTEGRITY_FAILED", "Evidence ledger verification failed.", details=evidence_result["findings"]))

    integrity = verify_pack_integrity(pack_root)
    if not integrity.get("valid"):
        findings.append(_finding("high", "PACK_INTEGRITY_FAILED", "Skill pack integrity verification failed.", details=integrity["findings"][:20]))

    # Skill format checks.
    skill_dirs = [p for p in (pack_root / "agent-skills").iterdir() if p.is_dir()]
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        if not skill_file.exists():
            findings.append(_finding("high", "SKILL_MISSING_MANIFEST", f"{directory.name} has no SKILL.md"))
            continue
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
            findings.append(_finding("high", "SKILL_BAD_FRONTMATTER", f"{directory.name}/SKILL.md lacks required front matter."))

    result = {
        "schema_version": 2,
        "generated_at": utc_now(),
        "healthy": not any(SEVERITY_RANK[f["severity"]] >= SEVERITY_RANK["high"] for f in findings),
        "finding_count": len(findings),
        "findings": sorted(findings, key=lambda f: (-SEVERITY_RANK[f["severity"]], f["code"])),
    }
    return result
