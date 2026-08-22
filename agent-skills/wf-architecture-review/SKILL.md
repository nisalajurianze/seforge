---
name: wf-architecture-review
description: Use for a new system, major redesign, service decomposition, platform choice, or architectural risk review.
---

# Architecture Review

## Invoke when

- new architecture
- major redesign
- service split
- platform change
- architecture review

## Procedure

1. Identify stakeholders, drivers, constraints, and quality-attribute scenarios.
2. Map context, boundaries, data ownership, trust, dependencies, and deployment.
3. Compare viable options and document trade-offs and exit costs.
4. Review failure, security, privacy, operations, migration, compatibility, and cost.
5. Record ADRs and measurable architecture fitness checks.

## Required outputs

- architecture views
- quality scenarios
- option analysis
- ADRs
- risk register
- fitness checks

## Completion gates

- [ ] drivers trace to decisions
- [ ] ownership and boundaries are explicit
- [ ] major risks have responses
- [ ] conformance can be tested

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
