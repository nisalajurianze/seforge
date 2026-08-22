---
name: wf-data-migration
description: Use for database, schema, storage, data ownership, import, export, or platform migration with dry runs, reconciliation, rollback, and cutover controls.
---

# Data Migration and Reconciliation

## Invoke when

- database migration
- schema change
- legacy data move
- cloud migration
- data import or export

## Procedure

1. Inventory sources, targets, owners, volumes, constraints, and retention.
2. Define mapping, transformation, rejection, and reconciliation rules.
3. Create reversible expand-migrate-contract steps where possible.
4. Run dry runs with representative data and measure duration.
5. Validate counts, invariants, totals, referential integrity, and samples.
6. Define cutover, rollback, monitoring, and source-retirement criteria.

## Required outputs

- migration specification
- mapping catalogue
- dry-run evidence
- reconciliation report
- cutover and rollback plan

## Completion gates

- [ ] mapping is complete
- [ ] dry run succeeds
- [ ] reconciliation closes material gaps
- [ ] rollback is feasible
- [ ] retirement waits for acceptance

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
