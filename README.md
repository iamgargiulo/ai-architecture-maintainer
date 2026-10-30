<div align="center">

# AI Arch

### Give every instruction a purpose. Give every decision a home.

**One skill for maintaining the context your coding agents carry forward.**

[Quick start](#quick-start) · [How it works](#how-it-works) · [Karpathy baseline](#karpathy-baseline) · [Design persistence](#design-persistence) · [Inside the repo](#inside-the-repo)

`Claude Code` · `Codex` · `Cursor` · `MIT`

</div>

---

Your repository evolves. Its agent instructions should evolve with it.

**`/ai-arch`** reviews persistent instructions, checks the Karpathy coding baseline, finds stale or conflicting guidance, and proposes the smallest useful change. It covers root instructions, scoped rules, skills, agents, hooks, permissions, and the design context that needs to survive the next session.

**Audit by default. Apply when requested. Preserve authored design intent.**

## Quick start

Install with the [Agent Skills CLI](https://github.com/vercel-labs/skills), selecting your coding agent when prompted:

```bash
npx skills@latest add iamgargiulo/ai-architecture-maintainer
```

In Claude Code or Cursor, invoke:

```text
/ai-arch
```

In Codex CLI or the IDE extension, invoke:

```text
$ai-arch
```

The workflow is shared; invocation syntax belongs to the host. See the official [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/docs/skills), and [Codex](https://learn.chatgpt.com/docs/build-skills) documentation.

<details>
<summary><strong>Manual installation and upgrades</strong></summary>

Copy the complete `skills/ai-arch/` folder into the location for your host:

| Host | Project installation |
|---|---|
| Claude Code | `.claude/skills/ai-arch/` |
| Codex | `.agents/skills/ai-arch/` |
| Cursor | `.cursor/skills/ai-arch/` |

Keep `SKILL.md`, `references/`, `scripts/`, and `agents/` together. Python 3.10+ is needed only for the optional inventory scanner.

**Upgrading from `ai-arch-maintainer` or `maintain-ai-architecture`?** Install `ai-arch`, then remove the previous installed folder after preserving any local customizations. Update saved invocations to `/ai-arch` or `$ai-arch` and keep only one active copy per host. The repository name remains `ai-architecture-maintainer`.

</details>

## Three ways to use it

| Mode | Request | Result |
|---|---|---|
| **Audit** | `/ai-arch` | Inspect the architecture and report findings. No edits. |
| **Propose** | `/ai-arch propose` | Show justified changes and an exact diff. No edits. |
| **Apply** | `/ai-arch apply` | Apply verified, minimal improvements and check the result. |

These are instructions interpreted by the skill, not flags for the Python scanner. In Codex, use `$ai-arch` with the same request text. Changes to permissions, hooks, or CI require an explicit request for those changes.

For a session wrap-up:

```text
/ai-arch propose
Review this session's corrections and discoveries. Keep only durable,
verified guidance that changes future decisions. Preserve DESIGN.md
and the artifact contracts of installed design skills.
```

## How it works

### 01 — Discover

Read existing guidance, inspect relevant code, and identify which hosts and design workflows the project actually uses.

### 02 — Decide

Evaluate durability, reuse, non-obviousness, impact, and verification. The normal persistence threshold is **8/10**—a review heuristic, not a performance benchmark. Verification and non-duplication still matter independently of the score.

### 03 — Route

| What you learned | Where it belongs |
|---|---|
| A repository-wide invariant | Root agent instructions |
| A subsystem constraint | Nested instructions or scoped rules |
| A reusable procedure | A skill |
| An isolated investigation workflow | An agent, when justified |
| A mechanically checkable requirement | A hook, script, or CI check |
| An access restriction | Host permissions or policy |
| Detailed technical knowledge | Documentation loaded when needed |
| Authored design or product intent | `DESIGN.md`, `PRODUCT.md`, or the declared canonical source |
| A personal preference | User-local configuration |
| Temporary status or cheap discovery | No new persistent instruction |

### 04 — Refine

Update, consolidate, relocate, or remove existing guidance before adding more. Keep an explicit record of candidates rejected from persistence and ambiguities that need evidence.

## Karpathy baseline

Every run checks whether the project's always-on instructions cover the four principles from [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills):

- Make assumptions and tradeoffs visible before editing.
- Choose the simplest solution that satisfies the request.
- Keep changes focused and preserve unrelated work.
- Define success criteria and verify the outcome.

The [bundled reference](skills/ai-arch/references/karpathy-guidelines.md) supplies the guidance without requiring a separate plugin or network access. The baseline is required even in a new project with no session learnings; the normal persistence score applies to other candidate instructions.

In **Audit** and **Propose**, missing guidance appears as an exact diff. In **Apply**, the skill merges missing guidance into `AGENTS.md`, `CLAUDE.md`, or an always-applied Cursor rule for the hosts actually used by the project. Equivalent existing rules satisfy the check; partial coverage receives only the missing details. Explicit overrides are preserved and reported. Repeating Apply should produce no additional baseline changes.

## Design persistence

**Your design system is an authoring input.** The skill treats it as persistent project context, even when the current implementation reflects the same decisions.

| External design workflow | What this maintainer preserves |
|---|---|
| [UI Craft](https://github.com/educlopez/ui-craft) | Project design context and declared sources of truth |
| [Impeccable](https://github.com/pbakaus/impeccable) | `DESIGN.md`, plus `PRODUCT.md` and surface briefs when consumed |
| [Taste](https://github.com/Leonxlnx/taste-skill) | Curated or generated design intent, including `DESIGN.md` |

These dependencies remain external. The maintainer reads the installed version's contract; it does not bundle or rewrite third-party skills.

When a recognized design workflow is present, the skill checks for `DESIGN.md` or an explicitly declared alternative. Missing context becomes a finding. It does not invent brand colors, typography, or product decisions to fill the gap.

## What you get back

- **Proposed changes:** file, action, evidence, score, and behavioral justification.
- **Karpathy baseline:** coverage and instruction path for each principle, with proposed or applied additions marked as required baseline.
- **Protected artifacts:** design/product sources, consumers, and missing inputs.
- **Rejected candidates:** what should stay out of persistent context, and why.
- **Ambiguities:** contradictions that cannot be resolved from current evidence.
- **Diff:** a concrete patch for review, or a summary of applied changes and checks.

## Inside the repo

| File | Purpose |
|---|---|
| [SKILL.md](skills/ai-arch/SKILL.md) | Core maintenance workflow |
| [Karpathy baseline](skills/ai-arch/references/karpathy-guidelines.md) | Coding principles and rules for merging missing coverage |
| [Routing matrix](skills/ai-arch/references/routing-matrix.md) | Choose the right destination for each instruction |
| [Platform map](skills/ai-arch/references/platform-map.md) | Host-specific placement and shared context |
| [Design persistence](skills/ai-arch/references/design-persistence.md) | Preserve design and product sources of truth |
| [Inventory scanner](skills/ai-arch/scripts/audit_ai_architecture.py) | Read-only structural inventory, Markdown or JSON |
| [Tests](tests/test_audit_ai_architecture.py) | Scanner regression tests |

<details>
<summary><strong>Run the inventory scanner</strong></summary>

```bash
python3 skills/ai-arch/scripts/audit_ai_architecture.py \
  --root /path/to/repository \
  --format markdown
```

Use `--format json` for structured output. The scanner supplies evidence for the audit; it is not a full secret scanner or a security certification.

**Current limitation:** use it on trusted repositories. It reads files beyond the configuration inventory, follows file symlinks, and includes the root path and skill metadata in JSON output. Review reports before sharing them.

</details>

## Development

```bash
python3 -m unittest discover -s tests -v
```

Run the tests locally with Python 3.10+. Runtime invocation should also be checked in each target host after installation; unit tests cover the scanner, not live agent behavior.

Contributions should make the workflow clearer, improve a concrete decision, or correct a verified compatibility issue. Keep references focused and preserve the design-persistence contract.

---

Built by [Alessandro Gargiulo](https://github.com/iamgargiulo). Released under the [MIT License](LICENSE).
