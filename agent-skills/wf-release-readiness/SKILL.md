---
name: wf-release-readiness
description: Use before production or customer release to prove scope, quality, security, operations, migration, rollback, documentation, and residual-risk acceptance.
---

# Release Readiness

## Invoke when

- production release
- customer rollout
- mobile store submission
- firmware release
- major deployment

## Procedure

1. Confirm approved scope, versions, artifacts, and target environments.
2. Verify project-native checks and relevant active-skill gates.
3. Review migrations, compatibility, backup, restore, rollback, and monitoring.
4. Confirm security, privacy, supply-chain, accessibility, performance, and support readiness as applicable.
5. Review known issues and obtain residual-risk acceptance.
6. Generate release evidence, notes, ownership, and post-release validation plan.

## Required outputs

- release report
- evidence index
- rollback plan
- release notes
- post-release validation plan

## Completion gates

- [ ] required checks pass
- [ ] artifacts are identifiable
- [ ] rollback is tested
- [ ] ownership is assigned
- [ ] residual risk is accepted

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
