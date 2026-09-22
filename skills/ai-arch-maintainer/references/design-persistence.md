# Design persistence contract

Read this reference whenever an audit finds design skills, `DESIGN.md`, `PRODUCT.md`, brand files, design tokens, surface briefs, or requests involving persistent UI taste.

## Core rule

Design intent is not ordinary implementation documentation. It is an authoring input used to evaluate and generate future work. Redundancy with CSS, components, tokens, screenshots, or code does not make it disposable.

## Recognized skill families

Detect skills by frontmatter and behavior, not only fixed paths.

| Skill family | Recognition hints | Persistent contract |
|---|---|---|
| UI Craft | `ui-craft` name or its audit/polish/shape companion skills | Preserve project design context, references, and any declared design source of truth. Do not rewrite vendor skill files. |
| Impeccable | `impeccable` name or launcher/context workflow | Preserve repository `DESIGN.md`; preserve `PRODUCT.md` and surface briefs when consumed by the installed workflow. Run/read its context workflow before changing owned artifacts. |
| Taste | `taste`, `design-taste-frontend`, `stitch-design-taste`, or equivalent frontmatter | Preserve generated or curated `DESIGN.md` output as design intent. Do not flatten it into a generic root instruction file. |
| Other design skills | Description says it generates, reads, or enforces design/brand/product files | Follow the installed skill's explicit artifact contract and record the canonical paths. |

## Required behavior

1. Inventory every `DESIGN.md`, `PRODUCT.md`, brand guide, token source, surface brief, and design-skill `SKILL.md`.
2. Determine ownership and precedence from explicit project instructions and installed skill contracts.
3. If a recognized design skill is installed, require repository-level `DESIGN.md` unless the project explicitly declares another canonical path.
4. If Impeccable or another installed workflow consumes `PRODUCT.md`, keep it persistent.
5. Never replace an authored design file with inferred prose from the current UI.
6. Never delete a design file because the codebase appears to implement it already.
7. When two design sources conflict, report the conflict and ask which is authoritative unless precedence is explicit.
8. When a required design file is missing, report the gap. Do not fabricate brand choices, colors, typography, or product intent.
9. Keep third-party skills external. Store project-specific adapters and design truth in the project, not in managed vendor directories.

## Suggested precedence

Use explicit repository rules first. When none exist, propose this order rather than silently imposing it:

1. direct user instruction for the current project;
2. canonical product and brand sources;
3. repository `PRODUCT.md` and `DESIGN.md`;
4. design tokens and component primitives;
5. incumbent implementation and current screenshots;
6. generic design-skill defaults.

The lower source may reveal drift but should not overwrite higher-level intent without confirmation.

## Audit output

For every protected artifact report:

- canonical path;
- owner/consumer;
- status: present, missing, duplicated, conflicting, or ambiguous;
- whether it is tracked;
- references from persistent instructions or skills;
- proposed action, if any.
