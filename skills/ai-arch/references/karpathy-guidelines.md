# Karpathy coding baseline

Adapted from the MIT-licensed [Karpathy Guidelines skill](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md). This bundled adaptation is the run-time source; the upstream link is attribution, not a dependency.

## Guidance to persist

Merge the following four principles into the project's always-on instructions, preserving equivalent existing wording. Use the project's language and style. Scale the process to the task; a trivial change needs proportionate checks.

```markdown
## Coding principles

- **Reason before editing.** Make assumptions and tradeoffs visible. When competing interpretations would change the outcome, explain the ambiguity and ask for clarification. Suggest a simpler approach when appropriate; pause if a material uncertainty prevents correct work.
- **Choose the simplest adequate solution.** Implement the requested behavior with minimal complexity. Avoid speculative features, abstractions used only once, unrequested configuration, and handling of impossible cases. Simplify code that has grown unnecessarily elaborate.
- **Keep edits focused.** Follow existing conventions and preserve unrelated code, comments, and formatting. Remove imports, variables, or functions made unused by your changes. Mention pre-existing dead code without deleting it unless requested. Every changed line should serve the task.
- **Verify the outcome.** Define observable success criteria and, for multiple steps, pair each step with a check. Reproduce bugs with a failing test, test invalid inputs when adding validation, and check tests before and after refactoring. Continue until the relevant checks pass; report blockers honestly.
```

## Coverage and placement

1. Compare meaning, not headings or exact phrases. Check each principle independently; when coverage is partial, add only the missing obligations. Keep unrelated project instructions intact.
2. Inspect instructions actually loaded by each active host: `AGENTS.md` for Codex, `CLAUDE.md` for Claude Code, and an always-applied Cursor project rule. Follow the routing matrix and existing shared-source conventions. A name or URL without the guidance, or an optional installed skill alone, is not always-on coverage.
3. Prefer an existing appropriate instruction file. If none exists, use the current host as evidence for the destination and create only that host's instructions in Apply mode. If no active host can be established, report the placement ambiguity instead of creating several host configurations.
4. When multiple hosts use a shared instruction source, maintain the baseline there and verify each adapter loads it. When they have independent instructions, merge only the missing coverage into each active host's file. A second run must produce no further baseline edits.
5. Honor explicit project or user overrides and report the affected principle as `overridden`, with the authoritative instruction. An audit request remains read-only even when principles are missing.
