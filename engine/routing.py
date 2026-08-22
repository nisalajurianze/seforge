from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import atomic_write_json, load_json, utc_now
from .state import ensure_layout, skill_manifest_path

CORE_SKILLS = [1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 17, 18, 21, 22, 24, 46, 47, 48]

TASK_SIGNAL_MAP = {
    3: ["architecture", "design", "service boundary", "module", "component"],
    4: ["configuration", "version", "branch", "merge", "feature flag"],
    5: ["production", "operation", "on-call", "slo", "incident", "runbook"],
    6: ["log", "metric", "trace", "observability", "telemetry", "alert"],
    7: ["reliability", "resilience", "retry", "timeout", "fallback", "recovery"],
    8: ["security", "vulnerability", "threat", "auth", "permission", "secret"],
    9: ["dependency", "supply chain", "sbom", "package", "provenance"],
    10: ["product", "user need", "mvp", "feature", "outcome"],
    11: ["ui", "ux", "accessibility", "screen", "form", "frontend"],
    12: ["privacy", "personal data", "retention", "consent", "deletion"],
    13: ["api", "integration", "webhook", "contract", "endpoint"],
    14: ["data pipeline", "etl", "warehouse", "analytics", "dataset"],
    15: ["cloud", "container", "kubernetes", "serverless", "microservice"],
    17: ["release", "deploy", "rollout", "canary", "rollback"],
    18: ["metric", "measurement", "improvement", "lead time"],
    19: ["cost", "finops", "budget", "tco"],
    20: ["carbon", "energy", "sustainability"],
    23: ["legacy", "modernize", "rewrite", "retire"],
    25: ["system of systems", "hardware", "human", "subsystem"],
    26: ["formal", "proof", "model checking", "invariant"],
    27: ["safety", "hazard", "harm", "fail-safe"],
    28: ["assurance", "independent verification", "certification"],
    29: ["human factors", "operator", "alarm", "handover"],
    30: ["localization", "internationalization", "translation", "rtl"],
    31: ["interoperability", "standards conformance", "protocol conformance", "standard compliance"],
    32: ["product line", "variant", "white label", "feature model"],
    33: ["domain model", "bounded context", "aggregate", "business rule"],
    34: ["embedded", "firmware", "sensor", "actuator", "real-time"],
    35: ["state machine", "workflow", "transition", "protocol"],
    36: ["concurrency", "thread", "async", "race", "deadlock"],
    37: ["transaction", "integrity", "consistency", "ledger", "idempotent"],
    38: ["event", "queue", "stream", "message", "kafka"],
    39: ["migration", "data move", "conversion", "reconciliation"],
    40: ["performance", "capacity", "scalability", "compatibility", "latency"],
    41: ["supplier", "vendor", "procurement", "saas"],
    42: ["open source", "license", "maintainer", "fork"],
    43: ["compliance", "audit", "control", "regulation"],
    44: ["experiment", "a/b", "analytics", "feature flag"],
    45: ["ai-assisted", "copilot", "codex", "claude", "generated code"],
    49: ["identity", "login", "authentication", "authorization", "sso"],
    50: ["cryptography", "encryption", "key", "certificate", "pqc"],
    51: ["tenant", "multi-tenant", "saas isolation"],
    52: ["offline", "sync", "replication", "conflict"],
    53: ["timezone", "calendar", "date", "time", "recurrence"],
    54: ["numeric", "floating point", "rounding", "scientific"],
    55: ["update", "patch", "firmware", "signing"],
    56: ["record", "archive", "legal hold", "retention"],
    57: ["forensic", "evidence", "investigation", "incident"],
    58: ["service management", "support", "ticket", "problem management"],
    59: ["asset", "inventory", "end of life", "renewal"],
    60: ["sanitization", "erase", "disposal", "delete data"],
    61: ["browser", "web", "html", "pwa"],
    62: ["mobile", "android", "ios", "app store"],
    63: ["network", "tcp", "tls", "dns", "http"],
    64: ["provenance", "lineage", "origin"],
    65: ["differential privacy", "confidential computing", "homomorphic"],
    66: ["fraud", "abuse", "bot", "trust and safety"],
    67: ["content authenticity", "c2pa", "media provenance"],
    68: ["blockchain", "smart contract", "distributed ledger"],
    69: ["quantum"],
    70: ["digital twin", "simulation"],
    71: ["autonomous", "robot", "drone"],
    72: ["geospatial", "map", "location", "gis"],
    73: ["edge", "mec", "fleet"],
    74: ["hpc", "gpu", "mpi", "openmp"],
    75: ["video", "audio", "streaming", "qoe"],
    76: ["scada", "plc", "industrial control", "ot"],
    77: ["ar", "vr", "xr", "immersive"],
    78: ["payment", "billing", "wallet", "money"],
    79: ["search", "retrieval", "ranking", "index"],
    80: ["knowledge graph", "ontology", "rdf", "sparql"],
}

FILE_SIGNAL_MAP = {
    11: [r"\.(tsx|jsx|vue|svelte|css|scss|html)$", r"(^|/)frontend/", r"(^|/)ui/"],
    13: [r"openapi", r"swagger", r"(^|/)api/", r"routes?"],
    34: [r"firmware", r"\.(c|cpp|h|hpp)$"],
    38: [r"kafka|queue|event|consumer|producer"],
    39: [r"migration|alembic|flyway|liquibase|prisma/migrations"],
    49: [r"auth|login|oauth|oidc|session"],
    50: [r"crypto|certificate|keystore|truststore"],
    61: [r"\.(tsx|jsx|vue|svelte|html|css|scss)$"],
    62: [r"AndroidManifest|\.swift$|\.xcodeproj|(^|/)ios/|(^|/)android/"],
    78: [r"payment|billing|invoice|ledger|wallet"],
    79: [r"search|index|ranking"],
}

def load_pack_manifest(pack_root: Path) -> dict[str, Any]:
    return load_json(pack_root / "manifest.json", {"skills": []})

def load_profiles(pack_root: Path) -> list[dict[str, Any]]:
    result = []
    for path in sorted((pack_root / "profiles").glob("*.json")):
        result.append(load_json(path, {}))
    return result

def route_skills(project_root: Path, pack_root: Path, facts: dict[str, Any],
                 context: dict[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    pack_manifest = load_pack_manifest(pack_root)
    skill_meta = {int(s["id"]): s for s in (pack_manifest.get("engineering_skills") or pack_manifest.get("skills", []))}
    activations: dict[int, dict[str, Any]] = {}

    def add(skill_id: int, status: str, confidence: str, rationale: str, source: str) -> None:
        if skill_id not in skill_meta:
            return
        existing = activations.get(skill_id)
        priority = {"active": 3, "recommended": 2, "candidate": 1}
        if existing and priority[existing["status"]] > priority[status]:
            existing["evidence"].append({"source": source, "rationale": rationale})
            return
        entry = existing or {
            "id": skill_id,
            "name": skill_meta[skill_id]["name"],
            "tier": skill_meta[skill_id]["tier"],
            "skill_path": f"agent-skills/se-{skill_id:02d}-{skill_meta[skill_id]['slug']}/SKILL.md",
            "status": status,
            "confidence": confidence,
            "owner": context.get("engineering_owner", "project-team"),
            "owner_status": "confirmed" if context.get("engineering_owner") else "provisional",
            "evidence": [],
            "required_artifacts": skill_meta[skill_id].get("required_artifacts", []),
            "quality_gates": skill_meta[skill_id].get("quality_gates", []),
        }
        entry["status"] = status
        entry["confidence"] = confidence
        entry["evidence"].append({"source": source, "rationale": rationale})
        activations[skill_id] = entry

    for sid in CORE_SKILLS:
        add(sid, "active", "high", "Universal engineering baseline.", "core-policy")

    profiles = load_profiles(pack_root)
    matched_profiles = []
    for profile in profiles:
        matched, evidence = _profile_matches(profile, facts, context)
        if not matched:
            continue
        matched_profiles.append({"name": profile["name"], "evidence": evidence})
        for sid in profile.get("required_skills", []):
            add(int(sid), "active", "high", f"Required by profile {profile['name']}.", f"profile:{profile['name']}")
        for sid in profile.get("recommended_skills", []):
            add(int(sid), "recommended", "medium", f"Recommended by profile {profile['name']}.", f"profile:{profile['name']}")

    if facts.get("signals", {}).get("migrations_present"):
        add(39, "active", "high", "Migration files were detected.", "repository")
        add(37, "active", "medium", "Migrations can affect data integrity.", "repository")
    if facts.get("signals", {}).get("sensitive_file_candidates_present"):
        add(8, "active", "high", "Potential secret or sensitive files were detected.", "repository")
        add(12, "recommended", "medium", "Data sensitivity requires confirmation.", "repository")
    if facts.get("domains", {}).get("identity"):
        add(49, "active", "high", "Identity/authentication signals were detected.", "repository")
    if facts.get("domains", {}).get("messaging"):
        add(38, "active", "high", "Messaging/streaming signals were detected.", "repository")
    if facts.get("domains", {}).get("search"):
        add(79, "active", "high", "Search technology signals were detected.", "repository")

    declared_impact = context.get("impact_level") or context.get("declared_impact")
    if declared_impact in {"L4", "critical"}:
        for sid in [25, 26, 27, 28, 43, 57]:
            add(sid, "active", "high", "Critical impact declared.", "user-context")

    manifest = {
        "schema_version": 2,
        "generated_at": utc_now(),
        "project": facts.get("project_name", project_root.name),
        "matched_profiles": matched_profiles,
        "skills": [activations[sid] for sid in sorted(activations)],
        "routing_notes": [
            "Active skills are project-level candidates; task-context selects a smaller task-specific subset.",
            "Recommended skills are not loaded unless the task reaches their decision area.",
            "Repository inference does not replace user confirmation for high-impact facts.",
        ],
    }
    ensure_layout(project_root)
    atomic_write_json(skill_manifest_path(project_root), manifest)
    return manifest

def select_task_skills(task: dict[str, Any], project_manifest: dict[str, Any],
                       max_skills: int = 8) -> list[int]:
    active = {
        int(s["id"]): s
        for s in project_manifest.get("skills", [])
        if s.get("status") in {"active", "recommended"}
    }
    text = " ".join([
        str(task.get("name", "")),
        str(task.get("description", "")),
        " ".join(task.get("acceptance_criteria", [])),
        " ".join(task.get("files", [])),
        " ".join(task.get("tags", [])),
    ]).lower()
    scores: dict[int, int] = {}

    # Universal task owners.
    for sid in [2, 8, 17, 22]:
        if sid in active:
            scores[sid] = scores.get(sid, 0) + 1

    for sid, signals in TASK_SIGNAL_MAP.items():
        if sid not in active:
            continue
        hits = sum(1 for signal in signals if signal in text)
        if hits:
            scores[sid] = scores.get(sid, 0) + hits * 3

    for sid, patterns in FILE_SIGNAL_MAP.items():
        if sid not in active:
            continue
        hits = sum(1 for pattern in patterns if re.search(pattern, text, re.I))
        if hits:
            scores[sid] = scores.get(sid, 0) + hits * 4

    explicit = [int(x) for x in task.get("skill_ids", []) if int(x) in active]
    for sid in explicit:
        scores[sid] = scores.get(sid, 0) + 100

    ranked = sorted(scores, key=lambda sid: (-scores[sid], sid))
    if not ranked:
        ranked = [sid for sid in [2, 8, 17, 22] if sid in active]
    return ranked[:max_skills]

def _profile_matches(profile: dict[str, Any], facts: dict[str, Any],
                     context: dict[str, Any]) -> tuple[bool, list[str]]:
    signals = profile.get("signals", {})
    evidence = []
    matched = False

    platforms = set(facts.get("platforms", []))
    for platform in signals.get("platforms", []):
        if platform in platforms:
            matched = True
            evidence.append(f"platform:{platform}")

    domains = set(facts.get("domains", {}).keys())
    for domain in signals.get("domains", []):
        if domain in domains:
            matched = True
            evidence.append(f"domain:{domain}")

    searchable = " ".join([
        facts.get("project_name", ""),
        facts.get("description", ""),
        json.dumps(context),
    ]).lower()
    for keyword in signals.get("keywords", []):
        if keyword.lower() in searchable:
            matched = True
            evidence.append(f"keyword:{keyword}")

    if signals.get("api_spec") and facts.get("signals", {}).get("api_spec_present"):
        matched = True
        evidence.append("api-spec")

    for impact in signals.get("impact", []):
        current = context.get("impact_level") or context.get("declared_impact")
        if current == impact:
            matched = True
            evidence.append(f"impact:{impact}")

    return matched, evidence
