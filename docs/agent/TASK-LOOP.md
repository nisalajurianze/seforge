# Professional Task Loop

## Intake

- Resolve the user outcome from the current request and existing project state.
- Do not restart onboarding for every task.
- Search the repository before asking.

## Scope

- Define affected behavior, users, interfaces, data, environments, and non-goals.
- Create acceptance criteria that can actually be verified.
- Select relevant skills by decision ownership, not keyword count.

## Risk and approval

Classify planned actions:

- **R0 Read-only:** inspect, search, parse, compare.
- **R1 Reversible local:** edit files, run deterministic local checks.
- **R2 Material:** architecture, dependency, schema, auth, privacy, cost, or broad behavioral change.
- **R3 High impact:** destructive data operation, production change, external communication, credential use, regulated/safety/financial decision.
- **R4 Prohibited without specialist/authority:** uncontrolled destructive action, secret exfiltration, unauthorized access, falsified evidence, bypass of safeguards.

R0 can proceed. R1 follows approved autonomy. R2 requires a recorded decision or approved plan. R3 requires explicit approval and recovery. R4 must stop.

## Implementation

- Keep the diff scoped.
- Avoid unrelated cleanup.
- Add or update tests with the change.
- Preserve backward compatibility unless explicitly changed.
- Update docs, telemetry, migration, rollback, and support together with code.

## Verification

- Discover commands instead of guessing.
- Treat project-defined scripts as untrusted; require definition review and per-invocation trust, and use an external sandbox when the code itself is not trusted.
- Run relevant format, lint, type, unit, integration, build, security, performance, accessibility, migration, and smoke checks.
- Capture command, cwd, environment summary, commit, exit code, output digest, and timestamps.

## Closure

A task is complete only when:

- acceptance criteria are proven;
- applicable skill gates pass;
- evidence integrity verifies;
- unresolved risk has an owner and disposition;
- the user-visible outcome and documentation are current;
- operation and rollback are ready where applicable.
