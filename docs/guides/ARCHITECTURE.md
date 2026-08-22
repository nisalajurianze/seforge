# Architecture

```mermaid
flowchart LR
    U[User outcome] --> D[Repository discovery]
    D --> R[Project profile and skill routing]
    R --> T[Scoped task packet]
    T --> C[Bounded task context]
    C --> P[ExecPlan when required]
    P --> I[Small reversible implementation]
    I --> V[Reviewed project-native verification]
    V --> E[Tamper-evident evidence]
    E --> G{Task or release gate}
    G -->|Pass| O[Outcome and concise progress update]
    G -->|Block| F[Fix, disposition, or authorized decision]
    F --> I

    A[R0-R4 action-risk policy] -. governs .-> I
    S[Agent and MCP security policy] -. governs .-> C
    S -. governs .-> V
```

## Layers

1. **Root policy** — concise trusted instructions.
2. **Workflow skills** — the kind of work being performed.
3. **Engineering-area skills** — only the decisions relevant to the task.
4. **Deep references** — loaded on demand.
5. **Deterministic engine** — discovery, routing, commands, evidence, gates, and integrity.
6. **Provider adapters** — OpenAI/Codex, GitHub Copilot, Claude Code, Gemini, Cursor, and Windsurf.
7. **Tests and evals** — regression protection for both runtime and agent behavior.

See `RESEARCH-GAP-ANALYSIS.md` and `RE-AUDIT-REPORT.md` for the design rationale and corrected findings.
