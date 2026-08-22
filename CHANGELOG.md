# Changelog

## 2.0.1 Repository Finalization — 2026-08-22

- Added animated README poster, logo, social preview, and polished GitHub landing page.
- Added repository governance, security, support, contribution, conduct, roadmap, citation, publishing, and notice files.
- Added GitHub issue forms, pull-request template, quality workflow, tag-based release workflow, and Dependabot configuration.
- Verified the repository workflows against current 2026 action releases and pinned exact action versions.
- Added quick-start and architecture guides.
- Kept the audited runtime version at 2.0.1; this update changes repository presentation and publishing automation, not the runtime contract.

## 2.0.1 — 2026-08-22

### Independent re-audit corrections

- Re-audited the complete distribution, runtime, installer, provider adapters, evidence ledger, gates, tests, evals, and final archive.
- Changed provider installation to 12 workflow skills by default; the full 92-skill catalogue is opt-in.
- Shortened engineering skill descriptions to stay within provider metadata budgets.
- Fixed the stale hyphenated task context command name and strengthened documentation-link validation.
- Replaced mutating Python compilation with an isolated AST syntax checker that ignores installed tooling and creates no bytecode.
- Stopped the validator and default eval runner from modifying the pack during validation.
- Corrected Python test discovery so pytest is selected only when declared; otherwise standard-library unittest is used.
- Added concise CLI error handling with an opt-in debug traceback mode.
- Prevented repository discovery from following external file symlinks.
- Narrowed an over-broad `standard` routing keyword that falsely activated interoperability engineering.
- Hardened project-command execution: R2 risk floor, persisted definition/source review, per-invocation trust, output redaction, and explicit unsandboxed-execution metadata.
- Preserved `PYTHONDONTWRITEBYTECODE=1` in verification subprocesses.
- Added acceptance-criterion-to-evidence mapping; unrelated passing evidence can no longer prove task completion.
- Made release readiness re-run every completed task gate.
- Hardened evidence verification against duplicate IDs, missing sources, changed attachments, and tampered record copies.
- Fixed manual and command evidence linkage to tasks.
- Reworked installation baselines so `--restore-backups` returns to the pre-first-install state after multiple upgrades.
- Added provider removal/pruning, modified-file preservation, Claude-hook persistence, and explicit hook disablement.
- Updated GitHub Actions templates to current major versions and added high-assurance pinning guidance.
- Updated v2 schemas, validator coverage, validation report, and end-to-end evidence.

### Verified

- 80 engineering Agent Skills and 12 workflow Agent Skills.
- 39 unit tests passed.
- 9 deterministic behavioral evals passed.
- Full all-provider install, task, verification, release, upgrade, provider-prune, uninstall, and baseline-restore scenario passed.
- Final pack and ZIP integrity verified.

## 2.0.0 — 2026-08-22

### Agent-native architecture

- Converted all 80 engineering areas into standard Agent Skill directories with YAML-front-matter `SKILL.md`.
- Added 12 workflow skills for discovery, planning, feature delivery, bugs, security, dependencies, migrations, incidents, performance, architecture, releases, and retirement.
- Added progressive disclosure: concise root policy, task-selected skills, and deep references on demand.
- Added 4k/8k/16k task-context budgets.

### Professional runtime

- Replaced the v1 structural CLI with a modular standard-library Python engine.
- Added evidence-based repository discovery with confidence and source paths.
- Added project profiles and task-specific skill routing.
- Added project-native command discovery for Node, Python, Maven, Gradle, .NET, Go, Rust, PHP, Ruby, and Make.
- Added project-script trust review, network permission, timeouts, sanitized environment, and R0–R4 action-risk classification.
- Added task packets, risk classification, workflow selection, and self-contained ExecPlans.
- Added task and release gates that require actual evidence.

### Security

- Added trusted control-plane versus untrusted data-plane rules.
- Added direct and indirect prompt-injection handling.
- Added MCP and external-tool authorization policy.
- Added third-party skill provenance and least-privilege rules.
- Added optional Claude `PreToolUse` policy hook.
- Added independent planner, architecture, test, security, and release reviewer agents.

### Evidence and integrity

- Added SHA-256 command-output evidence.
- Added a hash-chained evidence ledger.
- Added evidence-tamper verification.
- Added full distribution file-hash manifest and integrity command.
- Added project-state snapshots and atomic state writes.

### Installation and lifecycle

- Added idempotent provider-native installation.
- Added managed instruction blocks that preserve project-owned rules.
- Added timestamped backups.
- Added state migration from v1 to v2.
- Added uninstall with optional backup restoration.
- Removed four duplicated copies of the detailed skill corpus; `agent-skills/` is now canonical.

### Quality assurance

- Added unit tests for skill format, routing, discovery, command policy, context budgets, evidence integrity, gates, and install/uninstall.
- Added deterministic behavioral eval cases for user-question limits, project routing, task routing, safety policy, prompt injection, context budgets, release blocking, and installer idempotence.
- Added provider CI template.

## 1.3.0

Zero-friction concierge release. Superseded by v2.0.
