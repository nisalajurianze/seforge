# Deep Research and Gap Analysis — v1.3 to v2.0

## Scope

This review examined the complete v1.3 repository, including:

- 80 detailed engineering-area files;
- root and provider instruction files;
- installer and CLI behavior;
- routing, onboarding, plan, evidence, and release logic;
- schemas and validation;
- zero-friction user experience;
- current official guidance for AGENTS.md, Agent Skills, execution plans, provider customization, agent security, MCP authorization, evaluation, provenance, and artifact verification.

## Executive finding

v1.3 had strong breadth and user-intent handling, but it remained primarily a large documentation corpus wrapped by a structural CLI. Its main professional risks were:

- excessive static instruction volume;
- generic repeated skill text;
- no standard Agent Skills packaging;
- structural checks being stronger than real project verification;
- weak command trust, evidence integrity, and agent-security controls;
- no deterministic behavioral eval suite;
- limited upgrade, rollback, and provider-native orchestration.

v2.0 addresses these through progressive disclosure, modular Agent Skills, task-bounded context, project-native command discovery, tamper-evident evidence, action-risk policy, prompt-injection boundaries, provider-native agents, execution plans, deterministic tests, integrity verification, and state migration.

## Research basis

### Agent instruction and skill standards

- OpenAI Codex `AGENTS.md`: https://developers.openai.com/codex/agent-configuration/agents-md
- OpenAI Codex Agent Skills: https://developers.openai.com/codex/build-skills
- OpenAI Agent Skills API guidance: https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI ExecPlans and `PLANS.md`: https://developers.openai.com/cookbook/articles/codex_exec_plans
- OpenAI long-horizon task guidance: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex
- GitHub Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- GitHub repository and path-specific instructions: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- GitHub custom agents: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents
- Claude Code skills: https://docs.anthropic.com/en/docs/claude-code/skills
- Claude Code subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code permissions and hooks: https://docs.anthropic.com/en/docs/claude-code/permissions and https://docs.anthropic.com/en/docs/claude-code/hooks

### Agent security and external tools

- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Securing Agentic Applications Guide: https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/
- OWASP Agentic Skills Top 10: https://owasp.org/www-project-agentic-skills-top-10/
- NIST agent hijacking evaluation: https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations
- NIST AI agent security research: https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition
- MCP 2026 specification and security practices: https://modelcontextprotocol.io/specification/2026-07-28 and https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
- MCP authorization security considerations: https://modelcontextprotocol.io/specification/draft/basic/authorization/security-considerations

### Evaluation and software supply-chain integrity

- OpenAI Evals guidance: https://developers.openai.com/api/docs/guides/evals
- OpenAI testing Agent Skills: https://developers.openai.com/blog/eval-skills
- SLSA v1.2 provenance and verification: https://slsa.dev/spec/v1.2/
- Sigstore verification: https://docs.sigstore.dev/cosign/verifying/verify/

## Detailed findings and v2.0 responses

| # | v1.3 finding | Risk | v2.0 response |
|---:|---|---|---|
| 1 | Root instructions were nearly 1,000 words and repeated collaboration rules. | Important instructions compete for context and can conflict. | Replaced with a concise root `AGENTS.md` that routes to high-signal files and skills. |
| 2 | All 80 skills were stored as long Markdown documents, not standard Agent Skills. | Agents cannot reliably discover or progressively load the right guidance. | Packaged every area as a standard directory with YAML-front-matter `SKILL.md`, references, and assets. |
| 3 | The 80 detailed files contained extensive repeated boilerplate; 81 long lines appeared in at least 20 files and major blocks appeared in all 80. | High token cost without proportional task value. | Kept full guides as deep references and created concise task-invoked skill files. |
| 4 | Task startup instructed the agent to read every active skill. | Broad projects could load many unrelated skills. | Added task-level skill selection and bounded context bundles. |
| 5 | The router relied heavily on keyword and file-presence heuristics. | False activation and false confidence. | Added confidence, evidence source, decision ownership, and explicit unresolved status. |
| 6 | Foundational onboarding could be marked complete while important answers remained unknown. | Unknown high-impact facts could look resolved. | Separates observed, user-provided, inferred, defaulted, delegated, and unresolved facts with review triggers. |
| 7 | Structural `audit` and `validate` commands could be mistaken for project verification. | False production-readiness claims. | Added project-native command discovery and real execution evidence; structural checks are explicitly labeled. |
| 8 | Project scripts could be run without a strong trust model. | A malicious repository can execute arbitrary code. | Added command classification, script provenance, review requirement, approval boundaries, timeout, and sandbox guidance. |
| 9 | Evidence records were append-only JSON but lacked integrity chaining. | Evidence can be silently edited. | Added SHA-256 evidence files and a hash-chained evidence ledger. |
| 10 | No explicit indirect prompt-injection model existed in the runtime. | Repository or tool content can hijack the agent. | Added trusted control plane vs untrusted data plane, injection handling, and policy checks. |
| 11 | MCP and external tools had no dedicated authorization policy. | Token passthrough, excessive scopes, tool poisoning, and data exfiltration. | Added MCP policy for origin, scope, audience validation, consent, logging, and least privilege. |
| 12 | No third-party skill trust or provenance process. | Malicious skills can run code or exfiltrate data. | Added skill origin, digest, permissions, script review, and version-pinning rules. |
| 13 | Long-horizon plans were project documents but not aligned to a self-contained ExecPlan format. | Agents can lose context or drift across sessions. | Added `PLANS.md`, milestone validation, discovery and decision logs, and current progress. |
| 14 | No deterministic eval corpus for user burden, routing, safety, or instruction behavior. | Regressions in the agent operating model go undetected. | Added unit tests, static policy evals, scenario cases, and CI execution. |
| 15 | Provider support was mostly pointer files. | It did not exploit native skills, path instructions, custom agents, hooks, or subagents. | Added OpenAI/Codex skills, GitHub skills and custom agents, Claude skills/subagents, Gemini instructions, Cursor rules, and safe hook templates. |
| 16 | Provider instruction files could diverge. | Conflicting behavior across tools. | Uses one concise canonical policy and generated adapters with integrity checks. |
| 17 | Installer replacement behavior did not provide a full managed-block backup and restore model. | Existing user instructions can be overwritten or hard to restore. | Added managed blocks, timestamped backups, idempotent install, upgrade, and uninstall manifests. |
| 18 | State writes were not uniformly atomic or locked. | Interrupted writes or concurrent agents can corrupt state. | Added atomic file replacement and project-state lock support. |
| 19 | No state schema migration strategy. | Upgrades can break existing projects. | Added schema versioning and migration records. |
| 20 | No pack-integrity verification. | A modified or incomplete pack can silently run. | Added a complete file hash manifest and integrity command. |
| 21 | No explicit worktree or branch isolation guidance. | Concurrent agents can overwrite changes or contaminate the main tree. | Added isolated worktree policy for parallel, untrusted, and high-risk tasks. |
| 22 | Feature packets initially inherited all active skill IDs. | Task scope becomes noisy and gates become impractical. | Added affected-skill selection based on changed files, decision ownership, and task risk. |
| 23 | User approval was modeled mainly at plan level. | Either excessive blocking or unsafe broad delegation. | Added action-level risk classes R0–R4 and targeted approval. |
| 24 | “Best option” delegation could approve a broad plan while data sensitivity remained unknown. | User convenience could hide high-impact uncertainty. | Delegation is limited to low-risk reversible choices; material unknowns remain explicit. |
| 25 | No command registry tied to actual manifests. | Agents guess commands or skip important checks. | Added discovery for Node, Python, Java, Gradle, .NET, Go, Rust, PHP, Ruby, Make, Docker, and common CI. |
| 26 | No evidence freshness or expiry. | Old test or approval evidence may be reused after change. | Evidence records include commit, file scope, environment, skill/task, and invalidation triggers. |
| 27 | No task-context word budget. | Prompt bloat and lower instruction reliability. | Added 4k/8k/16k task bundles and deep-reference-on-demand rules. |
| 28 | No agent-role separation. | One agent can plan, implement, review, and approve its own work. | Added planner, architect, implementer, test reviewer, security reviewer, and release reviewer roles with independence guidance. |
| 29 | No local-only privacy statement for operational state. | Project context may be sent to unnecessary services. | Added local-first state and external-tool disclosure rules. |
| 30 | No portable export of a task's decisions and evidence. | Handover and independent review are difficult. | Added a self-contained review bundle and evidence index format. |

## Architectural decision

The pack now distinguishes:

1. **Root instructions** — short, always loaded.
2. **Workflow skills** — loaded for the type of work.
3. **Engineering-area skills** — loaded only for relevant decisions.
4. **Detailed references** — loaded on demand.
5. **Deterministic runtime** — discovery, state, command policy, verification, evidence, gates, and integrity.
6. **Provider adapters** — generated from one canonical policy.
7. **Evals and tests** — prevent regressions in both code and agent behavior.

## Definition of improvement

v2.0 is considered stronger than v1.3 only if it can demonstrate:

- lower default instruction volume;
- correct standard skill packaging;
- task-specific context generation;
- safe command classification;
- real verification evidence;
- integrity verification;
- deterministic test coverage;
- user-interruption limits;
- high-risk approval enforcement;
- install, upgrade, and uninstall reversibility.
