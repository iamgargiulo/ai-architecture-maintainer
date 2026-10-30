# Platform map

Use this as a decision aid, then verify current official documentation or the installed tool before adding configuration.

## Portable core

The portable unit is an Agent Skill folder containing `SKILL.md` with `name` and `description`, plus optional `scripts/`, `references/`, and `assets/`. Keep the core skill within the open Agent Skills subset. Avoid host-specific frontmatter in the canonical file unless portability has been tested.

## Claude Code

- Root and nested project guidance commonly lives in `CLAUDE.md`.
- Project skills live under `.claude/skills/<name>/SKILL.md`; plugins can expose `skills/<name>/SKILL.md`.
- Procedures belong in skills; always-on invariants belong in `CLAUDE.md` or scoped rules.
- Agents, hooks, settings, and permissions are Claude-specific mechanisms. Do not create them unless the use case justifies deterministic or isolated behavior.

## Codex

- Root and nested project guidance lives in `AGENTS.md`.
- Repository skills are discovered under `.agents/skills` from the working directory toward the repository root.
- `agents/openai.yaml` is optional UI and dependency metadata; it is not the canonical workflow body.
- Prefer standard skill content so the same folder remains usable by other Agent Skills hosts.

## Cursor

- Durable project constraints belong in Cursor project rules, normally under `.cursor/rules/`, using the repository's existing scoping pattern.
- Agent Skills support should use Cursor's current advertised skills location or a compatible installer. Detect existing paths before writing.
- Do not convert every Cursor rule into a skill: constraints and procedures remain different information types.

## Multi-host repositories

- Treat each host's always-on file as an adapter, not a full duplicate knowledge base.
- Put detailed procedures in portable skills and detailed explanations in normal docs.
- Keep shared semantic rules aligned, but preserve necessary host-specific syntax and capabilities.
- Record intentional differences. Unexplained drift is an audit finding.
- Prefer an installer or explicit copy step over committing several uncontrolled copies of the same skill.
