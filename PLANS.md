# PLANS.md — Execution Plans

Use an ExecPlan for multi-file, multi-hour, high-risk, migration, architecture, or long-horizon work.

An ExecPlan must be self-contained enough for an agent with only the current working tree and this plan.

## Required structure

### Purpose and user-visible outcome

Explain what changes and how a user or operator can observe success.

### Current state

Describe relevant architecture, files, behavior, constraints, tests, and known problems.

### Scope and non-goals

State what is included and intentionally excluded.

### Decisions and assumptions

Record selected options, alternatives, rationale, confidence, reversibility, and approvals.

### Security, privacy, data, operational, and migration impact

Address only what applies, but never silently omit a material impact.

### Milestones

For every milestone include:

- exact outcome;
- files or components expected to change;
- commands to validate;
- evidence to record;
- rollback or recovery;
- completion criterion.

### Progress

Maintain a timestamped checklist. Update it after every milestone.

### Discoveries

Record facts learned during implementation that change the plan.

### Validation

List actual project-native commands and user-visible verification. Do not use placeholder commands.

### Final outcome

Summarize delivered behavior, evidence, known limitations, residual risk, and follow-up work.

## Rules

- The plan is a living source of truth, not a one-time proposal.
- Fix failed validation before moving to a dependent milestone.
- Keep diffs scoped to the plan.
- Do not erase decision history; supersede it.
- Pause for material user decisions according to the project's autonomy level.
