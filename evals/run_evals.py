#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK_ROOT))

from engine.commands import discover_commands
from engine.context import build_task_context
from engine.discovery import discover
from engine.gates import release_gate
from engine.policy import assess_command, scan_untrusted_text
from engine.routing import route_skills
from engine.state import ensure_layout
from engine.tasks import create_task, generate_exec_plan

def load_cases(path: Path):
    cases = []
    for file in sorted(path.glob("*.jsonl")):
        for line in file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                cases.append(json.loads(line))
    return cases

def write_project(root: Path, description: str = "Demo API", files: list[str] | None = None):
    (root / "README.md").write_text(f"# Demo\n\n{description}\n", encoding="utf-8")
    (root / "package.json").write_text(json.dumps({
        "name":"eval-project",
        "description":description,
        "scripts":{"test":"echo ok","build":"echo build"}
    }), encoding="utf-8")
    for rel in files or ["src/index.js"]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("// eval\n", encoding="utf-8")
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests" / "basic.test.js").write_text("// eval test\n", encoding="utf-8")

def run_case(case: dict) -> tuple[bool, dict]:
    kind = case["type"]
    exp = case["expect"]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        if kind == "command_policy":
            result = assess_command(case["input"]["command"]).to_dict()
            ok = all(result.get(k) == v for k, v in exp.items())
            return ok, result

        if kind == "prompt_injection":
            findings = scan_untrusted_text(case["input"]["text"])
            result = {"finding_count": len(findings), "findings": findings}
            return len(findings) >= exp["minimum_findings"], result

        if kind == "question_budget":
            write_project(root, "Small demo")
            process = subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "init",
                "--target", str(root), "--json"
            ], capture_output=True, text=True, timeout=30)
            payload = json.loads(process.stdout)
            result = {"question_count": len(payload.get("material_questions", []))}
            return process.returncode == 0 and result["question_count"] <= exp["max_questions"], result

        if kind == "routing":
            write_project(root, case["input"]["description"], case["input"]["files"])
            ensure_layout(root)
            facts = discover(root)
            manifest = route_skills(root, PACK_ROOT, facts, {"impact_level":"L3"})
            active = {s["id"] for s in manifest["skills"] if s["status"] == "active"}
            result = {"active_skill_ids": sorted(active)}
            return set(exp["active_skill_ids"]).issubset(active), result

        if kind == "task_routing":
            write_project(root, "Identity API", case["input"]["files"])
            subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "init",
                "--target", str(root), "--goal", "Secure identity API", "--json"
            ], capture_output=True, text=True, timeout=30, check=True)
            task = create_task(root, name=case["input"]["name"], description=case["input"]["description"],
                               files=case["input"]["files"], acceptance_criteria=["works","negative case"])
            generate_exec_plan(root, task)
            context = build_task_context(root, PACK_ROOT, task["id"], budget_name="small", max_skills=exp["max_selected"])
            selected = set(context["selected_skill_ids"])
            result = context
            ok = set(exp["required_skill_ids"]).issubset(selected) and len(selected) <= exp["max_selected"]
            return ok, result

        if kind == "context_budget":
            write_project(root, "Auth API", ["src/auth.js"])
            subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "init",
                "--target", str(root), "--goal", "Secure auth API", "--json"
            ], capture_output=True, text=True, timeout=30, check=True)
            task = create_task(root, name="Add secure login",
                               description="Authentication sessions authorization negative tests",
                               files=["src/auth.js"], acceptance_criteria=["works","rejects invalid"])
            generate_exec_plan(root, task)
            result = build_task_context(root, PACK_ROOT, task["id"],
                                        budget_name=case["input"]["budget"],
                                        max_skills=case["input"]["max_skills"])
            ok = result["actual_words"] <= exp["max_words"] and len(result["selected_skill_ids"]) <= exp["max_skills"]
            return ok, result

        if kind == "release_gate":
            write_project(root)
            subprocess.run([
                sys.executable, "-S", str(PACK_ROOT / "sepack.py"), "init",
                "--target", str(root), "--json"
            ], capture_output=True, text=True, timeout=30, check=True)
            result = release_gate(root)
            return result["ready"] is exp["ready"], result

        if kind == "install":
            (root / "AGENTS.md").write_text("# Existing\n\nKeep me.\n", encoding="utf-8")
            cmd = [
                sys.executable, "-S", str(PACK_ROOT / "scripts" / "install.py"),
                "--target", str(root), "--providers", case["input"]["providers"], "--skip-quickstart"
            ]
            first = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            second = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            text = (root / "AGENTS.md").read_text(encoding="utf-8")
            result = {
                "managed_block_count": text.count("SEPACK:BEGIN v2"),
                "preserve_existing": "Keep me." in text,
                "returncodes": [first.returncode, second.returncode],
            }
            ok = result["managed_block_count"] == exp["managed_block_count"] and result["preserve_existing"] == exp["preserve_existing"] and first.returncode == second.returncode == 0
            return ok, result

        return False, {"error": f"Unknown eval type: {kind}"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default=str(PACK_ROOT / "evals" / "cases"))
    parser.add_argument("--output", help="Optional JSON report path. Omit to keep the installed pack immutable.")
    args = parser.parse_args()

    cases = load_cases(Path(args.cases))
    results = []
    passed = 0
    for case in cases:
        try:
            ok, detail = run_case(case)
        except Exception as exc:
            ok, detail = False, {"error": repr(exc)}
        passed += int(ok)
        results.append({
            "id": case["id"],
            "description": case["description"],
            "passed": ok,
            "detail": detail,
        })
        print(f"{'PASS' if ok else 'FAIL'} {case['id']} — {case['description']}")

    report = {
        "case_count": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "results": results,
    }
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"case_count":len(cases),"passed":passed,"failed":len(cases)-passed}, indent=2))
    return 0 if passed == len(cases) else 1

if __name__ == "__main__":
    raise SystemExit(main())
