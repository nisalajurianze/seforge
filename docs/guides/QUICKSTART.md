# Quick Start

## Install into a project

```bash
python -S scripts/install.py \
  --target /path/to/project \
  --providers all \
  --goal "Describe the user-visible project outcome" \
  --delegate-safe-work
```

The installer preserves existing project instructions, adds managed provider adapters, installs workflow skills, and creates `.engineering/` project state.

## Ask the AI normally

> Inspect this project, make it professional, use safe reversible defaults, and ask me only before material decisions.

The AI should inspect before asking, create scoped tasks, load only relevant skills, run reviewed project-native checks, record evidence, and report progress as:

```text
Done:
Current:
Need from you:
Risks:
Next:
```

## Verify the pack itself

```bash
python -S schemas/validate_pack.py
python -S -m unittest discover -s tests -p "test_*.py" -v
python -S evals/run_evals.py
python -S sepack.py integrity
```
