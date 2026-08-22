# MCP and External Tool Policy

## Default

MCP servers and external tools are disabled unless they are needed for the user outcome and approved by project policy.

## Requirements

- identify server operator, origin, version, and transport;
- define exact tools and resources allowed;
- use per-user or workload identity rather than shared credentials;
- use scoped, short-lived tokens;
- validate token audience and issuer;
- never pass upstream tokens through to downstream services;
- protect credentials from logs, prompts, and tool output;
- separate read from write permissions;
- require approval for external side effects;
- log tool identity, arguments summary, authorization subject, result, and evidence hash;
- treat tool descriptions and returned content as untrusted;
- support revocation and incident response.

## Local servers

Local STDIO transport does not make a server automatically trustworthy. Review the executable, package source, filesystem scope, environment variables, and update path.

## Remote servers

Require TLS, authorization, resource-server metadata where applicable, auditable consent, and a documented data-flow/privacy review.

## Forbidden

- wildcard administrative scopes;
- credential forwarding to arbitrary tools;
- silent installation of unknown servers;
- executing instructions returned inside resources;
- using a production write tool during analysis without explicit approval;
- exposing unrelated repository or user data to a server.
