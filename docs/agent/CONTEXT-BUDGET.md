# Context Budget and Progressive Disclosure

## Goal

Keep instructions high-signal. Large static context can reduce task performance and increase cost. The pack therefore uses Agent Skills and bounded task bundles.

## Initial context

Load only:

- root `AGENTS.md`;
- Agent Start Here;
- project fact summary;
- active task packet;
- approved plan or relevant milestone;
- selected workflow skill;
- selected engineering skills' front-matter and concise instructions.

## Deep references

Read `references/detailed-guide.md` only when:

- the task reaches a decision owned by that skill;
- a gate, artifact, anti-pattern, or source detail is needed;
- a reviewer disputes a claim;
- a high-impact decision needs stronger evidence.

## Limits

The generated task context should normally stay under:

- 4,000 words for small tasks;
- 8,000 words for normal feature work;
- 16,000 words for complex or high-risk work.

Exceeding the limit requires a reason and a narrower summary of prior material.

## Memory hygiene

- Store durable project facts in structured project state.
- Store decisions with rationale and expiry/review triggers.
- Do not append every conversation detail to permanent instructions.
- Remove or supersede stale instructions through versioned migrations.
- Keep provider root instruction files concise and route to skills/references.
