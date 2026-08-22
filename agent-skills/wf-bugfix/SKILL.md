---
name: wf-bugfix
description: Use for defects, regressions, failing tests, incidents, or incorrect behavior; requires reproduction, root cause, minimal fix, regression proof, and impact review.
---

# Evidence-Driven Bug Fix

## Invoke when

- bug report
- failing test
- regression
- incorrect result
- production defect

## Procedure

1. Reproduce the problem or state why reproduction is unavailable.
2. Capture expected versus actual behavior and affected versions.
3. Identify root cause and nearby failure modes.
4. Add a failing regression test before or with the fix when practical.
5. Apply the smallest safe fix and avoid unrelated refactoring.
6. Run focused and affected regression tests.
7. Document residual risk, monitoring, and release notes where needed.

## Required outputs

- reproduction record
- root-cause analysis
- regression test
- minimal fix
- verification evidence

## Completion gates

- [ ] problem is reproduced or bounded
- [ ] root cause is supported
- [ ] regression test passes
- [ ] adjacent behavior is checked

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
