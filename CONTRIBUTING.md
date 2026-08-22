# Contributing

Thank you for improving the SEForge. Contributions should make the pack more accurate, safer, easier to use, and easier to verify.

## Before opening a pull request

1. Read `AGENTS.md`, `docs/agent/START-HERE.md`, and `docs/security/AGENT-SECURITY.md`.
2. Keep changes scoped and explain the user-visible outcome.
3. Update the relevant Agent Skill, detailed reference, templates, tests, and source map together.
4. Do not add copyrighted source documents, secrets, personal data, or unverified claims.
5. Preserve the separation between verified facts, inference, defaults, and unresolved questions.

## Validate locally

```bash
python -S schemas/validate_pack.py
python -S -m unittest discover -s tests -p "test_*.py" -v
python -S evals/run_evals.py
python -S sepack.py integrity
```

After changing tracked files, maintainers must regenerate the integrity manifest only after all checks pass:

```bash
python -S sepack.py integrity --generate --maintainer
python -S sepack.py integrity
```

## Agent Skill changes

Every skill directory must contain:

```text
SKILL.md
references/detailed-guide.md
assets/checklist.md
```

`SKILL.md` must remain concise and use valid YAML front matter. Deep explanations belong in `references/`. Add or update deterministic tests when routing, policy, gates, command execution, installation, or evidence behavior changes.

## Pull request expectations

A pull request should include:

- purpose and scope;
- affected skills and workflows;
- security, compatibility, migration, and user-effort impact;
- commands actually run;
- evidence or screenshots when relevant;
- known limitations and residual risk.

See `.github/pull_request_template.md` for the complete checklist.
