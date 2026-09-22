# AI Architecture Maintainer

A portable Agent Skill for auditing and maintaining the persistent AI architecture of a software repository.

It decides whether durable knowledge belongs in always-on instructions, scoped rules, skills, agents, deterministic enforcement, normal documentation, protected design artifacts, local preferences, or nowhere. The objective is not to document everything an agent learns; it is to preserve only information that materially improves future decisions.

## What it audits

- `CLAUDE.md`, `AGENTS.md`, and Cursor project rules
- nested and path-scoped instructions
- Agent Skills and supporting references/scripts
- agents, hooks, settings, permissions, and CI enforcement
- stale, duplicated, contradictory, or oversized persistent context
- session learnings and user corrections that may deserve persistence
- design/product sources of truth such as `DESIGN.md` and `PRODUCT.md`

The default mode is read-only. It reports proposed changes, rejected candidates, ambiguities, protected artifacts, and a diff. It edits only when explicitly asked to apply changes.

## Design persistence

The skill interoperates with external design skills rather than bundling them:

- [UI Craft](https://github.com/educlopez/ui-craft)
- [Impeccable](https://github.com/pbakaus/impeccable)
- [Taste Skill](https://github.com/Leonxlnx/taste-skill)

When one of these—or a semantically equivalent design skill—is installed, the audit treats `DESIGN.md` as a required persistent authoring source unless the project explicitly declares a different canonical path. It also preserves `PRODUCT.md` and surface briefs when an installed workflow consumes them.

This is deliberate: design intent is an input to future generation and evaluation, not disposable documentation merely because current code reflects it.

## Install

Use the Agent Skills installer and select Claude Code, Codex, Cursor, or any combination offered by the installer:

```bash
npx skills@latest add iamgargiulo/ai-architecture-maintainer
```

Or install the skill folder manually:

| Host | Project location |
|---|---|
| Claude Code | `.claude/skills/maintain-ai-architecture/` |
| Codex | `.agents/skills/maintain-ai-architecture/` |
| Cursor | Use Cursor's current Agent Skills location or the installer above |

The canonical portable skill is in [`skills/maintain-ai-architecture`](skills/maintain-ai-architecture).

## Use

Explicit invocation depends on the host. Typical requests include:

```text
Audit this repository's persistent AI architecture. Do not edit files.
```

```text
Review what we learned in this session and propose only the durable,
non-obvious guidance worth persisting. Show the diff but do not apply it.
```

```text
Apply the approved AI-architecture changes and verify that DESIGN.md,
PRODUCT.md, and installed design-skill contracts remain intact.
```

## Read-only inventory

The bundled scanner inventories supported agent configuration and protected artifacts without modifying the repository:

```bash
python3 skills/maintain-ai-architecture/scripts/audit_ai_architecture.py \
  --root /path/to/repository \
  --format markdown
```

JSON output is also available with `--format json`.

## Maintenance model

Each candidate instruction is scored across durability, reuse, non-obviousness, impact, and verification. Normal candidates should score at least 8/10 and also be non-duplicative. Safety, data-integrity, and protected-authoring constraints receive separate consideration.

The skill prefers updating, consolidating, moving, or removing existing guidance before adding new persistent context.

## Development

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```

Validate the skill with the validator provided by your Agent Skills host before publishing changes.

## License

MIT
