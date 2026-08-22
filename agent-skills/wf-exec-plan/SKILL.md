---
name: wf-exec-plan
description: Use for multi-file, multi-hour, risky, or milestone-based work that needs a self-contained execution plan and continuous progress tracking.
---

# Execution Plan for Long-Horizon Work

## Invoke when

- multi-file change
- migration
- large refactor
- multi-hour task
- high-risk implementation

## Procedure

1. Create a self-contained ExecPlan using PLANS.md.
2. Describe purpose, user-visible outcome, current state, constraints, and non-goals.
3. List milestones with validation after each milestone.
4. Record discoveries, decisions, progress, and remaining work continuously.
5. Keep diffs scoped; revise the plan when evidence changes.
6. End with reproducible run and validation instructions plus known limitations.

## Required outputs

- approved ExecPlan
- milestone checklist
- decision log
- validation log
- final outcome summary

## Completion gates

- [ ] plan is self-contained
- [ ] milestones are testable
- [ ] progress is current
- [ ] validation commands are real
- [ ] known issues are explicit

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
