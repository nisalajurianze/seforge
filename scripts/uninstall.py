#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any

BEGIN = "<!-- SEPACK:BEGIN v2 -->"
END = "<!-- SEPACK:END -->"


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


def remove_managed_block(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    if BEGIN not in text or END not in text:
        return
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    updated = (text[:start].rstrip() + "\n" + text[end:].lstrip("\n")).strip()
    if updated:
        path.write_text(updated + "\n", encoding="utf-8")
    else:
        path.unlink()


def remove_hook_groups(path: Path, template: dict[str, Any]) -> None:
    if not path.exists() or not path.is_file():
        return
    value = load_json(path, {})
    hooks = value.get("hooks")
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
        value.pop("hooks", None)
    if value:
        write_json(path, value)
    else:
        path.unlink()


def restore_original(target: Path, rel: str, state: dict[str, Any]) -> None:
    path = target / rel
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    if not state.get("existed"):
        return
    backup_rel = state.get("backup")
    if not backup_rel:
        raise RuntimeError(f"Original backup is missing for {rel}")
    backup = target / backup_rel
    if not backup.exists():
        raise RuntimeError(f"Original backup file does not exist: {backup_rel}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup.is_dir():
        shutil.copytree(backup, path)
    else:
        shutil.copy2(backup, path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove managed skill-pack files while preserving project state")
    parser.add_argument("--target", required=True)
    parser.add_argument("--restore-backups", action="store_true", help="Restore the baseline that existed before the first managed installation.")
    parser.add_argument("--remove-state", action="store_true")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    engineering = target / ".engineering"
    manifest_path = engineering / "install-manifest.json"
    manifest = load_json(manifest_path)
    if not manifest:
        raise SystemExit("No .engineering/install-manifest.json found.")

    records = list(reversed(manifest.get("records", [])))
    if args.restore_backups and manifest.get("originals"):
        originals = manifest["originals"]
        for rel in sorted(originals, key=lambda value: (value.count("/"), value), reverse=True):
            restore_original(target, rel, originals[rel])
    else:
        for record in records:
            path = target / record["path"]
            action = record.get("action")
            if action == "managed_block":
                remove_managed_block(path)
            elif action == "json_merge_claude_hooks":
                remove_hook_groups(path, record.get("template", {}))
            elif action == "file_copy":
                installed_hash = record.get("installed_sha256")
                unchanged = path.exists() and path.is_file() and installed_hash and sha256(path) == installed_hash
                if unchanged or record.get("created"):
                    path.unlink(missing_ok=True)
            elif action == "pack_tree" and path.exists():
                shutil.rmtree(path)

    manifest_path.unlink(missing_ok=True)
    if args.remove_state and engineering.exists():
        shutil.rmtree(engineering)
    print("Skill-pack managed installation removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
