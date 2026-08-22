# Installation, Upgrade, and Removal

## Requirements

- Python 3.11 or later
- A writable target project
- No third-party Python packages are required by the core runtime

## Install or upgrade

```bash
python -S scripts/install.py \
  --target /path/to/project \
  --providers all \
  --goal "The outcome the project should deliver"
```

Available provider values:

```text
agents
openai
github
claude
gemini
cursor
windsurf
all
```

Use comma-separated values for a subset.


### Provider skill catalogue size

The default is:

```bash
--skill-install-mode workflow
```

This installs the 12 workflow skills into provider discovery folders. The 80 engineering-area skills stay inside `.engineering/skill-pack/agent-skills/` and are loaded through bounded task-context bundles. This avoids provider metadata truncation when many skills are installed.

Use the full catalogue only deliberately:

```bash
--skill-install-mode all
```

### Safe-work delegation

```bash
--delegate-safe-work
```

This authorizes R1 local, reversible work. It does not authorize destructive, production, costly, sensitive, externally visible, or irreversible work.

### Claude hook

```bash
--enable-claude-hooks
```

The installer merges the supplied `PreToolUse` hook into `.claude/settings.json`. The hook:

- asks before R3 commands;
- denies R4 security-bypass commands;
- asks before modifying agent policy or the installed pack.

The hook is optional because hooks execute local code and should be enabled deliberately. Once enabled, it remains enabled across upgrades that still include the Claude provider. Disable it explicitly with:

```bash
--disable-claude-hooks
```

### Changing provider selection

Running the installer with a smaller provider set prunes unchanged files previously managed for providers that are no longer selected. User-modified files are preserved and listed in `prune_warnings` inside `.engineering/install-manifest.json`. Claude hook entries are removed without deleting unrelated user hooks or permissions.

### Skip repository quickstart

```bash
--skip-quickstart
```

Use this for packaging or CI installation. The AI can run quickstart later.

## What is managed

The installer writes `.engineering/install-manifest.json`.

It records:

- installed pack version;
- enabled providers;
- every managed path;
- whether a path was created;
- installed file digest;
- current upgrade backup path;
- the original pre-install baseline for reliable multi-upgrade restoration;
- the provider skill-install mode.

Existing root instruction files receive a clearly delimited managed block:

```text
<!-- SEPACK:BEGIN v2 -->
...
<!-- SEPACK:END -->
```

Project-owned content outside the block is preserved.

## Backups

Before replacing a managed file or pack tree, the installer writes a timestamped backup under:

```text
.engineering/backups/install-<UTC timestamp>/
```

## Upgrade

Run the same install command again. The process is idempotent:

- the managed block is replaced rather than duplicated;
- provider files are refreshed;
- the previous installed pack is backed up;
- project engineering state is migrated separately.

## Remove managed installation

```bash
python -S scripts/uninstall.py --target /path/to/project
```

By default this removes managed pack/provider files and managed instruction blocks while preserving `.engineering` project state.

Restore the baseline that existed before the first managed installation, even after multiple upgrades:

```bash
python -S scripts/uninstall.py \
  --target /path/to/project \
  --restore-backups
```

Remove all `.engineering` state only when intentionally discarding plans, evidence, tasks, risks, and decisions:

```bash
python -S scripts/uninstall.py \
  --target /path/to/project \
  --remove-state
```

## Verify installation

Inside the target project:

```bash
python -S .engineering/skill-pack/sepack.py integrity
python -S .engineering/skill-pack/sepack.py doctor --target .
python -S .engineering/skill-pack/sepack.py brief --target .
```

A structural doctor result is not a substitute for running the project's reviewed native checks. Project-defined commands require a persisted command-definition review and `--trust-project-scripts` on each invocation. They run without an OS-level filesystem or network sandbox, so use an external isolated runner for untrusted code.
