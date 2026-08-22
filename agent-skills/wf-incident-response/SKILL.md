---
name: wf-incident-response
description: Use during operational failures, security incidents, data issues, or severe degradation to stabilize, preserve evidence, communicate, recover, and learn.
---

# Incident Response and Recovery

## Invoke when

- outage
- security incident
- data corruption
- severe degradation
- customer-impacting failure

## Procedure

1. Protect people and critical assets; declare incident scope and commander.
2. Stabilize service using the safest reversible action.
3. Preserve logs, timestamps, evidence, and chain of custody.
4. Communicate impact, uncertainty, and next update time.
5. Recover and validate user-visible outcomes and data integrity.
6. Complete a blameless timeline, root cause, corrective actions, and follow-up verification.

## Required outputs

- incident record
- timeline
- evidence set
- recovery validation
- post-incident actions

## Completion gates

- [ ] service is stabilized
- [ ] evidence is preserved
- [ ] recovery is validated
- [ ] owners and follow-ups exist

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
