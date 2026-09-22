---
name: maintain-ai-architecture
description: Audit, design, and maintain a repository's persistent AI-agent architecture across Claude Code, Codex, Cursor, and Agent Skills. Use when reviewing or changing CLAUDE.md, AGENTS.md, .cursor/rules, nested instructions, skills, subagents, hooks, permissions, AI-facing documentation, or when deciding where durable session learnings belong. Preserve design-system sources of truth such as DESIGN.md and PRODUCT.md, especially when ui-craft, impeccable, taste, or similar design skills are installed. Do not use for ordinary feature work unless the user asks to persist new agent guidance or audit the repository's AI configuration.
---

# Maintain AI Architecture

Maintain the smallest, highest-signal set of persistent instructions that materially improves future agent behavior. Treat persistent context as production infrastructure, not a session log.

## Operating modes

Infer the mode from the request:

- **Audit**: inspect and report only. This is the default.
- **Propose**: show exact proposed changes and a diff; do not write.
- **Apply**: make the approved or explicitly requested changes, then verify them.

Do not turn an audit or review request into edits. Do not apply hooks, permissions, CI changes, or other enforcement unless the user explicitly requests implementation.

## Workflow

### 1. Establish scope and repository truth

1. Resolve the repository root and inspect working-tree status. Preserve unrelated changes.
2. Run the read-only inventory script:

   ```bash
   python3 <skill-dir>/scripts/audit_ai_architecture.py --root <repo-root> --format markdown
   ```

3. Read completely:
   - root `CLAUDE.md`, `AGENTS.md`, and applicable Cursor project rules;
   - relevant nested instruction files and scoped rules;
   - metadata and bodies of skills relevant to the audit;
   - settings, hooks, agents, and referenced docs needed to validate claims;
   - the current session's corrections, dead ends, and durable discoveries.
4. Verify commands, paths, architectural claims, generated files, and completion requirements against the repository. Never promote an assumption into persistent truth.

Read [references/platform-map.md](references/platform-map.md) when more than one agent host is present or when adding/moving configuration between hosts.

### 2. Protect authoring sources of truth

Before pruning documentation, inspect the inventory's **Design persistence** section and read [references/design-persistence.md](references/design-persistence.md).

Treat existing `DESIGN.md`, `PRODUCT.md`, brand guidance, design tokens, surface briefs, and other declared design inputs as authoring sources of truth. Their contents may intentionally overlap code. Do not classify them as redundant merely because the implementation reflects them.

When `ui-craft`, `impeccable`, `taste`, `stitch-design-taste`, or a semantically equivalent design skill is present:

- require a repository-level `DESIGN.md` unless the repository explicitly declares a different canonical path;
- preserve `PRODUCT.md` when Impeccable or another installed skill consumes it;
- read the installed design skill before editing its owned artifacts;
- do not edit managed third-party skill files; change local adapters or project artifacts instead;
- report a missing required artifact as a gap, not as permission to invent its contents.

### 3. Classify every candidate

Assign each candidate to exactly one destination. Use [references/routing-matrix.md](references/routing-matrix.md) for host-specific placement.

1. Global always-on project instruction
2. Directory- or path-scoped instruction
3. Reusable procedure
4. Specialized isolated work
5. Deterministic enforcement
6. Access or safety boundary
7. Detailed or occasional documentation
8. Design/product source of truth
9. Personal preference
10. Temporary or cheaply discoverable information

The destination may be a root instruction file, nested instruction/rule, skill, agent, hook/CI check, permissions/settings, documentation, protected design artifact, local user configuration, or nowhere.

Do not force host-specific mechanisms into a repository that does not use that host. When multiple hosts coexist, preserve one semantic rule and keep adapters minimal; do not create divergent copies silently.

### 4. Apply the persistence test

Persist a normal candidate only when all are true:

- **Durable**: likely valid across many future sessions.
- **Reusable**: relevant to multiple future tasks.
- **Non-obvious**: not reliably and cheaply inferable from the repository.
- **Behavior-changing**: changes what a capable agent should do.
- **High-impact**: omission risks errors, violations, repeated corrections, or substantial wasted work.
- **Verified**: supported by current evidence or explicit project requirements.
- **Non-duplicative**: not already expressed sufficiently at the right scope.

Use this 0-2 heuristic: durability, reuse, non-obviousness, impact, verification. Normally require at least 8/10. Critical safety, data-integrity, or protected-authoring constraints may qualify despite lower frequency.

Prefer the generalized rule behind a repeated mistake, not the story of the mistake.

### 5. Audit existing architecture, not only additions

Evaluate every relevant existing instruction for truth, durability, scope, actionability, duplication, contradiction, discoverability, and token cost.

Prioritize, in order:

1. update or clarify an existing rule;
2. consolidate overlaps;
3. replace obsolete guidance;
4. move guidance to the correct scope or mechanism;
5. remove low-value material;
6. add a new instruction only when necessary.

Keep root always-on files intentionally small. Treat 200 lines as an audit warning, not an automatic deletion threshold. Remove low-value content before compressing useful content.

Never persist secrets, credentials, tokens, session IDs, volatile URLs, or environment values. Reference environment-variable names only when necessary.

### 6. Resolve conflicts conservatively

When instructions conflict with code, tests, schemas, configuration, installed skill contracts, or explicit user direction:

1. identify the authoritative source;
2. verify current behavior;
3. preserve protected design/product intent unless the user changes it;
4. report unresolved ambiguity instead of guessing.

Do not let a generic cleanup rule override a specialized installed skill's explicit artifact contract.

### 7. Produce the maintenance report

Use these sections:

#### Proposed changes

For each change include target file, action (`ADD`, `UPDATE`, `MOVE`, `CONSOLIDATE`, `REMOVE`, or `ENFORCE`), exact concept, persistence score, and one-sentence behavioral justification.

#### Protected artifacts

List design/product sources of truth, their owning or consuming skills, and whether each is present, missing, or ambiguous.

#### Rejected candidates

List notable session learnings intentionally not persisted and why: task-specific, temporary, discoverable, duplicated, personal, or insufficiently verified.

#### Ambiguities

List contradictions and missing evidence. Do not resolve them by assumption.

#### Diff

In Audit or Propose mode, show the proposed diff and stop. In Apply mode, apply only the smallest justified change.

### 8. Verify applied changes

After edits:

1. rerun the inventory script;
2. validate modified skill folders with the host's validator when available;
3. run only relevant repository checks;
4. confirm protected artifacts remain present and referenced correctly;
5. inspect the final diff for unrelated changes, duplicated rules, secrets, and stale adapters;
6. report what changed, why it deserves persistence, what was consolidated or removed, and any remaining ambiguity.

## Final decision filter

Before keeping any persistent line, ask:

> If this line disappeared, would a capable future agent be meaningfully more likely to make a wrong decision?

If not, remove it. For protected design/product artifacts, apply a different question:

> Is this file an intentional authoring input or cross-session source of truth for humans or installed skills?

If yes, preserve it even when its contents are reflected elsewhere.
