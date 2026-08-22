# Adaptive Project Interview Question Bank

The AI must use these questions progressively. It must not dump all questions on the user.

## Foundational interview

### F01 — intent
Me session eke oyata AI eken mona de karaganna one da?

- Why: The AI must know whether to guide, build, review, plan, audit, or answer before applying the engineering workflow.
- If unknown: `ask_for_mode_selection`
- Options: guide_and_build_with_me, review_and_improve_existing_project, create_plan_and_strategy_only, answer_questions_only, audit_and_fix_project, learn_or_explain

### F02 — project_stage
Project eka aluth ekakda, danata code/project ekak tiyenawada, nathnam production eke run wenawada?

- Why: Lifecycle stage changes the questions, risks, artifacts, and acceptable defaults.
- If unknown: `inspect_repository_and_select_existing_code_or_idea`
- Options: idea, planning, existing_code, in_development, production, maintenance, migration, retirement

### F03 — problem
Project eken solve karanna ona real problem eka mokakda?

- Why: A professional project must be driven by a validated problem rather than a technology choice.
- If unknown: `run_problem_discovery_and_do_not_commit_to_solution`
- Options: free text

### F04 — users
Main users saha stakeholders kawda? Oya danne nathnam users lage type eka kiyanna.

- Why: Requirements, accessibility, security, privacy, and validation depend on real users and decision owners.
- If unknown: `create_provisional_user_groups_and_mark_for_validation`
- Options: free text

### F05 — outcomes
Project eka success kiyala kiyanna puluwan measurable result monawada?

- Why: The AI needs measurable outcomes to avoid judging success only by completed features.
- If unknown: `propose_outcome_metrics_and_guardrails_for_approval`
- Options: free text

### F06 — scope
Must-have features, nice-to-have features, saha out-of-scope dewal monawada?

- Why: Scope controls schedule, architecture, verification, and release readiness.
- If unknown: `propose_minimum_viable_scope_based_on_risk_and_value`
- Options: free text

### F07 — platform
Meka web, mobile, desktop, API, cloud, embedded/IoT, data, AI, nathnam wena platform ekakda?

- Why: Platform determines architecture, testing, deployment, security, compatibility, and specialized skills.
- If unknown: `inspect_repository_and_recommend_the_simplest_suitable_platform`
- Options: web, mobile, desktop, backend_api, cloud, embedded_iot, data, ai_enabled, mixed, unknown

### F08 — data
Project eka collect/store/process karana data monawada? Personal, sensitive, financial, health, location, biometric data tiyenawada?

- Why: Data type controls privacy, security, retention, access, records, and erasure requirements.
- If unknown: `assume_personal_data_until_inventory_confirms_otherwise`
- Options: none, ordinary, personal, sensitive, financial, health, location, biometric, mixed, unknown

### F09 — impact
System eka fail unoth financial loss, safety harm, legal problem, data loss, nathnam major user impact wenawada?

- Why: Impact determines evidence rigor, independent review, and release gates.
- If unknown: `use_moderate_impact_and_escalate_when_harm_signals_exist`
- Options: low, moderate, high, critical, unknown

### F10 — constraints
Deadline, budget, team size, existing technology, hosting, devices, supplier, or university/company rules monawada?

- Why: Professional recommendations must fit real organizational and financial constraints.
- If unknown: `record_unknowns_and_choose_low_lock_in_reversible_options`
- Options: free text

### F11 — quality_priorities
Oyata wada important monawada: speed, security, reliability, usability, accessibility, low cost, scalability, maintainability, nathnam fast delivery?

- Why: Quality priorities drive architecture and trade-off decisions.
- If unknown: `balanced_quality_with_security_reliability_maintainability_baseline`
- Options: security, reliability, usability, accessibility, performance, scalability, maintainability, cost, delivery_speed, balanced, unknown

### F12 — deployment
System eka kohenda run karanne, kawda operate/support karanne, saha users lata release karanne kohomada?

- Why: A project is not complete without operation, support, monitoring, and recovery.
- If unknown: `recommend_simple_managed_deployment_with_clear_ownership_and_rollback`
- Options: free text

### F13 — approval
AI eka decision ganna one autonomy level eka monawada?

- Why: The AI must match the user's desired control and approval style.
- If unknown: `ask_before_major_decisions`
- Options: ask_before_every_change, ask_before_major_decisions, implement_reversible_changes_then_report, plan_only_no_code, answer_only

### F14 — communication
Plan eka follow karaddi updates denna one kohomada: feature-by-feature, daily milestones, phase gates, nathnam only blockers?

- Why: A shared working rhythm keeps the user and AI aligned.
- If unknown: `feature_by_feature_with_phase_gate_summaries`
- Options: feature_by_feature, daily_milestones, phase_gates, only_blockers, unknown

## Skill-level adaptive questions

### SE-01-Q1 — SWEBOK and Lifecycle Alignment
Me project ekata **SWEBOK and Lifecycle Alignment** adala wenawada? Udaharana signals: every software project, new project setup, lifecycle audit.

- Tier: `core`
- Why: Tailor a complete software lifecycle by mapping project work to recognized engineering knowledge areas, lifecycle processes, roles, outcomes, and evidence.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: project-context classification, lifecycle model selection, process tailoring, role and outcome mapping.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: tailored lifecycle map, knowledge-area coverage matrix, process responsibility matrix.

### SE-02-Q1 — Software Construction Engineering
Me project ekata **Software Construction Engineering** adala wenawada? Udaharana signals: any implementation work, code generation, refactoring.

- Tier: `core`
- Why: Turn approved designs into secure, readable, testable, efficient, portable, and maintainable executable software.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: language selection, type systems, memory and resource ownership, defensive programming.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: construction plan, coding standard, code-review checklist.

### SE-03-Q1 — Architecture Engineering and Governance
Me project ekata **Architecture Engineering and Governance** adala wenawada? Udaharana signals: new systems, major changes, distributed systems.

- Tier: `core`
- Why: Define and govern the system's fundamental structure, boundaries, responsibilities, quality trade-offs, and evolution constraints.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: architecture drivers, stakeholder concerns and viewpoints, context container component and deployment views, quality-attribute scenarios.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: architecture description, context and deployment views, ADR set.

### SE-04-Q1 — Software Configuration Management
Me project ekata **Software Configuration Management** adala wenawada? Udaharana signals: any team project, regulated work, multi-environment delivery.

- Tier: `core`
- Why: Identify, version, control, audit, and restore software artifacts, configurations, environments, schemas, and baselines.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: configuration identification, baselines, version control, branching and merging.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: configuration-management plan, configuration-item inventory, baseline register.

### SE-05-Q1 — Software Engineering Operations and SRE
Me project ekata **Software Engineering Operations and SRE** adala wenawada? Udaharana signals: production services, business-critical systems, 24x7 services.

- Tier: `core`
- Why: Engineer software as an operable service with explicit reliability objectives, ownership, capacity, incident response, recovery, and continual improvement.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: service ownership, service catalogue, SLIs SLOs and SLAs, error budgets.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: SLO document, production-readiness review, runbook set.

### SE-06-Q1 — Observability Engineering
Me project ekata **Observability Engineering** adala wenawada? Udaharana signals: distributed systems, production services, asynchronous flows.

- Tier: `core`
- Why: Design telemetry that allows teams to understand system behavior, user impact, causal paths, and failures across components and environments.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: telemetry requirements, structured logs, metrics, distributed traces.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: observability plan, telemetry schema, dashboard set.

### SE-07-Q1 — Reliability and Resilience Engineering
Me project ekata **Reliability and Resilience Engineering** adala wenawada? Udaharana signals: networked systems, critical workflows, external dependencies.

- Tier: `core`
- Why: Design systems to continue, degrade safely, recover predictably, and protect data when components, dependencies, or environments fail.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: failure-mode analysis, single points of failure, redundancy, graceful degradation.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: failure-mode register, resilience design, timeout and retry policy.

### SE-08-Q1 — Modern Software Security Engineering
Me project ekata **Modern Software Security Engineering** adala wenawada? Udaharana signals: every networked system, sensitive data, privileged operations.

- Tier: `core`
- Why: Integrate security requirements, threat analysis, secure design, implementation controls, verification, vulnerability response, and recovery into every lifecycle stage.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: security requirements, asset and trust-boundary analysis, threat modeling, abuse cases.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: threat model, security requirements, control matrix.

### SE-09-Q1 — Software Supply-Chain Engineering
Me project ekata **Software Supply-Chain Engineering** adala wenawada? Udaharana signals: third-party dependencies, CI/CD, package publication.

- Tier: `core`
- Why: Protect the integrity, transparency, provenance, licensing, and vulnerability posture of source, dependencies, builds, packages, and delivery channels.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: dependency inventory, SBOM, provenance, trusted builders.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: SBOM, provenance attestations, dependency policy.

### SE-10-Q1 — Product Engineering and Discovery
Me project ekata **Product Engineering and Discovery** adala wenawada? Udaharana signals: new products, uncertain requirements, feature prioritization.

- Tier: `core`
- Why: Ensure software work solves a validated user or business problem and is measured by outcomes rather than feature completion alone.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: problem discovery, user interviews, stakeholder needs, product vision.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: problem brief, opportunity map, hypothesis backlog.

### SE-11-Q1 — UX Interaction and Accessibility Engineering
Me project ekata **UX Interaction and Accessibility Engineering** adala wenawada? Udaharana signals: any user interface, public services, mobile or web apps.

- Tier: `core`
- Why: Design interactions that are understandable, efficient, inclusive, recoverable, and usable across devices, abilities, and contexts.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: information architecture, task flows, cognitive load, status feedback.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: interaction model, accessibility requirements, annotated wireframes.

### SE-12-Q1 — Privacy Engineering and Data Governance
Me project ekata **Privacy Engineering and Data Governance** adala wenawada? Udaharana signals: personal data, telemetry, analytics.

- Tier: `core`
- Why: Translate privacy obligations and individual-impact risks into data-minimizing architecture, controls, lifecycle rules, and verifiable user rights.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: data inventory, classification, purpose limitation, minimization.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: data inventory, processing-purpose register, privacy risk assessment.

### SE-13-Q1 — API and Integration Engineering
Me project ekata **API and Integration Engineering** adala wenawada? Udaharana signals: public or internal APIs, third-party integration, service boundaries.

- Tier: `core`
- Why: Design stable, secure, observable, evolvable contracts between components, organizations, devices, and external services.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: contract-first design, resource and operation modeling, schemas, error models.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: API specification, integration contract, error catalogue.

### SE-14-Q1 — Data-Intensive Software Engineering
Me project ekata **Data-Intensive Software Engineering** adala wenawada? Udaharana signals: analytics platforms, large datasets, ETL or ELT.

- Tier: `conditional`
- Why: Engineer reliable software around large, fast, heterogeneous, or long-lived data through explicit models, contracts, quality controls, pipelines, and recovery.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: transactional and analytical models, data contracts, schema evolution, validation.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: data architecture, data contracts, quality rules.

### SE-15-Q1 — Cloud-Native and Distributed Systems Engineering
Me project ekata **Cloud-Native and Distributed Systems Engineering** adala wenawada? Udaharana signals: cloud deployment, microservices, serverless.

- Tier: `conditional`
- Why: Design software for distributed execution, elastic infrastructure, partial failure, independent deployment, and cloud operational constraints.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: service boundaries, containers, orchestration, service discovery.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: cloud architecture, deployment topology, service dependency map.

### SE-16-Q1 — Platform Engineering and Developer Experience
Me project ekata **Platform Engineering and Developer Experience** adala wenawada? Udaharana signals: multiple teams, repeated setup work, inconsistent pipelines.

- Tier: `conditional`
- Why: Create reusable, secure, self-service engineering capabilities that reduce cognitive load and make the preferred path the easiest path.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: internal developer platform, golden paths, templates, self-service environments.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: platform product charter, golden-path templates, service catalogue.

### SE-17-Q1 — Release Engineering and Progressive Delivery
Me project ekata **Release Engineering and Progressive Delivery** adala wenawada? Udaharana signals: any production release, frequent delivery, high-risk change.

- Tier: `core`
- Why: Move verified changes into user environments safely through immutable artifacts, staged exposure, compatibility controls, evidence, and rollback or roll-forward.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: release policy, release candidates, artifact promotion, environment promotion.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: release plan, promotion record, feature-flag register.

### SE-18-Q1 — Engineering Measurement and Improvement
Me project ekata **Engineering Measurement and Improvement** adala wenawada? Udaharana signals: team improvement, delivery bottlenecks, quality trends.

- Tier: `core`
- Why: Use balanced, contextual metrics and experiments to understand delivery, quality, reliability, flow, and team outcomes and drive continual improvement.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: lead time, deployment frequency, failed-deployment recovery, change failure.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: measurement plan, metric definitions, baseline dashboard.

### SE-19-Q1 — Software Engineering Economics and FinOps
Me project ekata **Software Engineering Economics and FinOps** adala wenawada? Udaharana signals: cloud systems, build-buy decisions, costly scaling.

- Tier: `conditional`
- Why: Connect architecture and engineering choices to total cost, value, delay, risk, capacity, and accountable technology spending.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: total cost of ownership, build buy subscribe, opportunity cost, cost of delay.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: economic decision model, TCO estimate, unit-cost metrics.

### SE-20-Q1 — Sustainable Software Engineering
Me project ekata **Sustainable Software Engineering** adala wenawada? Udaharana signals: large compute, data centers, AI or ML.

- Tier: `conditional`
- Why: Reduce software-induced emissions and resource waste through measurable changes in energy, hardware use, carbon intensity, data movement, and workload timing.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: energy efficiency, carbon-aware execution, hardware efficiency, data-transfer reduction.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: sustainability baseline, functional unit, SCI calculation plan.

### SE-21-Q1 — Professional Practice Law and Governance
Me project ekata **Professional Practice Law and Governance** adala wenawada? Udaharana signals: every project, regulated domains, open-source use.

- Tier: `core`
- Why: Ensure engineering decisions are ethical, lawful, accountable, competent, transparent, and aligned with contractual and professional responsibilities.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: professional ethics, competence boundaries, honest estimates, intellectual property.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: governance register, obligation map, ethics and harm assessment.

### SE-22-Q1 — Documentation Engineering
Me project ekata **Documentation Engineering** adala wenawada? Udaharana signals: every project, APIs, operations.

- Tier: `core`
- Why: Treat documentation as versioned, tested, audience-specific product content required for use, development, operation, assurance, and change.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: documentation strategy, architecture docs, ADRs, API docs.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: documentation plan, audience map, docs repository.

### SE-23-Q1 — Legacy Modernization and Retirement
Me project ekata **Legacy Modernization and Retirement** adala wenawada? Udaharana signals: unsupported technology, high maintenance cost, migration.

- Tier: `conditional`
- Why: Assess, change, migrate, or retire legacy systems while preserving business behavior, data integrity, continuity, and recoverability.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: legacy inventory, business criticality, technical health, dependency discovery.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: legacy assessment, modernization option analysis, dependency map.

### SE-24-Q1 — Specialized Project Profile Routing
Me project ekata **Specialized Project Profile Routing** adala wenawada? Udaharana signals: project initiation, major scope change, new domain.

- Tier: `core`
- Why: Classify a project and activate only the engineering skills, rigor, evidence, and domain profiles that materially apply.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: platform classification, criticality, data sensitivity, regulatory context.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: project context profile, activated-skill manifest, skipped-skill rationale.

### SE-25-Q1 — Systems and System-of-Systems Engineering
Me project ekata **Systems and System-of-Systems Engineering** adala wenawada? Udaharana signals: hardware-software products, socio-technical systems, system-of-systems.

- Tier: `conditional`
- Why: Coordinate software with hardware, people, procedures, suppliers, physical environments, and other systems across the full system lifecycle.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: system of interest, boundaries, operational concepts, allocation to hardware software and people.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: operational concept, system context, requirement allocation.

### SE-26-Q1 — Formal Methods and Mathematical Verification
Me project ekata **Formal Methods and Mathematical Verification** adala wenawada? Udaharana signals: safety-critical logic, protocols, security-critical algorithms.

- Tier: `specialized`
- Why: Use mathematical specifications and analysis to prove or systematically check critical correctness properties beyond what testing alone can establish.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: formal specification, preconditions postconditions and invariants, state models, temporal logic.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: formal model, property catalogue, proof or model-check report.

### SE-27-Q1 — Software Safety Engineering
Me project ekata **Software Safety Engineering** adala wenawada? Udaharana signals: medical transport industrial aerospace energy robotics or other harm-capable systems.

- Tier: `specialized`
- Why: Prevent software from contributing to unacceptable harm by identifying hazards, deriving safety constraints, designing safe behavior, and maintaining safety evidence.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: hazard identification, severity and likelihood, safety constraints, safety requirements.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: hazard log, safety requirements, safety architecture.

### SE-28-Q1 — Assurance Cases Integrity Levels and Independent V&V
Me project ekata **Assurance Cases Integrity Levels and Independent V&V** adala wenawada? Udaharana signals: critical systems, certification, regulated release.

- Tier: `specialized`
- Why: Build structured claims, arguments, and independent evidence showing why a system is sufficiently trustworthy for its context and impact.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: top-level claims, subclaims, evidence, assumptions.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: assurance case, evidence index, integrity-level rationale.

### SE-29-Q1 — Human Factors and Socio-Technical Engineering
Me project ekata **Human Factors and Socio-Technical Engineering** adala wenawada? Udaharana signals: operator systems, decision support, high workload.

- Tier: `conditional`
- Why: Engineer the interaction of people, software, hardware, procedures, workload, incentives, and organization to reduce human-system failure.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: work context, cognitive and physical workload, attention and interruption, decision support.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: human-task analysis, operator journey, workload and error analysis.

### SE-30-Q1 — Internationalization Localization and Culturalization
Me project ekata **Internationalization Localization and Culturalization** adala wenawada? Udaharana signals: multi-country or multilingual users, public products, global data exchange.

- Tier: `conditional`
- Why: Design software, content, data, and workflows so they can be correctly adapted across languages, scripts, regions, formats, and cultures.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: Unicode and UTF-8, normalization, RTL and bidirectional text, font fallback.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: internationalization requirements, locale data model, translation-resource plan.

### SE-31-Q1 — Interoperability and Standards-Conformance Engineering
Me project ekata **Interoperability and Standards-Conformance Engineering** adala wenawada? Udaharana signals: cross-vendor integration, public standards, data exchange.

- Tier: `conditional`
- Why: Ensure systems exchange information and behavior correctly at syntactic, semantic, protocol, identity, timing, organizational, and lifecycle levels.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: syntactic semantic and organizational interoperability, shared vocabularies, canonical models, protocol conformance.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: standards profile, conformance matrix, interoperability test suite.

### SE-32-Q1 — Software Product-Line and Variability Engineering
Me project ekata **Software Product-Line and Variability Engineering** adala wenawada? Udaharana signals: white-label products, editions, regional variants.

- Tier: `specialized`
- Why: Manage a family of related products through reusable core assets, explicit variability, valid configurations, and product-line evolution.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: product-line scope, core assets, commonality, variability.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: product-line scope, feature model, variability rules.

### SE-33-Q1 — Domain Engineering and Bounded-Context Design
Me project ekata **Domain Engineering and Bounded-Context Design** adala wenawada? Udaharana signals: complex business rules, multiple teams, domain ambiguity.

- Tier: `conditional`
- Why: Capture complex business knowledge as explicit language, rules, models, ownership boundaries, and integration relationships.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: domain discovery, ubiquitous language, core supporting and generic domains, bounded contexts.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: domain glossary, context map, domain model.

### SE-34-Q1 — Real-Time Embedded and Cyber-Physical Systems Engineering
Me project ekata **Real-Time Embedded and Cyber-Physical Systems Engineering** adala wenawada? Udaharana signals: firmware, sensors and actuators, devices.

- Tier: `specialized`
- Why: Engineer software that interacts with hardware and physical processes under timing, resource, power, calibration, update, and safety constraints.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: hard and soft real-time, deadlines, worst-case execution, scheduling.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: timing requirements, hardware-software interface, resource budget.

### SE-35-Q1 — Protocol State-Machine and Workflow Correctness
Me project ekata **Protocol State-Machine and Workflow Correctness** adala wenawada? Udaharana signals: payments, approvals, bookings.

- Tier: `conditional`
- Why: Model stateful behavior explicitly so only valid transitions occur and timeouts, retries, crashes, duplicates, and version changes remain correct.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: states, transitions, events, guards.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: state model, transition table, invariant list.

### SE-36-Q1 — Concurrency Parallelism and Memory-Model Engineering
Me project ekata **Concurrency Parallelism and Memory-Model Engineering** adala wenawada? Udaharana signals: async servers, multi-threading, parallel algorithms.

- Tier: `conditional`
- Why: Design and verify correct behavior when work executes concurrently across threads, tasks, processes, cores, accelerators, or machines.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: threads processes and async, shared-state ownership, races, deadlocks.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: concurrency model, shared-state inventory, lock-order policy.

### SE-37-Q1 — Transaction Consistency and Data-Integrity Engineering
Me project ekata **Transaction Consistency and Data-Integrity Engineering** adala wenawada? Udaharana signals: money, inventory, bookings.

- Tier: `conditional`
- Why: Preserve business invariants and trustworthy records under concurrency, retries, partial failures, distributed execution, and recovery.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: transaction boundaries, atomicity, isolation, invariants.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: integrity model, transaction boundary map, invariant catalogue.

### SE-38-Q1 — Event-Driven Messaging and Streaming Engineering
Me project ekata **Event-Driven Messaging and Streaming Engineering** adala wenawada? Udaharana signals: queues, pub-sub, event sourcing.

- Tier: `conditional`
- Why: Build dependable asynchronous systems with explicit event contracts, delivery semantics, ordering, replay, compatibility, and operational controls.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: event contracts, event identity, correlation and causation, ordering.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: event catalogue, schema registry policy, delivery-semantics decision.

### SE-39-Q1 — Data Migration Conversion and Reconciliation Engineering
Me project ekata **Data Migration Conversion and Reconciliation Engineering** adala wenawada? Udaharana signals: legacy replacement, cloud migration, mergers.

- Tier: `conditional`
- Why: Move data between schemas, platforms, products, or owners while preserving meaning, integrity, completeness, traceability, and reversibility.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: source inventory, source-target mapping, profiling, cleaning.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: migration specification, mapping catalogue, dry-run report.

### SE-40-Q1 — Performance Modelling Capacity Scalability and Compatibility
Me project ekata **Performance Modelling Capacity Scalability and Compatibility** adala wenawada? Udaharana signals: user-facing services, high load, large data.

- Tier: `conditional`
- Why: Define measurable performance budgets, predict capacity, validate scaling and tail behavior, and preserve compatibility across versions and environments.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: workload models, concurrency, throughput, latency percentiles.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: performance requirements, workload model, capacity model.

### SE-41-Q1 — Software Acquisition Supplier and Third-Party Service Engineering
Me project ekata **Software Acquisition Supplier and Third-Party Service Engineering** adala wenawada? Udaharana signals: buy or subscribe decisions, outsourced development, critical SaaS.

- Tier: `conditional`
- Why: Select, contract, accept, monitor, and exit external software, SaaS, components, vendors, and development services using engineering evidence.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: acquisition requirements, build buy subscribe, supplier capability, technical due diligence.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: acquisition specification, supplier evaluation, technical due-diligence report.

### SE-42-Q1 — Open-Source Program Governance and Community Sustainability
Me project ekata **Open-Source Program Governance and Community Sustainability** adala wenawada? Udaharana signals: open-source dependencies, internal forks, publishing projects.

- Tier: `conditional`
- Why: Manage open-source use and contribution through policy, licensing, project health, security, sustainability, patching, and upstream relationships.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: usage policy, approval, licenses, maintainer activity.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: OSS policy, component assessment, license obligations.

### SE-43-Q1 — Compliance Engineering and Continuous Audit Evidence
Me project ekata **Compliance Engineering and Continuous Audit Evidence** adala wenawada? Udaharana signals: regulated sectors, contractual controls, certifications.

- Tier: `conditional`
- Why: Implement obligations as traceable controls, automated checks, durable evidence, owned exceptions, and continuously reviewable assurance.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: obligation register, control mapping, traceability, policy as code.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: obligation-control matrix, control implementation plan, evidence catalogue.

### SE-44-Q1 — Experimentation Feature Lifecycle and Product Analytics Governance
Me project ekata **Experimentation Feature Lifecycle and Product Analytics Governance** adala wenawada? Udaharana signals: A/B tests, feature flags, uncertain product changes.

- Tier: `conditional`
- Why: Evaluate product changes through controlled hypotheses, trustworthy exposure data, guardrail metrics, responsible rollout, and retirement decisions.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: hypothesis, primary and guardrail metrics, population, exposure logging.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: experiment protocol, metric definitions, exposure schema.

### SE-45-Q1 — AI-Assisted Software Development Governance
Me project ekata **AI-Assisted Software Development Governance** adala wenawada? Udaharana signals: AI coding assistants, generated tests, generated documentation.

- Tier: `conditional`
- Why: Govern AI coding, testing, documentation, review, and analysis tools so velocity gains do not weaken confidentiality, correctness, licensing, provenance, or accountability.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: approved tools, source confidentiality, prompt exposure, generated-code provenance.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: AI-use policy, tool risk assessment, generated-change review checklist.

### SE-46-Q1 — Engineering Knowledge Management Onboarding and Bus-Factor Reduction
Me project ekata **Engineering Knowledge Management Onboarding and Bus-Factor Reduction** adala wenawada? Udaharana signals: team growth, handover, critical experts.

- Tier: `core`
- Why: Preserve and transfer system, domain, operational, and decision knowledge so the project does not depend on inaccessible individuals.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: ownership map, domain glossary, ADRs, operational knowledge.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: knowledge map, ownership catalogue, onboarding plan.

### SE-47-Q1 — Reproducibility Hermetic Builds and Deterministic Environments
Me project ekata **Reproducibility Hermetic Builds and Deterministic Environments** adala wenawada? Udaharana signals: CI/CD, regulated builds, scientific software.

- Tier: `core`
- Why: Ensure a trusted artifact, environment, experiment, or result can be independently recreated from declared inputs and instructions.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: toolchain pinning, compiler and runtime versions, dependency locks, build inputs.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: reproducible build specification, pinned toolchain, environment manifest.

### SE-48-Q1 — Engineering Tools and CASE Automation Governance
Me project ekata **Engineering Tools and CASE Automation Governance** adala wenawada? Udaharana signals: tool selection, CASE tools, ALM platforms.

- Tier: `core`
- Why: Select and integrate engineering tools based on lifecycle value, interoperability, evidence quality, security, maintainability, and exit risk.
- If unknown: `activate_with_proportionate_standard_evidence`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: tool requirements, upper lower and integrated CASE, repositories, modeling.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: tool evaluation matrix, integration architecture, tool data-retention plan.

### SE-49-Q1 — Digital Identity and Access-Lifecycle Engineering
Me project ekata **Digital Identity and Access-Lifecycle Engineering** adala wenawada? Udaharana signals: user accounts, workforce access, SSO.

- Tier: `conditional`
- Why: Engineer identity proofing, enrollment, authentication, federation, sessions, authorization, recovery, privilege, and termination as one controlled lifecycle.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: identity proofing, enrollment, assurance levels, passwords MFA and passkeys.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: identity architecture, assurance-level decision, authenticator policy.

### SE-50-Q1 — Cryptographic Engineering Agility and Post-Quantum Migration
Me project ekata **Cryptographic Engineering Agility and Post-Quantum Migration** adala wenawada? Udaharana signals: sensitive data, signatures, secure channels.

- Tier: `conditional`
- Why: Apply cryptography correctly through asset inventory, approved algorithms, key lifecycle, protocol design, agility, deprecation, and migration planning.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: cryptographic inventory, algorithm selection, key generation storage rotation and revocation, certificates.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: cryptographic inventory, key-management plan, algorithm policy.

### SE-51-Q1 — Multi-Tenant SaaS Isolation Engineering
Me project ekata **Multi-Tenant SaaS Isolation Engineering** adala wenawada? Udaharana signals: multi-tenant SaaS, shared databases, shared queues.

- Tier: `specialized`
- Why: Prevent one tenant from accessing, influencing, exhausting, or observing another tenant's data, configuration, compute, keys, or operations.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: trusted tenant context, tenant authorization, data models, database isolation.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: tenancy model, isolation threat model, tenant-context propagation design.

### SE-52-Q1 — Offline-First Replication and Conflict-Resolution Engineering
Me project ekata **Offline-First Replication and Conflict-Resolution Engineering** adala wenawada? Udaharana signals: field apps, mobile, edge.

- Tier: `conditional`
- Why: Allow useful, correct operation during disconnection and safely reconcile local and remote changes after connectivity returns.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: local source of truth, offline reads and writes, pending operation queue, sync protocol.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: sync contract, offline capability matrix, conflict policy.

### SE-53-Q1 — Temporal Calendar and Timezone Correctness Engineering
Me project ekata **Temporal Calendar and Timezone Correctness Engineering** adala wenawada? Udaharana signals: appointments, billing, expiry.

- Tier: `conditional`
- Why: Model instants, local dates, calendar periods, schedules, recurrence, expiry, and clock behavior without timezone or daylight-saving ambiguity.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: instant versus local date, UTC, zone identifiers, offsets.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: temporal data model, timezone policy, recurrence specification.

### SE-54-Q1 — Numerical and Scientific Correctness Engineering
Me project ekata **Numerical and Scientific Correctness Engineering** adala wenawada? Udaharana signals: finance, simulation, graphics.

- Tier: `specialized`
- Why: Ensure calculations are mathematically appropriate, numerically stable, dimensionally correct, reproducible, and validated against trusted references.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: floating-point representation, rounding, precision loss, overflow and underflow.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: numerical requirements, precision and rounding policy, unit model.

### SE-55-Q1 — Secure Software Update Patch and Firmware Delivery
Me project ekata **Secure Software Update Patch and Firmware Delivery** adala wenawada? Udaharana signals: auto-update, package repositories, desktop apps.

- Tier: `conditional`
- Why: Deliver trustworthy updates despite repository compromise, network attack, key loss, interruption, rollback attempts, and constrained devices.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: update metadata, artifact signing, root keys, offline roots.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: update threat model, signing-key hierarchy, metadata policy.

### SE-56-Q1 — Records Retention Archival and Legal-Hold Engineering
Me project ekata **Records Retention Archival and Legal-Hold Engineering** adala wenawada? Udaharana signals: government, finance, healthcare.

- Tier: `conditional`
- Why: Manage authoritative records through capture, metadata, retention, legal hold, immutable history, retrieval, migration, and defensible disposal.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: record identification, classification, authoritative copy, metadata.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: records inventory, retention schedule, legal-hold workflow.

### SE-57-Q1 — Digital Forensics and Evidence-Readiness Engineering
Me project ekata **Digital Forensics and Evidence-Readiness Engineering** adala wenawada? Udaharana signals: security incidents, fraud, regulated logs.

- Tier: `conditional`
- Why: Design systems so incidents can be reconstructed using preserved, trustworthy, legally and ethically handled evidence.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: forensic logging, accurate timestamps, evidence-source inventory, log integrity.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: forensic-readiness plan, evidence-source map, chain-of-custody template.

### SE-58-Q1 — IT Service Management and Supportability Engineering
Me project ekata **IT Service Management and Supportability Engineering** adala wenawada? Udaharana signals: operational services, support desk, enterprise applications.

- Tier: `conditional`
- Why: Design software and operating processes so services can be requested, supported, changed, restored, reviewed, and continually improved.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: service definition, service ownership, service catalogue, support tiers.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: service definition, support model, request and incident workflows.

### SE-59-Q1 — IT Asset Software Inventory and End-of-Life Governance
Me project ekata **IT Asset Software Inventory and End-of-Life Governance** adala wenawada? Udaharana signals: production estates, licenses, cloud resources.

- Tier: `conditional`
- Why: Maintain accurate ownership, version, support, dependency, cost, renewal, and end-of-life information for technology assets.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: asset inventory, ownership, software and runtime inventory, cloud-resource inventory.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: asset register, ownership map, EOL calendar.

### SE-60-Q1 — Data Erasure Media Sanitization and Secure Disposal
Me project ekata **Data Erasure Media Sanitization and Secure Disposal** adala wenawada? Udaharana signals: device reuse, account deletion, decommissioning.

- Tier: `conditional`
- Why: Ensure data becomes infeasible to recover from active systems, replicas, backups, caches, devices, and media according to sensitivity and obligations.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: logical and physical deletion, cryptographic erase, snapshots, replicas.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: erasure scope map, sanitization decision, disposal procedure.

### SE-61-Q1 — Web Platform and Browser-Conformance Engineering
Me project ekata **Web Platform and Browser-Conformance Engineering** adala wenawada? Udaharana signals: web frontends, PWAs, browser extensions.

- Tier: `conditional`
- Why: Build standards-based web software that behaves securely, accessibly, progressively, and compatibly across browsers and constrained environments.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: semantic HTML, DOM behavior, browser security model, storage APIs.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: browser support policy, web architecture, compatibility matrix.

### SE-62-Q1 — Mobile Device-Ecosystem Engineering
Me project ekata **Mobile Device-Ecosystem Engineering** adala wenawada? Udaharana signals: Android or iOS apps, mobile SDKs, field apps.

- Tier: `conditional`
- Why: Engineer native and hybrid mobile software for lifecycle interruptions, permissions, storage, networks, battery, devices, OS versions, stores, and real-device behavior.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: app lifecycle, background execution, process termination, state restoration.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: mobile platform matrix, lifecycle state model, permission plan.

### SE-63-Q1 — Network and Transport-Protocol Engineering
Me project ekata **Network and Transport-Protocol Engineering** adala wenawada? Udaharana signals: distributed systems, APIs, streaming.

- Tier: `conditional`
- Why: Design application behavior around real transport semantics, latency, loss, intermediaries, DNS, TLS, retries, congestion, and partitions.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: TCP lifecycle, HTTP semantics, safe and idempotent methods, HTTP caching.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: network assumptions, timeout budget, retry policy.

### SE-64-Q1 — Data Provenance Lineage and Origin-Tracking Engineering
Me project ekata **Data Provenance Lineage and Origin-Tracking Engineering** adala wenawada? Udaharana signals: analytics, audit, machine learning.

- Tier: `conditional`
- Why: Record where data came from, who or what transformed it, which versions and activities produced outputs, and how to assess trust or reverse effects.
- If unknown: `inspect_project_signals_and_activate_only_if_relevant`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: source-system identity, data origin, data owner, creation activity.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: provenance model, lineage graph, dataset version register.

### SE-65-Q1 — Privacy-Enhancing Technology and Confidential-Computing Engineering
Me project ekata **Privacy-Enhancing Technology and Confidential-Computing Engineering** adala wenawada? Udaharana signals: cross-organization analytics, highly sensitive data, encrypted computation.

- Tier: `specialized`
- Why: Enable useful computation while reducing data exposure through trusted execution, differential privacy, advanced cryptography, and explicit privacy-utility trade-offs.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: data-use threat model, trusted execution environments, remote attestation, enclave lifecycle.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: PET selection analysis, threat and trust model, privacy budget.

### SE-66-Q1 — Trust Safety Abuse and Fraud-Resistance Engineering
Me project ekata **Trust Safety Abuse and Fraud-Resistance Engineering** adala wenawada? Udaharana signals: marketplaces, social platforms, payments.

- Tier: `specialized`
- Why: Prevent and respond to harmful or fraudulent use of otherwise valid features through abuse modeling, detection, friction, investigation, appeals, and measurement.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: abuse cases, misuse journeys, business-logic attacks, fraud scenarios.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: abuse threat model, misuse-case catalogue, detection and response policy.

### SE-67-Q1 — Digital-Content Authenticity and Media-Provenance Engineering
Me project ekata **Digital-Content Authenticity and Media-Provenance Engineering** adala wenawada? Udaharana signals: publishing, cameras, media editing.

- Tier: `specialized`
- Why: Attach and verify cryptographic provenance for media and documents while preserving edit history, trust context, revocation, interoperability, and privacy.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: capture-time provenance, creator identity, edit history, signed manifests.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: content provenance profile, signing and verification design, trust-store policy.

### SE-68-Q1 — Blockchain Distributed-Ledger and Smart-Contract Engineering
Me project ekata **Blockchain Distributed-Ledger and Smart-Contract Engineering** adala wenawada? Udaharana signals: multi-party shared state without one trusted operator, smart contracts, tokenized workflows.

- Tier: `specialized`
- Why: Determine when a distributed ledger is justified and engineer consensus, contracts, keys, finality, governance, privacy, upgrade, and off-chain integration correctly.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: DLT necessity analysis, trust model, permissioned versus permissionless design, consensus assumptions.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: DLT decision record, trust and threat model, contract specification.

### SE-69-Q1 — Quantum-Software Engineering
Me project ekata **Quantum-Software Engineering** adala wenawada? Udaharana signals: quantum algorithms, quantum SDKs, research prototypes.

- Tier: `specialized`
- Why: Engineer hybrid quantum-classical software with justified quantum suitability, resource estimates, noisy execution, probabilistic validation, portability, and classical baselines.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: quantum suitability analysis, classical baseline, quantum and classical partitioning, circuit design.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: quantum suitability assessment, classical baseline, circuit specification.

### SE-70-Q1 — Digital-Twin and Simulation Engineering
Me project ekata **Digital-Twin and Simulation Engineering** adala wenawada? Udaharana signals: industrial assets, buildings, logistics.

- Tier: `specialized`
- Why: Create trustworthy synchronized representations of physical assets or processes with calibrated models, uncertainty, lifecycle identity, and controlled decision or actuation boundaries.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: physical-twin identity, synchronization model, sensor-data quality, model calibration.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: twin scope and identity, synchronization contract, model validation plan.

### SE-71-Q1 — Autonomous and Robotic-System Assurance Engineering
Me project ekata **Autonomous and Robotic-System Assurance Engineering** adala wenawada? Udaharana signals: robots, drones, autonomous vehicles.

- Tier: `specialized`
- Why: Constrain and assure autonomous behavior under uncertain perception, changing environments, component faults, and human takeover requirements.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: operational design domain, environment assumptions, perception uncertainty, decision boundaries.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: ODD specification, autonomy hazard analysis, runtime monitor design.

### SE-72-Q1 — Geospatial and Location-Intelligence Engineering
Me project ekata **Geospatial and Location-Intelligence Engineering** adala wenawada? Udaharana signals: maps, routing, geofencing.

- Tier: `specialized`
- Why: Ensure coordinate, projection, geometry, accuracy, privacy, spatial indexing, and interoperable geospatial services are correct.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: coordinate reference systems, latitude and longitude correctness, projection transformations, spatial precision.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: CRS policy, spatial data model, accuracy requirements.

### SE-73-Q1 — Edge and Computing-Continuum Engineering
Me project ekata **Edge and Computing-Continuum Engineering** adala wenawada? Udaharana signals: low-latency local processing, IoT fleets, mobile edge.

- Tier: `specialized`
- Why: Place and move workloads across device, edge, and cloud while managing latency, mobility, disconnection, constrained resources, fleet security, and data consistency.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: edge placement decisions, cloud and edge partitioning, workload migration, device mobility.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: placement decision, edge topology, synchronization design.

### SE-74-Q1 — High-Performance and Accelerator-Computing Engineering
Me project ekata **High-Performance and Accelerator-Computing Engineering** adala wenawada? Udaharana signals: HPC clusters, GPU workloads, simulations.

- Tier: `specialized`
- Why: Engineer parallel software for distributed memory, shared memory, GPUs, or accelerators with scalable decomposition, reproducible numerics, profiling, and recovery.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: parallel decomposition, data partitioning, distributed versus shared memory, MPI communication.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: parallel architecture, scaling model, resource and topology assumptions.

### SE-75-Q1 — Real-Time Media and Quality-of-Experience Engineering
Me project ekata **Real-Time Media and Quality-of-Experience Engineering** adala wenawada? Udaharana signals: live streaming, conferencing, video-on-demand.

- Tier: `specialized`
- Why: Deliver audio and video with controlled startup, latency, buffering, synchronization, adaptation, accessibility, and perceived quality across networks and devices.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: media-session lifecycle, live versus on-demand, encoding profiles, adaptive bitrate.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: media profile, latency budget, adaptive-bitrate strategy.

### SE-76-Q1 — Operational-Technology and Industrial-Control Engineering
Me project ekata **Operational-Technology and Industrial-Control Engineering** adala wenawada? Udaharana signals: PLC SCADA or DCS, factories, utilities.

- Tier: `specialized`
- Why: Engineer software for physical industrial operations where safety, deterministic behavior, long asset life, legacy protocols, restricted change, and continuity dominate.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: physical-process awareness, deterministic timing, safety interlocks, network segmentation.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: OT system context, safety and control boundaries, network zoning.

### SE-77-Q1 — Spatial AR VR and Immersive-System Engineering
Me project ekata **Spatial AR VR and Immersive-System Engineering** adala wenawada? Udaharana signals: AR, VR, mixed reality.

- Tier: `specialized`
- Why: Build immersive systems that correctly manage coordinate spaces, tracking, latency, environment understanding, comfort, privacy, accessibility, and physical safety.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: coordinate spaces, head and hand tracking, motion-to-photon latency, spatial anchors.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: spatial interaction model, coordinate-space specification, comfort budget.

### SE-78-Q1 — Financial Messaging Payment and Ledger Engineering
Me project ekata **Financial Messaging Payment and Ledger Engineering** adala wenawada? Udaharana signals: payments, wallets, banking.

- Tier: `specialized`
- Why: Preserve monetary correctness through explicit payment states, decimal precision, idempotency, double-entry records, reconciliation, settlement, disputes, and provider failure handling.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: monetary data types, double-entry ledgers, idempotent payment initiation, authorization and capture.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: payment state model, ledger design, idempotency key policy.

### SE-79-Q1 — Search and Information-Retrieval Engineering
Me project ekata **Search and Information-Retrieval Engineering** adala wenawada? Udaharana signals: site search, document discovery, product search.

- Tier: `specialized`
- Why: Build search systems with controlled ingestion, indexing, query understanding, ranking, freshness, access filtering, relevance evaluation, and regression protection.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: document ingestion, tokenization, indexing, query parsing.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: search requirements, document and query schema, ranking strategy.

### SE-80-Q1 — Knowledge-Graph Ontology and Semantic-System Engineering
Me project ekata **Knowledge-Graph Ontology and Semantic-System Engineering** adala wenawada? Udaharana signals: complex relationship data, semantic integration, enterprise knowledge.

- Tier: `specialized`
- Why: Represent and reason over entities, relationships, vocabularies, provenance, and semantics with governed identity, ontology evolution, constraints, and interoperability.
- If unknown: `do_not_force; if signals_exist_flag_for_specialist_review_and_user_approval`
- Follow-ups:
  - Me area eken satisfy karanna ona requirement/outcome mokakda? Main focus: domain vocabulary, entity identity, IRIs, RDF graphs.
  - Me decision/control eka own karanne kawda?
  - Applicable standard, legal rule, supplier constraint, or project limitation tiyenawada?
  - Failure unoth impact eka monawada saha acceptable residual risk eka kochchara da?
  - Required evidence/artifacts walin monawada project ekata one? Suggested: semantic model, ontology, identity policy.
