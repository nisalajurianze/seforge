# Research and Synthesis Method

## Inputs

- the user's uploaded Software Engineering lectures and Sommerville reference;
- the previously developed 80-area engineering taxonomy;
- official standards and provider documentation;
- current agent-security, MCP, evaluation, provenance, and supply-chain guidance;
- executable tests and behavioral evals.

## v2.0 method

1. Audit the previous pack's files, line duplication, instruction size, and runtime behavior.
2. Distinguish always-loaded policy from workflow skills, engineering skills, and deep references.
3. Convert each engineering area to a standard Agent Skill.
4. Add task-level routing and context budgets.
5. Replace structural completion claims with command execution and evidence records.
6. Add action-risk, prompt-injection, skill, MCP, and tool security.
7. Add state locking, atomic writes, migration, backups, uninstall, and integrity verification.
8. Test deterministic behavior and run scenario evals.
9. Package only one canonical copy of the skill corpus.
10. State limitations honestly.

## Evidence standard

A claim in the pack is classified as:

- source-derived;
- verified project fact;
- inference with confidence;
- pack default;
- user decision;
- execution evidence;
- unresolved.

No inference or default is silently promoted to verified fact.

## Maintenance

Before a new release:

- revalidate provider formats and current standards;
- run the validator, unit tests, evals, pack integrity, and end-to-end installation;
- review failed or changed evals;
- regenerate `PACK-INTEGRITY.json`;
- update the changelog and source map;
- test upgrade and uninstall against the previous supported state version.
