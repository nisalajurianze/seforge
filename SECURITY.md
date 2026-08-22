# Security Policy

## Supported release

Security fixes are applied to the latest release line. Older versions may not receive patches.

## Reporting a vulnerability

Please do **not** open a public issue for a vulnerability that could expose credentials, private data, unsafe command execution, authorization bypass, evidence tampering, prompt injection, provider-hook abuse, or supply-chain compromise.

Use the repository's **Security → Report a vulnerability** private advisory flow. Include:

- affected version and files;
- reproduction steps or a minimal proof of concept;
- expected and actual behavior;
- impact and realistic attack conditions;
- suggested mitigation, when available.

Do not include live secrets, personal information, or destructive payloads.

## Security boundary

The pack classifies and gates project-defined commands, sanitizes the environment, redacts common secret patterns, and records tamper-evident evidence. It does **not** provide a complete operating-system sandbox or guaranteed network-egress isolation. Run untrusted project code in a restricted container, virtual machine, or isolated CI runner.

See `docs/security/AGENT-SECURITY.md`, `docs/security/MCP-POLICY.md`, and `RE-AUDIT-REPORT.md`.
