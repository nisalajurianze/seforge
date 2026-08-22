# Publishing to GitHub

This folder is ready to become a GitHub repository.

## 1. Create an empty GitHub repository

Recommended repository name:

```text
universal-software-engineering-skill-pack
```

Do not initialize the remote repository with a README, license, or `.gitignore`, because those files already exist here.

## 2. Push the repository

```bash
git init
git add .
git commit -m "release: SEForge v2.0.1"
git branch -M main
git remote add origin https://github.com/<owner>/universal-software-engineering-skill-pack.git
git push -u origin main
```

## 3. Configure the repository

Recommended GitHub settings:

- enable Issues and Discussions;
- enable private vulnerability reporting;
- protect `main`;
- require the `Quality Gate` workflow before merge;
- require pull-request review;
- prevent force pushes and branch deletion;
- enable Dependabot alerts;
- upload `docs/assets/social-preview.png` under **Settings → General → Social preview**.

## 4. Create the first release

```bash
git tag -a v2.0.1 -m "SEForge v2.0.1"
git push origin v2.0.1
```

The release workflow builds a source archive, creates a SHA-256 checksum, and uploads both files to the GitHub release.

## Suggested repository topics

```text
ai-agents, agent-skills, software-engineering, devsecops, sre, quality-engineering, prompt-injection, mcp, github-copilot, claude-code, codex
```
