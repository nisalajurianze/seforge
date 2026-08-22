#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
warnings: list[str] = []

def error(message: str) -> None:
    errors.append(message)

def warn(message: str) -> None:
    warnings.append(message)

def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        error(f"{path.relative_to(ROOT)}: missing YAML front matter")
        return {}
    try:
        block = text.split("---", 2)[1]
    except IndexError:
        error(f"{path.relative_to(ROOT)}: malformed front matter")
        return {}
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result

manifest_path = ROOT / "manifest.json"
if not manifest_path.exists():
    error("manifest.json missing")
    manifest = {}
else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

if manifest.get("version") != "2.0.1":
    error("manifest version must be 2.0.1")
if manifest.get("engineering_skill_count") != 80:
    error("engineering_skill_count must be 80")
if manifest.get("workflow_skill_count") != 12:
    error("workflow_skill_count must be 12")
if manifest.get("agent_skill_count") != 92:
    error("agent_skill_count must be 92")

pack_schema_path = ROOT / "schemas" / "v2" / "pack-manifest.schema.json"
if pack_schema_path.exists():
    try:
        pack_schema = json.loads(pack_schema_path.read_text(encoding="utf-8"))
        schema_version = pack_schema.get("properties", {}).get("version", {}).get("const")
        if schema_version != manifest.get("version"):
            error(f"pack-manifest schema version {schema_version!r} does not match manifest version {manifest.get('version')!r}")
    except Exception as exc:
        error(f"invalid pack manifest schema: {exc}")
if len(manifest.get("engineering_skills", [])) != 80:
    error("manifest engineering_skills must contain 80 entries")
if len(manifest.get("workflow_skills", [])) != 12:
    error("manifest workflow_skills must contain 12 entries")

for skill in manifest.get("engineering_skills", []):
    for key in ("agent_skill_path", "detailed_reference_path"):
        rel = skill.get(key)
        if not rel or not (ROOT / rel).exists():
            error(f"manifest path missing for SE-{int(skill.get('id', 0)):02d} {key}: {rel}")
for workflow in manifest.get("workflow_skills", []):
    rel = workflow.get("path")
    if not rel or not (ROOT / rel).exists():
        error(f"workflow manifest path missing: {rel}")

skill_root = ROOT / "agent-skills"
skill_dirs = sorted([p for p in skill_root.iterdir() if p.is_dir()]) if skill_root.exists() else []
engineering_dirs = [p for p in skill_dirs if p.name.startswith("se-")]
workflow_dirs = [p for p in skill_dirs if p.name.startswith("wf-")]
if len(engineering_dirs) != 80:
    error(f"expected 80 engineering skill directories, found {len(engineering_dirs)}")
if len(workflow_dirs) != 12:
    error(f"expected 12 workflow skill directories, found {len(workflow_dirs)}")
if len(skill_dirs) != 92:
    error(f"expected 92 total agent skills, found {len(skill_dirs)}")

names = set()
for directory in skill_dirs:
    skill_file = directory / "SKILL.md"
    if not skill_file.exists():
        error(f"{directory.relative_to(ROOT)}: SKILL.md missing")
        continue
    front = parse_frontmatter(skill_file)
    name = front.get("name", "")
    description = front.get("description", "")
    if not name:
        error(f"{skill_file.relative_to(ROOT)}: name missing")
    if name in names:
        error(f"duplicate Agent Skill name: {name}")
    names.add(name)
    if len(name) > 64:
        error(f"{skill_file.relative_to(ROOT)}: name exceeds 64 characters")
    if not description:
        error(f"{skill_file.relative_to(ROOT)}: description missing")
    if len(description) > 1024:
        error(f"{skill_file.relative_to(ROOT)}: description exceeds 1024 characters")
    if directory.name.startswith("se-"):
        if not (directory / "references" / "detailed-guide.md").exists():
            error(f"{directory.relative_to(ROOT)}: detailed guide missing")
        if not (directory / "assets" / "checklist.md").exists():
            error(f"{directory.relative_to(ROOT)}: checklist missing")

workflow_description_chars = 0
for directory in workflow_dirs:
    front = parse_frontmatter(directory / "SKILL.md")
    workflow_description_chars += len(front.get("description", ""))
if workflow_description_chars > 8000:
    error(f"workflow skill descriptions exceed the 8,000-character discovery budget: {workflow_description_chars}")

for pattern in ("provider-templates/github/agents/*.agent.md", "provider-templates/claude/agents/*.md"):
    for agent_path in ROOT.glob(pattern):
        front = parse_frontmatter(agent_path)
        for field in ("name", "description", "tools"):
            if not front.get(field):
                error(f"{agent_path.relative_to(ROOT)}: required frontmatter field missing: {field}")

required_files = [
    "AGENTS.md", "SKILL.md", "PLANS.md", "README.md", "INSTALL.md",
    "USER-GUIDE.md", "SOURCE-MAP.md", "RESEARCH-GAP-ANALYSIS.md",
    "engine/cli.py", "engine/policy.py", "engine/evidence.py",
    "scripts/install.py", "scripts/uninstall.py",
    "provider-templates/github/engineering-quality-gate.yml",
    "docs/agent/START-HERE.md", "docs/security/AGENT-SECURITY.md",
    "docs/security/MCP-POLICY.md", "evals/run_evals.py",
]
for rel in required_files:
    if not (ROOT / rel).exists():
        error(f"required file missing: {rel}")

# The canonical corpus must not be duplicated in the distribution.
for rel in ["skills", ".agents/skills", "reference/engineering-areas", "runtime"]:
    if (ROOT / rel).exists():
        error(f"obsolete or duplicate directory must not be distributed: {rel}")

agents_words = len((ROOT / "AGENTS.md").read_text(encoding="utf-8").split())
if agents_words > 500:
    error(f"AGENTS.md should remain concise; found {agents_words} words")

# Compile Python without executing project code.
python_files = [
    p for p in ROOT.rglob("*.py")
    if "__pycache__" not in p.parts and ".engineering" not in p.parts
]
for path in python_files:
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as exc:
        error(f"syntax error in {path.relative_to(ROOT)}: {exc}")

# Parse all JSON files except generated eval results.
for path in ROOT.rglob("*.json"):
    if path.name == "latest-results.json":
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

if not list((ROOT / "tests").glob("test_*.py")):
    error("no unit tests found")
if not list((ROOT / "evals" / "cases").glob("*.jsonl")):
    error("no eval cases found")

# Local Markdown link checks and command-name drift detection.
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "`task-context`" in text:
        error(f"{path.relative_to(ROOT)}: stale command name `task-context`; use `task context`")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#") or target.startswith("mailto:"):
            continue
        raw_target = target.split("#", 1)[0]
        candidate = (path.parent / raw_target).resolve()
        if raw_target and not candidate.exists():
            error(f"{path.relative_to(ROOT)}: broken local link {target}")

installer_text = (ROOT / "scripts" / "install.py").read_text(encoding="utf-8")
if 'default="workflow"' not in installer_text:
    error("installer must default to workflow-only provider skill installation")

for cache in ROOT.rglob("__pycache__"):
    warn(f"transient cache should be removed before packaging: {cache.relative_to(ROOT)}")

print(json.dumps({
    "valid": not errors,
    "errors": errors,
    "warnings": warnings,
    "counts": {
        "engineering_skills": len(engineering_dirs),
        "workflow_skills": len(workflow_dirs),
        "python_files": len(python_files),
        "unit_tests": len(list((ROOT / "tests").glob("test_*.py"))),
    }
}, indent=2))

raise SystemExit(0 if not errors else 1)
