# Independent Re-Audit Report — v2.0.1

**Audit date:** 2026-08-22
**Audited baseline:** `universal-software-engineering-skill-pack-v2.0-agent-native.zip`
**Corrected release:** `2.0.1`
**Final disposition:** PASS with documented residual limitations

## Honest conclusion

The original v2.0 archive was internally consistent, its checksum and ZIP structure were valid, and its original validator, 20 unit tests, and 9 behavioral evals passed. That did **not** mean every engineering path was correct. The fresh re-audit found material design, lifecycle, evidence, and execution-control gaps that the original test suite did not cover.

No confirmed critical vulnerability was found. The re-audit recorded **25 findings**:

- High: 6
- Medium: 16
- Low/documentation: 3
- Corrected or mitigated in v2.0.1: 24
- Residual architectural limitation: 1 — built-in project-command execution is not an OS sandbox

## Audit scope

The review covered:

- all 80 engineering-area Agent Skills and 12 workflow Agent Skills;
- root, provider, and path-specific instructions;
- context budgets and task-specific routing;
- repository discovery and project-profile inference;
- command discovery, review, execution, environment, and output handling;
- task creation, approval, evidence mapping, task gates, and release gates;
- evidence files, ledger chain, attachment integrity, and tamper detection;
- installation, provider changes, hooks, upgrades, uninstall, and restoration;
- state migration, schema versions, integrity manifests, tests, evals, and ZIP packaging;
- current official OpenAI, GitHub, Claude, MCP, and GitHub Actions guidance.

## Findings and corrections

| ID | Severity | Finding in v2.0 | v2.0.1 correction |
|---|---|---|---|
| RA-01 | High | Release readiness did not re-run the gate for every completed task. A previously forced or later-invalid task could remain marked complete. | `release_gate()` now evaluates every completed/closed task and blocks release when any task gate fails. |
| RA-02 | High | A task needed only some passing evidence; evidence was not mapped to each acceptance criterion. | Added `acceptance_evidence` mapping. Every criterion requires linked passing evidence; unrelated evidence cannot close the task. |
| RA-03 | High | Multi-upgrade uninstall could restore the immediately previous installed version instead of the pre-first-install user baseline. | Installer schema v3 preserves a permanent original baseline; `--restore-backups` restores every baseline entry after any number of upgrades. |
| RA-04 | High | Reducing the provider set could leave old provider skills, agents, instructions, or Claude hooks behind. | Added provider lifecycle pruning, unchanged-file restoration, modified-file preservation warnings, and hook cleanup. |
| RA-05 | High | Project-defined commands could run with a one-time review or a direct trust flag, while the runtime did not clearly state that execution was unsandboxed. | Project commands now have an R2 risk floor and require both a persisted definition/source review and per-invocation `--trust-project-scripts`. Evidence records state the isolation boundary. |
| RA-06 | High | Evidence verification checked the ledger and attachments but did not fully compare duplicate record files, reject missing external sources at record time, or detect all duplicate IDs. | Evidence creation rejects external/missing sources; verification checks record copies, source existence/hash, duplicate IDs, attachments, and chain integrity. |
| RA-07 | Medium | Python `compileall .` traversed installed tooling/provider trees and produced bytecode. | Replaced with a pack-owned AST syntax checker that excludes tooling/build/virtual-environment trees and writes no bytecode. |
| RA-08 | Medium | Verification subprocess environment dropped `PYTHONDONTWRITEBYTECODE`, allowing project tests to create `__pycache__`. | The execution environment now forces `PYTHONDONTWRITEBYTECODE=1`; regression tests confirm no bytecode pollution. |
| RA-09 | Medium | The presence of a `tests/` directory could select pytest even when pytest was not declared. | Pytest is selected only when declared; otherwise standard-library unittest discovery is registered. |
| RA-10 | Medium | The validator used `py_compile`, mutating the pack it was supposed to validate. | Validator uses `ast.parse` and has a no-bytecode mutation regression test. |
| RA-11 | Medium | The eval runner overwrote a tracked results file by default, invalidating pack integrity after evaluation. | Default eval execution is read-only; writing results requires an explicit `--output`. |
| RA-12 | Medium | Installing all 92 skills into every provider discovery directory by default could exceed initial metadata budgets and cause omission/truncation. | Default provider installation exposes only 12 workflow skills. Engineering-area skills remain task-loaded; all 92 are opt-in. |
| RA-13 | Medium | Engineering skill descriptions were long and repetitive, increasing initial metadata pressure. | Regenerated concise descriptions and added a validator budget check. |
| RA-14 | Medium | Manual evidence was not consistently added to the task's evidence index. | Manual and command evidence now update task evidence IDs and optional criterion links atomically through the CLI flow. |
| RA-15 | Medium | Repository discovery could inspect a file symlink resolving outside the project root. | External-resolving file symlinks are skipped; a boundary regression test was added. |
| RA-16 | Medium | Expected CLI failures could emit full Python tracebacks. | Added concise top-level error handling; maintainers can restore tracebacks with `SEPACK_DEBUG=1`. |
| RA-17 | Medium | Claude hook enablement was not a complete lifecycle state; later upgrades/provider changes could leave the hook behind. | Hook state persists across Claude upgrades, can be disabled explicitly, and is removed when Claude is no longer selected. |
| RA-18 | Medium | Provider-managed files modified by the user did not have an explicit preservation policy during provider removal. | Modified files are preserved and reported in `prune_warnings`; unchanged managed files are restored or removed safely. |
| RA-19 | Medium | GitHub Actions templates used outdated major action versions. | Updated to current major templates and added immutable-SHA guidance for high-assurance repositories. |
| RA-20 | Medium | The v2 distribution schema still required `2.0.0` after the corrected runtime version changed. | Schema and validator now require `2.0.1`. |
| RA-21 | Medium | Validator coverage did not verify every manifest skill path, provider agent front matter, metadata budget, all local Markdown links, installer default mode, or stale command names. | Expanded deterministic distribution validation across all these areas. |
| RA-22 | Medium | The keyword `standard` over-activated interoperability engineering for phrases such as “Python standard-library tests.” | Replaced with precise conformance phrases and added a routing precision test. |
| RA-23 | Medium | Documentation referred to a nonexistent hyphenated task context command. | Corrected to `task context`; validator rejects the stale backticked command form. |
| RA-24 | Low | Validation and end-to-end reports still described the earlier all-92 default and v2.0 counts. | Rebuilt reports from the v2.0.1 test and E2E results. |
| RA-25 | Low / residual | `--allow-network` is policy acknowledgement, not an OS firewall; local project code can access the filesystem/network unless the host isolates it. | Clearly documented; project commands require review and per-invocation trust. Untrusted code must run in an external container, VM, restricted CI runner, or equivalent sandbox. |

## Verification performed

### Static distribution validation

- 80 engineering skills present
- 12 workflow skills present
- 92 total canonical Agent Skills
- unique valid skill names and front matter
- manifest paths and deep references present
- provider agent front matter valid
- workflow metadata budget below 8,000 characters
- all local Markdown links checked
- current schema and installer defaults checked
- Python parsed without generating bytecode
- JSON files parsed
- duplicate legacy trees absent

### Unit and regression tests

- 17 test files
- 39 test cases
- 39 passed
- 0 failed

The suite covers routing, context limits, prompt-injection patterns, command risk, command review, per-invocation trust, source-hash invalidation, secret redaction, evidence tamper detection, acceptance-evidence coverage, release regression, symlink boundaries, Python command isolation, state migration, provider lifecycle, hook lifecycle, multi-upgrade restoration, CLI errors, validator immutability, eval immutability, and pack integrity.

### Behavioral evals

- 9 cases
- 9 passed
- 0 failed

### End-to-end scenario

The final scenario passed:

1. all-provider installation with the default 12-workflow catalogue;
2. existing `AGENTS.md`, `CLAUDE.md`, Claude permissions, and unrelated user hook preservation;
3. provider-content exclusion from project inference;
4. installed-pack integrity and doctor checks;
5. bounded task context and task-specific skill routing;
6. pack-owned Python syntax verification;
7. blocked unreviewed project tests;
8. blocked reviewed project tests without per-invocation trust;
9. real unittest execution with evidence linked to its acceptance criterion;
10. no bytecode/cache mutation;
11. task and release gates;
12. evidence-chain verification;
13. upgrade from 12 to 92 provider-visible skills and prune back to 12;
14. provider removal and hook cleanup;
15. exact restoration of the pre-first-install baseline after multiple upgrades.

See `evals/latest-e2e.json`.

## Residual limitations

The corrected pack is not a universal security boundary:

- Provider client applications were not launched in the audit container. Their generated structures, metadata, hooks, instructions, lifecycle behavior, and counts were tested.
- Built-in command execution is a local process boundary, not an OS filesystem/network sandbox.
- Pattern-based prompt-injection and secret redaction are defense in depth, not semantic guarantees.
- The E2E project used Python; other supported ecosystems are covered by discovery logic and unit tests but not every toolchain was installed and executed.
- Legal, safety, clinical, financial, regulatory, and certification decisions still require competent authorized specialists.
- Official provider and protocol formats can change; high-stakes use requires periodic source revalidation.

## Final assessment

v2.0.1 is materially safer and more trustworthy than the original v2.0. The audited controls now behave consistently with the stated workflow, and the final release is suitable as a professional engineering-assistance pack within the documented trust and sandbox limitations. It must not be described as mathematically perfect, formally certified, or a replacement for specialist authorization.
