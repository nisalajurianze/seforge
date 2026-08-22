---
name: wf-project-discovery
description: Use at the start of a new or unfamiliar repository to inspect first, infer project facts, minimize user questions, and create a concise project brief.
---

# Project Discovery and Zero-Friction Intake

## Invoke when

- new repository
- unknown codebase
- user asks to make project professional
- project context missing

## Procedure

1. Read trusted root instructions and identify the user's requested outcome.
2. Inspect manifests, README, source layout, tests, CI, infrastructure, migrations, and recent changes.
3. Separate observed facts from inferences, defaults, and unresolved questions.
4. Run the project detector and command discovery in dry-run mode.
5. Activate only relevant engineering skills and assign confidence to each activation.
6. Produce a concise brief with Done, Current, Need from you, Risks, and Next.
7. Ask at most three material questions; use reversible defaults for low-risk unknowns.

## Required outputs

- project fact sheet
- initial skill manifest
- command registry
- concierge brief
- initial risk list

## Completion gates

- [ ] repository inspected before questions
- [ ] facts and assumptions separated
- [ ] no more than three initial questions
- [ ] high-impact unknowns remain visible

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
