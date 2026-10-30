# Routing matrix

Use this reference when deciding where durable knowledge belongs. Prefer the host's existing conventions over creating new parallel structures.

| Information type | Generic destination | Claude Code | Codex | Cursor |
|---|---|---|---|---|
| Repository-wide invariant | Root always-on instructions | `CLAUDE.md` | `AGENTS.md` | Project rule that always applies |
| Directory-specific invariant | Nearest scoped instruction | Nested `CLAUDE.md` or scoped rule | Nested `AGENTS.md` | `.cursor/rules/*.mdc` with path scope |
| Reusable procedure | Agent Skill | `.claude/skills/<name>/SKILL.md` or plugin skill | `.agents/skills/<name>/SKILL.md` | Existing Cursor Agent Skills location |
| Specialized isolated investigation | Agent/subagent only when context isolation helps | `.claude/agents/` | Codex subagent configuration when supported | Cursor agent/subagent mechanism when supported |
| Deterministic repository behavior | Executable enforcement | Hook, script, or CI | Script, rule, or CI | Hook, script, or CI |
| Access boundary | Permissions/sandbox/policy | Claude settings/permissions | Codex policy/config | Cursor settings/policy |
| Detailed occasional knowledge | Normal docs | `docs/` referenced when needed | `docs/` referenced when needed | `docs/` referenced when needed |
| Design/product intent | Protected source-of-truth artifact | `DESIGN.md`, `PRODUCT.md`, brand docs | Same | Same |
| Personal preference | User/local config | User settings or local files | User config | User settings |
| Task state or cheap discovery | Nowhere persistent | Issue/plan/code inspection | Issue/plan/code inspection | Issue/plan/code inspection |

## Cross-host rules

- Use standard `name` and `description` frontmatter for portable skills. Put host-only frontmatter behind a host-specific adapter only when required.
- Never assume that one host reads another host's root instruction file.
- Do not copy a long canonical procedure into three always-on files. Keep the procedure in a skill and add only the minimum invocation/constraint guidance each host needs.
- Do not use symlinks unless every target environment and installer is known to preserve and follow them.
- When a repository already contains equivalent host-specific files, update them as a coordinated set or explicitly document why one differs.
- Verify current host documentation before adding a new path. Existing repository paths are evidence; remembered paths are not.

## Placement tests

- If the content says **what must remain true**, it is probably an instruction or rule.
- If it says **how to perform a multi-step task**, it is probably a skill.
- If a machine can reliably reject violations, prefer deterministic enforcement over repeated prose.
- If it is read only for rare investigations, keep it in docs or a reference loaded on demand.
- If it defines product or visual intent, keep it as a protected authoring artifact even when code mirrors it.
