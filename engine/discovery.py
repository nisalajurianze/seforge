from __future__ import annotations

import json
import os
import re
import tomllib
from pathlib import Path
from typing import Any

from .common import safe_relative, utc_now

IGNORE_DIRS = {
    ".git", ".engineering", ".idea", ".vscode", "__pycache__", "node_modules",
    "vendor", "dist", "build", "target", ".venv", "venv", ".tox", ".mypy_cache",
    ".pytest_cache", "coverage", ".next", ".turbo",
    ".agents", ".claude", ".cursor", ".gemini", ".windsurf",
}
PROVIDER_GENERATED_PREFIXES = {
    ".github/skills",
    ".github/agents",
    ".github/instructions",
}
PROVIDER_INSTRUCTION_FILES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".windsurfrules",
    ".github/copilot-instructions.md",
}

STACK_MARKERS = {
    "node": ["package.json"],
    "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "poetry.lock"],
    "java_maven": ["pom.xml"],
    "java_gradle": ["build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"],
    "dotnet": ["*.sln", "*.csproj", "*.fsproj"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "php": ["composer.json"],
    "ruby": ["Gemfile"],
    "android": ["AndroidManifest.xml"],
    "ios": ["*.xcodeproj", "*.xcworkspace", "Podfile"],
    "docker": ["Dockerfile", "compose.yaml", "compose.yml", "docker-compose.yml", "docker-compose.yaml"],
    "kubernetes": ["Chart.yaml", "kustomization.yaml"],
    "terraform": ["*.tf"],
    "make": ["Makefile"],
}

SENSITIVE_FILE_PATTERNS = [
    re.compile(r"(^|/)\.env($|\.)", re.I),
    re.compile(r"(secret|credential|private[-_]?key|id_rsa|\.pem$|\.p12$|\.pfx$)", re.I),
]

DOMAIN_SIGNALS = {
    "payments": ["payment", "billing", "invoice", "wallet", "ledger", "stripe", "paypal"],
    "healthcare": ["patient", "medical", "healthcare", "hospital", "clinical", "ehr"],
    "identity": ["oauth", "openid", "sso", "authentication", "authorization", "login"],
    "geospatial": ["map", "gis", "geospatial", "latitude", "longitude", "geofence"],
    "ai_enabled": ["openai", "anthropic", "gemini", "llm", "embedding", "langchain", "agent"],
    "messaging": ["kafka", "rabbitmq", "nats", "pubsub", "eventbus"],
    "search": ["elasticsearch", "opensearch", "solr", "meilisearch", "algolia"],
    "embedded_iot": ["firmware", "sensor", "mqtt", "embedded", "microcontroller", "arduino"],
}

def _walk(root: Path, max_files: int = 50000):
    count = 0
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        try:
            rel_current = current_path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            rel_current = ""
        if any(rel_current == prefix or rel_current.startswith(prefix + "/") for prefix in PROVIDER_GENERATED_PREFIXES):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in files:
            candidate = current_path / name
            try:
                resolved_candidate = candidate.resolve()
                rel_candidate = resolved_candidate.relative_to(root.resolve()).as_posix()
            except (OSError, ValueError):
                continue
            if rel_candidate in PROVIDER_INSTRUCTION_FILES:
                continue
            count += 1
            if count > max_files:
                return
            yield candidate

def _matches_marker(path: Path, root: Path, markers: list[str]) -> bool:
    rel = safe_relative(path, root)
    name = path.name
    for marker in markers:
        if marker.startswith("*."):
            if name.endswith(marker[1:]):
                return True
        elif name == marker or rel.endswith("/" + marker):
            return True
    return False

def _read_text(path: Path, limit: int = 200_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _read_toml(path: Path) -> dict[str, Any]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def discover(project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    files = list(_walk(project_root))
    rel_files = [safe_relative(p, project_root) for p in files]

    stack_evidence: dict[str, list[str]] = {}
    for stack, markers in STACK_MARKERS.items():
        matches = [safe_relative(p, project_root) for p in files if _matches_marker(p, project_root, markers)]
        if matches:
            stack_evidence[stack] = matches[:20]

    package = _read_json(project_root / "package.json")
    pyproject = _read_toml(project_root / "pyproject.toml")
    composer = _read_json(project_root / "composer.json")
    cargo = _read_toml(project_root / "Cargo.toml")

    readme_candidates = [p for p in files if p.name.lower() in {"readme.md", "readme.rst", "readme.txt"}]
    readme_text = _read_text(readme_candidates[0], 50_000) if readme_candidates else ""

    source_extensions = {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".kts", ".cs",
        ".fs", ".go", ".rs", ".php", ".rb", ".swift", ".c", ".cpp", ".h", ".hpp",
    }
    source_files = [p for p in files if p.suffix.lower() in source_extensions]
    test_files = [
        p for p in files
        if any(part.lower() in {"test", "tests", "__tests__", "spec", "specs"} for part in p.parts)
        or re.search(r"(test|spec)\.", p.name, re.I)
    ]

    ci_files = [
        p for p in files
        if ".github/workflows" in safe_relative(p, project_root)
        or p.name in {".gitlab-ci.yml", "azure-pipelines.yml", "Jenkinsfile", "bitbucket-pipelines.yml"}
    ]
    migration_files = [
        p for p in files
        if any(part.lower() in {"migration", "migrations", "alembic", "flyway", "liquibase"} for part in p.parts)
        or "prisma/migrations" in safe_relative(p, project_root)
    ]
    api_files = [
        p for p in files
        if p.name.lower() in {"openapi.yaml", "openapi.yml", "openapi.json", "swagger.yaml", "swagger.yml", "asyncapi.yaml", "asyncapi.yml"}
    ]
    infra_files = [
        p for p in files
        if p.name in {"Dockerfile", "compose.yaml", "compose.yml", "docker-compose.yml", "Chart.yaml", "kustomization.yaml"}
        or p.suffix == ".tf"
    ]

    sensitive_candidates = [
        safe_relative(p, project_root)
        for p in files
        if any(pattern.search(safe_relative(p, project_root)) for pattern in SENSITIVE_FILE_PATTERNS)
    ]

    searchable = " ".join([
        project_root.name,
        package.get("name", ""),
        package.get("description", ""),
        str(pyproject.get("project", {}).get("name", "")),
        str(pyproject.get("project", {}).get("description", "")),
        str(composer.get("name", "")),
        str(cargo.get("package", {}).get("name", "")),
        readme_text[:20_000],
        " ".join(rel_files[:3000]),
    ]).lower()

    domains: dict[str, list[str]] = {}
    for domain, signals in DOMAIN_SIGNALS.items():
        matches = [signal for signal in signals if signal in searchable]
        if matches:
            domains[domain] = matches

    project_name = (
        package.get("name")
        or pyproject.get("project", {}).get("name")
        or composer.get("name")
        or cargo.get("package", {}).get("name")
        or project_root.name
    )
    description = (
        package.get("description")
        or pyproject.get("project", {}).get("description")
        or _first_description(readme_text)
        or ""
    )

    platforms = []
    if "android" in stack_evidence or "ios" in stack_evidence:
        platforms.append("mobile")
    if "node" in stack_evidence or any("/public/" in f"/{x}/" or "/src/pages/" in f"/{x}/" for x in rel_files):
        platforms.append("web")
    if any(x in stack_evidence for x in {"python", "java_maven", "java_gradle", "dotnet", "go", "rust", "php", "ruby"}):
        platforms.append("backend_or_library")
    if infra_files:
        platforms.append("cloud_or_container")
    if "embedded_iot" in domains:
        platforms.append("embedded_or_iot")
    if not platforms:
        platforms.append("unknown")

    facts = {
        "schema_version": 2,
        "generated_at": utc_now(),
        "project_root": str(project_root),
        "project_name": project_name,
        "description": description,
        "stacks": sorted(stack_evidence),
        "stack_evidence": stack_evidence,
        "platforms": list(dict.fromkeys(platforms)),
        "domains": domains,
        "counts": {
            "files_scanned": len(files),
            "source_files": len(source_files),
            "test_files": len(test_files),
            "ci_files": len(ci_files),
            "migration_files": len(migration_files),
            "api_spec_files": len(api_files),
            "infrastructure_files": len(infra_files),
        },
        "signals": {
            "existing_code": bool(source_files),
            "tests_present": bool(test_files),
            "ci_present": bool(ci_files),
            "migrations_present": bool(migration_files),
            "api_spec_present": bool(api_files),
            "infrastructure_present": bool(infra_files),
            "readme_present": bool(readme_candidates),
            "sensitive_file_candidates_present": bool(sensitive_candidates),
        },
        "evidence": {
            "readme": safe_relative(readme_candidates[0], project_root) if readme_candidates else None,
            "ci_files": [safe_relative(p, project_root) for p in ci_files[:20]],
            "migration_files": [safe_relative(p, project_root) for p in migration_files[:20]],
            "api_spec_files": [safe_relative(p, project_root) for p in api_files[:20]],
            "infrastructure_files": [safe_relative(p, project_root) for p in infra_files[:20]],
            "sensitive_file_candidates": sensitive_candidates[:20],
        },
        "metadata": {
            "package_json": {
                "name": package.get("name"),
                "version": package.get("version"),
                "scripts": sorted((package.get("scripts") or {}).keys()),
                "dependencies": len(package.get("dependencies") or {}),
                "dev_dependencies": len(package.get("devDependencies") or {}),
            } if package else None,
            "pyproject": {
                "name": pyproject.get("project", {}).get("name"),
                "requires_python": pyproject.get("project", {}).get("requires-python"),
            } if pyproject else None,
        },
        "confidence": {
            "project_name": "high",
            "description": "medium" if description else "low",
            "platforms": "high" if platforms != ["unknown"] else "low",
            "domains": "medium",
            "data_sensitivity": "unresolved",
        },
    }
    return facts

def _first_description(readme: str) -> str:
    chunks = []
    for line in readme.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("![") or stripped.startswith("[!["):
            continue
        chunks.append(stripped)
        if len(" ".join(chunks)) >= 300:
            break
    return " ".join(chunks)[:500]
