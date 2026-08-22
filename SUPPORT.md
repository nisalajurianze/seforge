# Support

Use the most suitable GitHub channel:

- **Questions and setup help:** GitHub Discussions, when enabled.
- **Confirmed defects:** Bug report issue form.
- **Feature proposals:** Feature request issue form.
- **Security vulnerabilities:** Private security advisory, never a public issue.

Before reporting a defect, run:

```bash
python -S schemas/validate_pack.py
python -S sepack.py integrity
python -S sepack.py doctor --target .
```

Include the pack version, operating system, Python version, provider, exact command, sanitized output, and a minimal reproduction.
