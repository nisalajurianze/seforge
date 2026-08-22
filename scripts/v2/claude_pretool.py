#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACK_ROOT))

from engine.policy import assess_command

def emit(decision: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        emit("ask", "Skill-pack policy hook could not parse the tool request.")
        return 0

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool in {"Bash", "PowerShell"}:
        command = str(tool_input.get("command", ""))
        assessment = assess_command(command)
        if assessment.prohibited or assessment.risk == "R4":
            emit("deny", "Command is prohibited by the project action-risk policy: " + "; ".join(assessment.reasons))
        elif assessment.risk == "R3":
            emit("ask", "High-impact command requires explicit approval: " + "; ".join(assessment.reasons))
        return 0

    if tool in {"Write", "Edit"}:
        path = str(tool_input.get("file_path") or tool_input.get("path") or "")
        normalized = path.replace("\\", "/")
        protected = [
            "/.engineering/skill-pack/",
            "/AGENTS.md",
            "/.github/copilot-instructions.md",
            "/CLAUDE.md",
            "/GEMINI.md",
        ]
        if any(item in "/" + normalized.lstrip("/") for item in protected):
            emit("ask", "Editing agent policy or the installed skill pack requires explicit review.")
        return 0

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
