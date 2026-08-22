from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import time
import tomllib
from pathlib import Path
from typing import Any

from .common import atomic_write_json, canonical_json_bytes, safe_relative, sha256_bytes, sha256_file, utc_now
from .policy import assess_command
from .state import command_registry_path, ensure_layout
from .evidence import record_command_evidence

CATEGORY_ORDER = ["format", "lint", "typecheck", "unit", "integration", "e2e", "security", "build", "smoke", "other"]

def _entry(command_id: str, category: str, argv: list[str], source: str, *,
           cwd: str = ".", trust: str = "project_defined", network: bool = False,
           description: str = "") -> dict[str, Any]:
    rendered = " ".join(shlex.quote(x) for x in argv)
    assessment = assess_command(rendered)
    if network:
        assessment.network = True
    risk = assessment.risk
    reasons = list(assessment.reasons)
    if trust == "project_defined" and risk == "R1":
        risk = "R2"
        reasons.append("executes project-controlled code without an OS sandbox")
    return {
        "id": command_id,
        "category": category,
        "argv": argv,
        "rendered": rendered,
        "cwd": cwd,
        "source": source,
        "trust": trust,
        "network": bool(network or assessment.network),
        "risk": risk,
        "risk_reasons": list(dict.fromkeys(reasons)),
        "execution_isolation": "process_only_no_os_sandbox",
        "description": description,
        "reviewed": False,
        "enabled": True,
    }

def discover_commands(project_root: Path, facts: dict[str, Any] | None = None) -> dict[str, Any]:
    project_root = project_root.resolve()
    entries: list[dict[str, Any]] = []

    package_path = project_root / "package.json"
    if package_path.exists():
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
        except Exception:
            package = {}
        scripts = package.get("scripts") or {}
        manager = _node_manager(project_root)
        for script_name, script_body in scripts.items():
            category = _script_category(script_name)
            entries.append(_entry(
                f"node:{script_name}",
                category,
                [manager, "run", script_name],
                "package.json",
                trust="project_defined",
                network=_likely_network(script_body),
                description=f"package.json script: {script_body}",
            ))

    pyproject_path = project_root / "pyproject.toml"
    pyproject = {}
    if pyproject_path.exists():
        try:
            pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        except Exception:
            pyproject = {}
    python_markers = [
        project_root / "requirements.txt", project_root / "requirements-dev.txt",
        project_root / "setup.cfg", project_root / "tox.ini", project_root / "pytest.ini",
    ]
    python_project = pyproject_path.exists() or any(path.exists() for path in python_markers) or any(project_root.glob("*.py")) or (project_root / "src").exists()
    if python_project:
        syntax_script = Path(__file__).resolve().parents[1] / "scripts" / "v2" / "python_syntax_check.py"
        entries.append(_entry(
            "python:compile", "build",
            [os.sys.executable, str(syntax_script), "--project-root", "."],
            "skill-pack:python_syntax_check", trust="pack_defined",
            description="Syntax-check project Python source without importing it, creating bytecode, or traversing installed tooling."
        ))
        dependency_text = json.dumps(pyproject).lower()
        for marker in python_markers:
            if marker.exists() and marker.is_file():
                dependency_text += "\n" + marker.read_text(encoding="utf-8", errors="ignore").lower()
        if "pytest" in dependency_text:
            entries.append(_entry("python:pytest", "unit", [os.sys.executable, "-m", "pytest"],
                                  "project-convention", trust="project_defined",
                                  description="Run the project pytest suite."))
        elif (project_root / "tests").exists():
            entries.append(_entry(
                "python:unittest", "unit",
                [os.sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                "project-convention", trust="project_defined",
                description="Run the standard-library unittest discovery suite because pytest was not declared."
            ))
        if "ruff" in json.dumps(pyproject).lower():
            entries.append(_entry("python:ruff", "lint", [os.sys.executable, "-m", "ruff", "check", "."],
                                  "pyproject.toml", trust="project_defined"))
        if "mypy" in json.dumps(pyproject).lower():
            entries.append(_entry("python:mypy", "typecheck", [os.sys.executable, "-m", "mypy", "."],
                                  "pyproject.toml", trust="project_defined"))

    if (project_root / "pom.xml").exists():
        entries += [
            _entry("maven:test", "unit", ["mvn", "-B", "test"], "pom.xml", trust="project_defined"),
            _entry("maven:verify", "build", ["mvn", "-B", "verify"], "pom.xml", trust="project_defined"),
        ]

    gradle_wrapper = "gradlew.bat" if os.name == "nt" else "./gradlew"
    if (project_root / "gradlew").exists() or (project_root / "gradlew.bat").exists():
        entries += [
            _entry("gradle:test", "unit", [gradle_wrapper, "test"], "gradle-wrapper", trust="project_defined"),
            _entry("gradle:build", "build", [gradle_wrapper, "build"], "gradle-wrapper", trust="project_defined"),
        ]
    elif (project_root / "build.gradle").exists() or (project_root / "build.gradle.kts").exists():
        entries += [
            _entry("gradle:test", "unit", ["gradle", "test"], "gradle-build", trust="project_defined"),
            _entry("gradle:build", "build", ["gradle", "build"], "gradle-build", trust="project_defined"),
        ]

    if any(project_root.glob("*.sln")) or any(project_root.rglob("*.csproj")):
        entries += [
            _entry("dotnet:build", "build", ["dotnet", "build", "--no-restore"], "dotnet-project", trust="project_defined"),
            _entry("dotnet:test", "unit", ["dotnet", "test", "--no-build"], "dotnet-project", trust="project_defined"),
        ]

    if (project_root / "go.mod").exists():
        entries += [
            _entry("go:vet", "lint", ["go", "vet", "./..."], "go.mod", trust="project_defined"),
            _entry("go:test", "unit", ["go", "test", "./..."], "go.mod", trust="project_defined"),
            _entry("go:build", "build", ["go", "build", "./..."], "go.mod", trust="project_defined"),
        ]

    if (project_root / "Cargo.toml").exists():
        entries += [
            _entry("rust:fmt", "format", ["cargo", "fmt", "--", "--check"], "Cargo.toml", trust="project_defined"),
            _entry("rust:clippy", "lint", ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"], "Cargo.toml", trust="project_defined"),
            _entry("rust:test", "unit", ["cargo", "test"], "Cargo.toml", trust="project_defined"),
            _entry("rust:build", "build", ["cargo", "build"], "Cargo.toml", trust="project_defined"),
        ]

    composer_path = project_root / "composer.json"
    if composer_path.exists():
        try:
            composer = json.loads(composer_path.read_text(encoding="utf-8"))
        except Exception:
            composer = {}
        for name, value in (composer.get("scripts") or {}).items():
            entries.append(_entry(f"composer:{name}", _script_category(name), ["composer", "run-script", name],
                                  "composer.json", trust="project_defined",
                                  network=_likely_network(str(value)), description=str(value)))

    if (project_root / "Gemfile").exists():
        if (project_root / "spec").exists():
            entries.append(_entry("ruby:rspec", "unit", ["bundle", "exec", "rspec"], "Gemfile", trust="project_defined"))
        if (project_root / "Rakefile").exists():
            entries.append(_entry("ruby:rake-test", "unit", ["bundle", "exec", "rake", "test"], "Rakefile", trust="project_defined"))

    makefile = project_root / "Makefile"
    if makefile.exists():
        for target in _make_targets(makefile):
            entries.append(_entry(f"make:{target}", _script_category(target), ["make", target],
                                  "Makefile", trust="project_defined"))

    # Deduplicate IDs while preserving first discovery.
    seen = set()
    unique = []
    for item in entries:
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        item["available"] = shutil.which(item["argv"][0]) is not None or item["argv"][0].startswith("./")
        source_candidate = project_root / str(item.get("source", ""))
        if source_candidate.is_file():
            item["source_path"] = safe_relative(source_candidate, project_root)
            item["source_sha256"] = sha256_file(source_candidate)
        else:
            item["source_path"] = None
            item["source_sha256"] = None
        definition_payload = {
            "id": item["id"],
            "argv": item["argv"],
            "cwd": item["cwd"],
            "source": item["source"],
            "description": item.get("description", ""),
        }
        item["definition_hash"] = sha256_bytes(canonical_json_bytes(definition_payload))
        item["reviewed_definition_hash"] = None
        item["reviewed_source_sha256"] = None
        unique.append(item)

    registry = {
        "schema_version": 2,
        "generated_at": utc_now(),
        "project_root": str(project_root),
        "commands": sorted(unique, key=lambda x: (CATEGORY_ORDER.index(x["category"]) if x["category"] in CATEGORY_ORDER else 999, x["id"])),
        "policy": {
            "project_defined_commands_are_untrusted_until_reviewed": True,
            "network_requires_explicit_flag": True,
            "R3_or_R4_requires_explicit_approval": True,
        },
    }
    ensure_layout(project_root)
    atomic_write_json(command_registry_path(project_root), registry)
    return registry

def execute_command(project_root: Path, command: dict[str, Any], *,
                    trust_project_scripts: bool = False,
                    allow_network: bool = False,
                    explicit_approval: bool = False,
                    timeout_seconds: int = 900,
                    task_id: str | None = None,
                    skill_ids: list[int] | None = None) -> dict[str, Any]:
    if not command.get("enabled", True):
        raise PermissionError(f"Command is disabled: {command['id']}")
    if not command.get("available", True):
        raise FileNotFoundError(f"Executable not available for command: {command['id']}")
    if command.get("trust") == "project_defined":
        if not command.get("reviewed"):
            raise PermissionError(
                f"{command['id']} executes project-defined code. Review the command definition first."
            )
        if not trust_project_scripts:
            raise PermissionError(
                f"{command['id']} requires --trust-project-scripts for this unsandboxed invocation."
            )
        if command.get("reviewed_definition_hash") != command.get("definition_hash"):
            raise PermissionError(f"{command['id']} definition changed after review. Re-discover and review it.")
        source_path = command.get("source_path")
        reviewed_source = command.get("reviewed_source_sha256")
        if source_path and reviewed_source:
            current_source = (project_root / source_path).resolve()
            try:
                current_source.relative_to(project_root.resolve())
            except ValueError as exc:
                raise PermissionError("Command source path escapes project root.") from exc
            if not current_source.exists() or sha256_file(current_source) != reviewed_source:
                raise PermissionError(f"{command['id']} source file changed after review. Re-discover and review it.")
    if command.get("network") and not allow_network:
        raise PermissionError(f"{command['id']} may access the network. Pass --allow-network after review.")
    if command.get("risk") in {"R3", "R4"} and not explicit_approval:
        raise PermissionError(f"{command['id']} is {command['risk']} and requires explicit approval.")
    if command.get("risk") == "R4":
        raise PermissionError(f"{command['id']} is prohibited by default.")

    cwd = (project_root / command.get("cwd", ".")).resolve()
    try:
        cwd.relative_to(project_root.resolve())
    except ValueError as exc:
        raise PermissionError("Command cwd escapes the project root.") from exc

    started = time.time()
    process = subprocess.run(
        command["argv"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        env=_sanitized_env(),
    )
    ended = time.time()
    result = {
        "command_id": command["id"],
        "argv": command["argv"],
        "rendered": command["rendered"],
        "cwd": safe_relative(cwd, project_root),
        "source": command.get("source"),
        "trust": command.get("trust"),
        "risk": command.get("risk"),
        "execution_isolation": command.get("execution_isolation", "process_only_no_os_sandbox"),
        "network_policy_note": "allow-network is a policy acknowledgement, not OS-level egress isolation",
        "started_at_epoch": started,
        "ended_at_epoch": ended,
        "duration_seconds": round(ended - started, 3),
        "exit_code": process.returncode,
        "stdout": _truncate(_redact(process.stdout)),
        "stderr": _truncate(_redact(process.stderr)),
        "result": "pass" if process.returncode == 0 else "fail",
    }
    evidence = record_command_evidence(project_root, result, task_id=task_id, skill_ids=skill_ids)
    result["evidence"] = evidence
    return result

def _sanitized_env() -> dict[str, str]:
    env = {}
    for key, value in os.environ.items():
        if key in {"PATH", "HOME", "USER", "USERNAME", "SHELL", "COMSPEC", "SYSTEMROOT", "TEMP", "TMP", "LANG"} or key.startswith("LC_") or key == "CI":
            env[key] = value
    env["SEPACK_EXECUTION"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


REDACTION_PATTERNS = [
    (re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|pwd)\b\s*[:=]\s*[^\s,;]+"), r"\1=[REDACTED]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "[REDACTED PRIVATE KEY]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED AWS ACCESS KEY]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED GITHUB TOKEN]"),
]

def _redact(value: str) -> str:
    result = value
    for pattern, replacement in REDACTION_PATTERNS:
        result = pattern.sub(replacement, result)
    return result

def _truncate(value: str, limit: int = 200_000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value)-limit} characters]"

def _node_manager(project_root: Path) -> str:
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project_root / "yarn.lock").exists():
        return "yarn"
    return "npm"

def _script_category(name: str) -> str:
    value = name.lower()
    if "format" in value or value in {"fmt"}:
        return "format"
    if "lint" in value:
        return "lint"
    if "type" in value or "tsc" in value:
        return "typecheck"
    if "e2e" in value or "playwright" in value or "cypress" in value:
        return "e2e"
    if "integration" in value:
        return "integration"
    if "security" in value or "audit" in value:
        return "security"
    if "test" in value or "spec" in value:
        return "unit"
    if "build" in value or "compile" in value:
        return "build"
    if "smoke" in value:
        return "smoke"
    return "other"

def _likely_network(script: str) -> bool:
    return bool(re.search(r"\b(curl|wget|npm\s+(install|publish)|pnpm\s+publish|yarn\s+publish|pip\s+install|docker\s+push|git\s+push|deploy)\b", script, re.I))

def _make_targets(path: Path) -> list[str]:
    targets = []
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = re.match(r"^([A-Za-z0-9_.-]+)\s*:(?![=])", line)
            if match and not match.group(1).startswith("."):
                targets.append(match.group(1))
    except OSError:
        return []
    return targets[:100]
