# SE-79 — Search and Information-Retrieval Engineering

**Tier:** `specialized`
**Canonical file:** `079-search-and-information-retrieval-engineering.md`
**Intended use:** Direct project execution by an AI assistant, engineering team, reviewer, or auditor.

## 1. Purpose and precise definition

Build search systems with controlled ingestion, indexing, query understanding, ranking, freshness, access filtering, relevance evaluation, and regression protection.

This skill is an execution contract, not a study note. When activated, it must result in concrete decisions, project artifacts, implementation or configuration changes where needed, verification evidence, ownership, and an explicit statement of remaining limitations or risks.

## 2. When to activate

Activate this skill when one or more conditions apply:

- site search
- document discovery
- product search
- logs
- enterprise knowledge

Do not activate it only because a fashionable tool or term appears in the project. Activation must be justified by context, impact, lifecycle stage, product type, data, platform, user need, or obligation.

## 3. Required inputs

- Project goal, users, stakeholders, operating context, and measurable outcomes
- Functional, quality, security, privacy, data, operational, legal, and support requirements that apply
- Current architecture, interfaces, states, dependencies, environments, suppliers, and deployment model
- Risk and criticality classification, known incidents, defects, constraints, and assumptions
- Existing code, tests, telemetry, documentation, decisions, and evidence

Missing inputs must be recorded as assumptions. Decisions dependent on unresolved assumptions remain provisional.

## 4. AI and team execution contract

- Do not treat a document, diagram, tool output, or passing demo as completion by itself.
- Use measurable criteria instead of unsupported adjectives such as fast, secure, scalable, reliable, accessible, or compliant.
- State assumptions, uncertainty, alternatives, owners, review dates, and residual risk.
- Tailor effort to impact: lightweight evidence for low-risk work and independent, stronger evidence for high-consequence work.
- Maintain traceability from need or risk to decision, implementation, verification, ownership, and change history.
- Escalate or stop when a critical unknown makes a defensible decision impossible.
- Preserve existing correct behavior unless an approved change intentionally replaces it.
- Prefer primary, official, versioned sources for current standards, APIs, protocols, and platform behavior.

## 5. Step-by-step operating workflow

1. Confirm why **SE-79 Search and Information-Retrieval Engineering** is activated and define the current scope.
2. Inspect the existing system and gather the required inputs before proposing irreversible changes.
3. Convert relevant needs, threats, failures, obligations, or outcomes into measurable requirements.
4. Identify options and compare them using correctness, risk, complexity, cost, operability, maintainability, and exit criteria.
5. Record the decision, assumptions, rejected alternatives, owners, and verification obligations.
6. Create the required artifacts early enough to guide implementation rather than document it afterward.
7. Implement the smallest coherent control or design that satisfies the approved requirement.
8. Verify normal, invalid, boundary, misuse, dependency-failure, recovery, upgrade, and rollback scenarios as applicable.
9. Connect evidence to the project evidence register and resolve, mitigate, transfer, or formally accept remaining findings.
10. Reassess this skill after material changes to requirements, architecture, data, platform, supplier, threat, regulation, or operations.

## 6. Detailed competency map

- **Document ingestion** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Tokenization** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Indexing** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Query parsing** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Ranking** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Filters and facets** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Typo tolerance** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Synonyms** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Multilingual search** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Freshness** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Relevance judgments** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Precision and recall** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Ranking metrics** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Zero-result analysis** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Search latency** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Index consistency** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.
- **Privacy and access filtering** — establish the applicable requirement or risk; select a proportionate technique; define ownership and interfaces; implement or configure the control; verify normal, boundary, failure, recovery, and change behavior where relevant; retain evidence and review triggers.

For each competency, the project record should answer: **what applies, why it applies, who owns it, how it is implemented, how it is verified, what can change it, and what evidence proves the current claim**.

## 7. Required project artifacts

- search requirements
- document and query schema
- ranking strategy
- relevance judgment set
- offline evaluation
- access-filter design
- search-quality dashboard

Every artifact must include an owner, version or commit, status, creation/review date, applicable scope, links to requirements or risks, and the next review trigger.

## 8. Verification strategy

At minimum, select and document the relevant verification methods:

- Static review of requirements, architecture, configuration, code, data contracts, and procedures.
- Automated checks kept in version control where practical.
- Positive, negative, boundary, malformed, misuse, concurrency, and compatibility tests where applicable.
- Dependency, timeout, partial-failure, interruption, recovery, rollback, and restore tests where applicable.
- Representative performance, accessibility, usability, security, privacy, or domain validation where applicable.
- Independent review or assurance when project impact, regulation, safety, or financial exposure requires it.
- Post-release telemetry and operational validation for claims that cannot be fully established before deployment.

A verification record must identify the version, environment, data, method, expected result, actual result, outcome, evidence location, owner, and date.

## 9. Quality and completion gates

This skill may be marked complete for the current scope only when:

- evaluation set represents real queries
- permissions apply before results
- index freshness is measured
- ranking changes run regression
- zero-result causes are analyzed

Universal completion conditions also apply:

- Critical findings are resolved, mitigated, transferred, or accepted by an authorized owner.
- Evidence is reproducible, attributable, and protected from silent modification.
- Related requirements, tests, documentation, configuration, monitoring, support, and change records are updated.
- Known limitations, unsupported cases, expiry dates, and residual risks are explicit.
- A change trigger is defined so stale evidence is not treated as permanent truth.

## 10. Prohibited shortcuts and anti-patterns

- LIKE query as complete search
- click-through as sole relevance truth
- leaking restricted titles
- tuning on test set only

Also prohibited:

- Fabricating test execution, metrics, approvals, citations, or completion status.
- Hiding failed checks or relabeling them as environment problems without evidence.
- Treating a scanner, framework, vendor, certification logo, or AI-generated output as a substitute for engineering judgment.
- Marking the skill complete when ownership, operation, support, or future change handling is undefined.

## 11. Evidence checklist

- [ ] Activation reason and scope are recorded.
- [ ] Requirements, risks, assumptions, and decision criteria are explicit.
- [ ] Alternatives and trade-offs are documented.
- [ ] Required artifacts exist and have owners.
- [ ] Implementation or controls match the approved decision.
- [ ] Verification covers the applicable normal and adverse conditions.
- [ ] Findings and residual risks have dispositions.
- [ ] Related skills and project-wide traceability are updated.
- [ ] Operational ownership, monitoring, maintenance, and review triggers are assigned.
- [ ] Completion claim is supported by named evidence.

## 12. Integration with adjacent skills

- SE-14 — Data-Intensive Software Engineering
- SE-25 — Systems and System-of-Systems Engineering
- SE-30 — Internationalization Localization and Culturalization
- SE-31 — Interoperability and Standards-Conformance Engineering
- SE-64 — Data Provenance Lineage and Origin-Tracking Engineering
- SE-80 — Knowledge-Graph Ontology and Semantic-System Engineering

The project router may activate additional skills when this skill reveals new data sensitivity, physical impact, supplier dependency, platform behavior, threat, failure mode, or compliance obligation.

## 13. Source basis

### Uploaded academic foundation

The uploaded Software Engineering lectures and Ian Sommerville reference provide the baseline for professional software development, process models, Agile, requirements, design and implementation, testing, dependability and security, evolution, maintenance, and CASE tools. The repository-level source map identifies those files and routes unrelated AI-search handouts out of this pack.

### Current official or primary sources

- **NIST_TREC:** [NIST Text REtrieval Conference](https://trec.nist.gov/)
- **W3C_I18N:** [W3C Internationalization guidance](https://www.w3.org/International/)
- **ISO25010:** [ISO/IEC 25010:2023 — Product quality model](https://www.iso.org/standard/78176.html)

### Synthesis note

The workflow, artifacts, gates, anti-patterns, and evidence rules in this file are an original operational synthesis for direct project use. They do not reproduce a complete standard and do not by themselves establish formal certification or legal compliance.

## 14. Definition of done

The project can answer all of these questions with evidence:

1. Why was this skill activated?
2. What measurable need, risk, obligation, or outcome does it address?
3. What decision was made, and what alternatives were rejected?
4. What was implemented, configured, changed, or deliberately not changed?
5. How was the result verified under the relevant normal and adverse conditions?
6. Who owns operation, support, monitoring, review, and future change?
7. What limitations or residual risks remain, and who accepted them?
