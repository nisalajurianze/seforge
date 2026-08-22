---
name: wf-performance-investigation
description: Use for latency, throughput, resource, scaling, cost-performance, or responsiveness problems; requires measurement before optimization.
---

# Performance Investigation

## Invoke when

- slow system
- latency regression
- capacity concern
- resource spike
- scaling problem

## Procedure

1. Define user-visible metric, workload, environment, and baseline.
2. Instrument and profile before changing code.
3. Locate the dominant bottleneck and verify causality.
4. Form a hypothesis and change one major variable at a time.
5. Re-run representative benchmarks including tail behavior and resource use.
6. Check correctness, cost, reliability, and regression impact.

## Required outputs

- performance baseline
- profile
- hypothesis log
- benchmark evidence
- capacity recommendation

## Completion gates

- [ ] measurement is representative
- [ ] bottleneck is demonstrated
- [ ] improvement is repeatable
- [ ] quality trade-offs are acceptable

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
