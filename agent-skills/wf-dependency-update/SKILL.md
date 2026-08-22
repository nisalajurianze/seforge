---
name: wf-dependency-update
description: Use to update libraries, runtimes, frameworks, actions, plugins, or toolchains while controlling compatibility, provenance, licenses, security, and rollback.
---

# Safe Dependency and Toolchain Update

## Invoke when

- dependency update
- runtime upgrade
- framework upgrade
- security patch
- CI action update

## Procedure

1. Identify direct and transitive impact, support status, changelog, and migration notes.
2. Verify package identity, source, license, and integrity.
3. Update lockfiles and toolchain pins reproducibly.
4. Run build, tests, compatibility, and affected security checks.
5. Review behavior changes, deprecations, performance, and operational impact.
6. Record rollback and update SBOM or inventory.

## Required outputs

- update decision
- locked dependency change
- compatibility evidence
- security evidence
- rollback note

## Completion gates

- [ ] source identity is verified
- [ ] lockfiles are updated
- [ ] affected tests pass
- [ ] breaking changes are handled
- [ ] rollback is known

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
