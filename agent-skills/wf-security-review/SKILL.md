---
name: wf-security-review
description: Use for authentication, authorization, sensitive data, external exposure, dependencies, AI tools, or a requested security review.
---

# Security Review and Threat Validation

## Invoke when

- auth change
- sensitive data
- public endpoint
- dependency change
- security review
- AI agent or MCP integration

## Procedure

1. Define assets, actors, trust boundaries, entry points, and attacker goals.
2. Review authorization separately from authentication.
3. Check secrets, dependencies, input handling, output handling, logging, and update path.
4. Model prompt injection, tool poisoning, excessive agency, and data exfiltration for agentic systems.
5. Run relevant static, dependency, configuration, and integration tests.
6. Classify findings and require disposition for critical or high risk.

## Required outputs

- threat model
- security findings
- test evidence
- risk dispositions
- security release note

## Completion gates

- [ ] trust boundaries are explicit
- [ ] least privilege is verified
- [ ] critical findings are resolved or accepted
- [ ] evidence is current

## Operating rules

- Inspect before asking.
- Keep user questions material and minimal.
- Distinguish fact, inference, default, and unresolved uncertainty.
- Use the smallest safe reversible step.
- Record commands and evidence; never fabricate execution.
- Stop before destructive, externally consequential, sensitive, or irreversible action without the required approval.
- Update the shared plan, task packet, decisions, risks, and user-facing progress card.
