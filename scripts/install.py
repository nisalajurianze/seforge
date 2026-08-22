#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

PACK_ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- SEPACK:BEGIN v2 -->"
END = "<!-- SEPACK:END -->"
PROVIDERS = {"agents", "openai", "github", "claude", "gemini", "cursor", "windsurf"}


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def provider_set(value: str) -> set[str]:
    requested = {item.strip().lower() for item in value.split(",") if item.strip()}
    if "all" in requested:
        return set(PROVIDERS)
    unknown = requested - PROVIDERS
    if unknown:
        raise SystemExit("Unknown providers: " + ", ".join(sorted(unknown)))
    return requested


def managed_content(pointer: str) -> str:
    return f"{BEGIN}\n{pointer.strip()}\n{END}\n"


def remove_managed_block_text(text: str) -> str:
    if BEGIN not in text or END not in text:
        return text
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    return (text[:start].rstrip() + "\n" + text[end:].lstrip("\n")).strip() + "\n"


def previous_record_map(previous_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in previous_manifest.get("records", []):
        result[record.get("path", "")] = record
    return result


def _copy_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)


def ensure_original(
    path: Path,
    target_root: Path,
    baseline_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    *,
    reconstruct_managed_block: bool = False,
    reconstruct_json_hook: dict[str, Any] | None = None,
) -> None:
    rel = path.relative_to(target_root).as_posix()
    if rel in originals:
        return

    previous = previous_record_map(previous_manifest).get(rel)
    state: dict[str, Any] = {
        "existed": path.exists(),
        "kind": "directory" if path.is_dir() else "file",
        "backup": None,
        "source": "current_pre_install",
    }

    if previous and previous.get("created") is True and not reconstruct_managed_block and reconstruct_json_hook is None:
        state.update({"existed": False, "kind": "file", "source": "legacy_manifest_created"})
        originals[rel] = state
        return

    baseline = baseline_root / rel
    if reconstruct_managed_block and path.exists() and path.is_file():
        baseline.parent.mkdir(parents=True, exist_ok=True)
        baseline.write_text(remove_managed_block_text(path.read_text(encoding="utf-8", errors="ignore")), encoding="utf-8")
        state.update({"existed": True, "kind": "file", "backup": baseline.relative_to(target_root).as_posix(), "source": "reconstructed_without_managed_block"})
    elif reconstruct_json_hook is not None and path.exists() and path.is_file():
        value = load_json(path, {})
        _remove_hook_groups(value, reconstruct_json_hook)
        write_json(baseline, value)
        state.update({"existed": True, "kind": "file", "backup": baseline.relative_to(target_root).as_posix(), "source": "reconstructed_without_skill_pack_hook"})
    elif previous and previous.get("backup"):
        prior_backup = target_root / previous["backup"]
        if prior_backup.exists():
            _copy_path(prior_backup, baseline)
            state.update({
                "existed": True,
                "kind": "directory" if prior_backup.is_dir() else "file",
                "backup": baseline.relative_to(target_root).as_posix(),
                "source": "legacy_previous_backup",
            })
        elif path.exists():
            _copy_path(path, baseline)
            state.update({"backup": baseline.relative_to(target_root).as_posix(), "source": "current_fallback_legacy_backup_missing"})
    elif path.exists():
        _copy_path(path, baseline)
        state["backup"] = baseline.relative_to(target_root).as_posix()

    originals[rel] = state


def backup_current(path: Path, backup_root: Path, target_root: Path) -> str | None:
    if not path.exists():
        return None
    destination = backup_root / path.relative_to(target_root)
    _copy_path(path, destination)
    return destination.relative_to(target_root).as_posix()


def merge_managed_block(
    path: Path,
    pointer: str,
    backup_root: Path,
    baseline_root: Path,
    target_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    ensure_original(path, target_root, baseline_root, originals, previous_manifest, reconstruct_managed_block=True)
    existed = path.exists()
    backup = backup_current(path, backup_root, target_root)
    existing = path.read_text(encoding="utf-8", errors="ignore") if existed else ""
    block = managed_content(pointer)
    if BEGIN in existing and END in existing:
        start = existing.index(BEGIN)
        end = existing.index(END, start) + len(END)
        updated = existing[:start].rstrip() + "\n\n" + block + existing[end:].lstrip("\n")
    elif existing.strip():
        updated = existing.rstrip() + "\n\n" + block
    else:
        updated = block
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")
    records.append({
        "path": path.relative_to(target_root).as_posix(),
        "action": "managed_block",
        "created": not existed,
        "backup": backup,
        "installed_sha256": sha256(path),
    })


def copy_file(
    source: Path,
    destination: Path,
    backup_root: Path,
    baseline_root: Path,
    target_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    ensure_original(destination, target_root, baseline_root, originals, previous_manifest)
    existed = destination.exists()
    backup = backup_current(destination, backup_root, target_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    records.append({
        "path": destination.relative_to(target_root).as_posix(),
        "action": "file_copy",
        "created": not existed,
        "backup": backup,
        "installed_sha256": sha256(destination),
    })


def sync_managed_tree(
    source: Path,
    destination: Path,
    backup_root: Path,
    baseline_root: Path,
    target_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    for src in source.rglob("*"):
        if src.is_file():
            copy_file(src, destination / src.relative_to(source), backup_root, baseline_root, target_root, originals, previous_manifest, records)


def selected_skill_directories(mode: str) -> list[Path]:
    directories = [path for path in (PACK_ROOT / "agent-skills").iterdir() if path.is_dir()]
    if mode == "workflow":
        directories = [path for path in directories if path.name.startswith("wf-")]
    return sorted(directories, key=lambda path: path.name)


def _restore_previous_file(target_root: Path, record: dict[str, Any], originals: dict[str, dict[str, Any]]) -> None:
    rel = record.get("path")
    if not rel:
        return
    path = target_root / rel
    original = originals.get(rel)
    if original is not None:
        if path.exists():
            path.unlink(missing_ok=True)
        if original.get("existed") and original.get("backup"):
            backup = target_root / original["backup"]
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)
        return
    if record.get("created"):
        path.unlink(missing_ok=True)
    elif record.get("backup"):
        backup = target_root / record["backup"]
        if backup.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)


def prune_unselected_managed_skills(
    destination: Path,
    selected_names: set[str],
    target_root: Path,
    previous_manifest: dict[str, Any],
    originals: dict[str, dict[str, Any]],
) -> None:
    try:
        prefix = destination.relative_to(target_root).as_posix().rstrip("/") + "/"
    except ValueError:
        return
    for record in reversed(previous_manifest.get("records", [])):
        rel = str(record.get("path", ""))
        if record.get("action") != "file_copy" or not rel.startswith(prefix):
            continue
        remainder = rel[len(prefix):]
        skill_name = remainder.split("/", 1)[0]
        if not skill_name.startswith(("se-", "wf-")) or skill_name in selected_names:
            continue
        _restore_previous_file(target_root, record, originals)
    if destination.exists():
        for child in sorted(destination.iterdir(), reverse=True):
            if child.is_dir() and child.name.startswith(("se-", "wf-")) and child.name not in selected_names:
                for directory in sorted([p for p in child.rglob("*") if p.is_dir()], reverse=True):
                    try:
                        directory.rmdir()
                    except OSError:
                        pass
                try:
                    child.rmdir()
                except OSError:
                    pass


def sync_selected_skills(
    destination: Path,
    mode: str,
    backup_root: Path,
    baseline_root: Path,
    target_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    selected = selected_skill_directories(mode)
    selected_names = {path.name for path in selected}
    prune_unselected_managed_skills(destination, selected_names, target_root, previous_manifest, originals)
    for source_dir in selected:
        sync_managed_tree(source_dir, destination / source_dir.name, backup_root, baseline_root, target_root, originals, previous_manifest, records)


def copy_pack(
    destination: Path,
    backup_root: Path,
    baseline_root: Path,
    target_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    ensure_original(destination, target_root, baseline_root, originals, previous_manifest)
    existed = destination.exists()
    backup = backup_current(destination, backup_root, target_root)
    if destination.exists():
        shutil.rmtree(destination)

    def ignore(_directory, names):
        return {name for name in names if name in {".git", "__pycache__"} or name.endswith((".zip", ".pyc"))}

    shutil.copytree(PACK_ROOT, destination, ignore=ignore)
    records.append({
        "path": destination.relative_to(target_root).as_posix(),
        "action": "pack_tree",
        "created": not existed,
        "backup": backup,
        "installed_version": load_json(destination / "manifest.json", {}).get("version"),
    })


def _remove_hook_groups(settings: dict[str, Any], template: dict[str, Any]) -> None:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return
    for event, groups in template.get("hooks", {}).items():
        current = hooks.get(event)
        if not isinstance(current, list):
            continue
        remove = {json.dumps(group, sort_keys=True) for group in groups}
        hooks[event] = [group for group in current if json.dumps(group, sort_keys=True) not in remove]
        if not hooks[event]:
            hooks.pop(event, None)
    if not hooks:
        settings.pop("hooks", None)


def merge_claude_settings(
    target: Path,
    backup_root: Path,
    baseline_root: Path,
    originals: dict[str, dict[str, Any]],
    previous_manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    settings_path = target / ".claude" / "settings.json"
    template = load_json(PACK_ROOT / "provider-templates" / "claude" / "settings.skill-pack.json", {})
    ensure_original(
        settings_path, target, baseline_root, originals, previous_manifest,
        reconstruct_json_hook=template,
    )
    existed = settings_path.exists()
    backup = backup_current(settings_path, backup_root, target)
    existing = load_json(settings_path, {})
    hooks = existing.setdefault("hooks", {})
    for event, groups in template.get("hooks", {}).items():
        current = hooks.setdefault(event, [])
        rendered = {json.dumps(item, sort_keys=True) for item in current}
        for group in groups:
            if json.dumps(group, sort_keys=True) not in rendered:
                current.append(group)
    write_json(settings_path, existing)
    records.append({
        "path": settings_path.relative_to(target).as_posix(),
        "action": "json_merge_claude_hooks",
        "created": not existed,
        "backup": backup,
        "installed_sha256": sha256(settings_path),
        "template": template,
    })



PROVIDER_PATH_RULES = {
    "claude": ("CLAUDE.md", ".claude/skills/", ".claude/agents/", ".claude/settings.skill-pack.json", ".claude/settings.json"),
    "github": (".github/copilot-instructions.md", ".github/skills/", ".github/agents/", ".github/instructions/", ".github/workflows/engineering-quality-gate.yml"),
    "openai_agents": (".agents/skills/",),
    "gemini": ("GEMINI.md",),
    "cursor": (".cursor/rules/software-engineering.mdc",),
    "windsurf": (".windsurfrules",),
}


def _provider_group_enabled(group: str, providers: set[str]) -> bool:
    if group == "openai_agents":
        return bool(providers & {"openai", "agents"})
    return group in providers


def _path_matches_rules(rel: str, rules: tuple[str, ...]) -> bool:
    return any(rel == rule.rstrip("/") or rel.startswith(rule) for rule in rules)


def prune_disabled_provider_records(
    target: Path,
    providers: set[str],
    previous_manifest: dict[str, Any],
    originals: dict[str, dict[str, Any]],
) -> list[str]:
    disabled_rules = [
        rules for group, rules in PROVIDER_PATH_RULES.items()
        if not _provider_group_enabled(group, providers)
    ]
    if not disabled_rules:
        return []
    warnings: list[str] = []
    for record in reversed(previous_manifest.get("records", [])):
        rel = str(record.get("path", ""))
        if not rel or not any(_path_matches_rules(rel, rules) for rules in disabled_rules):
            continue
        path = target / rel
        action = record.get("action")
        if action == "managed_block":
            if path.exists() and path.is_file():
                updated = remove_managed_block_text(path.read_text(encoding="utf-8", errors="ignore")).strip()
                if updated:
                    path.write_text(updated + "\n", encoding="utf-8")
                else:
                    path.unlink()
        elif action == "json_merge_claude_hooks":
            if path.exists() and path.is_file():
                value = load_json(path, {})
                _remove_hook_groups(value, record.get("template", {}))
                if value:
                    write_json(path, value)
                else:
                    path.unlink()
        elif action == "file_copy":
            if not path.exists() or not path.is_file():
                continue
            installed_hash = record.get("installed_sha256")
            if installed_hash and sha256(path) != installed_hash:
                warnings.append(f"Preserved modified previously managed file: {rel}")
                continue
            _restore_previous_file(target, record, originals)
    return warnings


def disable_claude_settings_hook(target: Path, previous_manifest: dict[str, Any]) -> None:
    settings_path = target / ".claude" / "settings.json"
    if not settings_path.exists() or not settings_path.is_file():
        return
    templates = [
        record.get("template", {})
        for record in previous_manifest.get("records", [])
        if record.get("path") == ".claude/settings.json" and record.get("action") == "json_merge_claude_hooks"
    ]
    if not templates:
        templates = [load_json(PACK_ROOT / "provider-templates" / "claude" / "settings.skill-pack.json", {})]
    value = load_json(settings_path, {})
    for template in templates:
        _remove_hook_groups(value, template)
    if value:
        write_json(settings_path, value)
    else:
        settings_path.unlink()


def install(args) -> int:
    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    engineering = target / ".engineering"
    manifest_path = engineering / "install-manifest.json"
    previous_manifest = load_json(manifest_path, {})
    originals = dict(previous_manifest.get("originals", {}))
    baseline_root = engineering / "backups" / "original-baseline"
    backup_root = engineering / "backups" / f"install-{utc_stamp()}"
    backup_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    providers = provider_set(args.providers)
    prune_warnings = prune_disabled_provider_records(target, providers, previous_manifest, originals)

    previous_hooks_enabled = bool(previous_manifest.get("claude_hooks_enabled"))
    hooks_enabled = bool("claude" in providers and (args.enable_claude_hooks or (previous_hooks_enabled and not args.disable_claude_hooks)))
    if args.disable_claude_hooks:
        disable_claude_settings_hook(target, previous_manifest)

    destination = engineering / "skill-pack"
    copy_pack(destination, backup_root, baseline_root, target, originals, previous_manifest, records)

    pointer = """Read `.engineering/skill-pack/docs/agent/START-HERE.md`.
Use the installed workflow Agent Skills under `.agents/skills` or the provider-specific skills directory.
Load engineering-area skills from the task context bundle; do not load all 80 areas globally.
Inspect before asking; follow the action-risk and evidence policies."""

    merge_managed_block(target / "AGENTS.md", pointer, backup_root, baseline_root, target, originals, previous_manifest, records)

    if "claude" in providers:
        merge_managed_block(target / "CLAUDE.md", pointer, backup_root, baseline_root, target, originals, previous_manifest, records)
        sync_selected_skills(target / ".claude" / "skills", args.skill_install_mode, backup_root, baseline_root, target, originals, previous_manifest, records)
        sync_managed_tree(PACK_ROOT / "provider-templates" / "claude" / "agents", target / ".claude" / "agents", backup_root, baseline_root, target, originals, previous_manifest, records)
        copy_file(PACK_ROOT / "provider-templates" / "claude" / "settings.skill-pack.json", target / ".claude" / "settings.skill-pack.json", backup_root, baseline_root, target, originals, previous_manifest, records)
        if hooks_enabled:
            merge_claude_settings(target, backup_root, baseline_root, originals, previous_manifest, records)

    if "github" in providers:
        merge_managed_block(target / ".github" / "copilot-instructions.md", pointer, backup_root, baseline_root, target, originals, previous_manifest, records)
        sync_selected_skills(target / ".github" / "skills", args.skill_install_mode, backup_root, baseline_root, target, originals, previous_manifest, records)
        sync_managed_tree(PACK_ROOT / "provider-templates" / "github" / "agents", target / ".github" / "agents", backup_root, baseline_root, target, originals, previous_manifest, records)
        sync_managed_tree(PACK_ROOT / "provider-templates" / "github" / "instructions", target / ".github" / "instructions", backup_root, baseline_root, target, originals, previous_manifest, records)
        copy_file(PACK_ROOT / "provider-templates" / "github" / "engineering-quality-gate.yml", target / ".github" / "workflows" / "engineering-quality-gate.yml", backup_root, baseline_root, target, originals, previous_manifest, records)

    if "openai" in providers or "agents" in providers:
        sync_selected_skills(target / ".agents" / "skills", args.skill_install_mode, backup_root, baseline_root, target, originals, previous_manifest, records)

    if "gemini" in providers:
        merge_managed_block(target / "GEMINI.md", pointer, backup_root, baseline_root, target, originals, previous_manifest, records)

    if "cursor" in providers:
        copy_file(PACK_ROOT / "provider-templates" / "cursor" / "software-engineering.mdc", target / ".cursor" / "rules" / "software-engineering.mdc", backup_root, baseline_root, target, originals, previous_manifest, records)

    if "windsurf" in providers:
        merge_managed_block(target / ".windsurfrules", pointer, backup_root, baseline_root, target, originals, previous_manifest, records)

    history = list(previous_manifest.get("history", []))
    if previous_manifest.get("installed_at"):
        history.append({
            "installed_at": previous_manifest.get("installed_at"),
            "pack_version": previous_manifest.get("pack_version"),
            "providers": previous_manifest.get("providers", []),
            "skill_install_mode": previous_manifest.get("skill_install_mode", "all"),
            "backup_root": previous_manifest.get("backup_root"),
        })

    install_manifest = {
        "schema_version": 3,
        "installed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "pack_version": load_json(PACK_ROOT / "manifest.json", {}).get("version"),
        "source_pack": str(PACK_ROOT),
        "providers": sorted(providers),
        "skill_install_mode": args.skill_install_mode,
        "installed_provider_skill_count": len(selected_skill_directories(args.skill_install_mode)),
        "claude_hooks_enabled": hooks_enabled,
        "prune_warnings": prune_warnings,
        "backup_root": backup_root.relative_to(target).as_posix(),
        "baseline_root": baseline_root.relative_to(target).as_posix(),
        "originals": originals,
        "history": history[-20:],
        "records": records,
    }
    write_json(manifest_path, install_manifest)

    if not args.skip_quickstart:
        cmd = [
            sys.executable, "-S", str(destination / "sepack.py"), "quickstart",
            "--target", str(target), "--mode", args.mode, "--autonomy", args.autonomy,
        ]
        if args.goal:
            cmd += ["--goal", args.goal]
        if args.impact:
            cmd += ["--impact", args.impact]
        if args.delegate_safe_work:
            cmd.append("--delegate-safe-work")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("Quickstart reported findings. The pack is installed; run doctor for details.", file=sys.stderr)

    print(f"Installed v2.0.1 skill pack to {destination}")
    print("The AI should read AGENTS.md and manage internal engineering state itself.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or upgrade the agent-native Software Engineering Skill Pack")
    parser.add_argument("--target", required=True)
    parser.add_argument("--providers", default="all")
    parser.add_argument("--skill-install-mode", choices=["workflow", "all"], default="workflow",
                        help="Install only the 12 workflow skills by default. Use all only when the provider can handle a large skill catalogue.")
    parser.add_argument("--goal")
    parser.add_argument("--mode", default="guide_and_build")
    parser.add_argument("--autonomy", default="ask_before_material_decisions")
    parser.add_argument("--impact", choices=["L1", "L2", "L3", "L4"])
    parser.add_argument("--delegate-safe-work", action="store_true")
    hooks = parser.add_mutually_exclusive_group()
    hooks.add_argument("--enable-claude-hooks", action="store_true")
    hooks.add_argument("--disable-claude-hooks", action="store_true")
    parser.add_argument("--skip-quickstart", action="store_true")
    return install(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
