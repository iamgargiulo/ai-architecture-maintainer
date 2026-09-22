#!/usr/bin/env python3
"""Read-only inventory for persistent AI-agent architecture in a repository."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".venv",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

ROOT_INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md"}
PROTECTED_DESIGN_NAMES = {
    "BRAND.md",
    "DESIGN.md",
    "PRODUCT.md",
    "STYLEGUIDE.md",
    "STYLE_GUIDE.md",
}
DESIGN_SKILL_HINTS = (
    "ui-craft",
    "impeccable",
    "taste-skill",
    "design-taste",
    "stitch-design-taste",
)
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key)\b\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


@dataclass(frozen=True)
class FileRecord:
    path: str
    lines: int
    tracked: bool | None


@dataclass(frozen=True)
class SkillRecord:
    path: str
    name: str | None
    description: str | None
    lines: int
    design_related: bool
    valid_minimum_frontmatter: bool


def walk_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        base = Path(current)
        for name in sorted(files):
            yield base / name


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def line_count(text: str) -> int:
    return len(text.splitlines())


def tracked_paths(root: Path) -> set[str] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return {item.decode("utf-8", errors="replace") for item in result.stdout.split(b"\0") if item}


def is_tracked(rel: str, tracked: set[str] | None) -> bool | None:
    if tracked is None:
        return None
    return rel in tracked


def parse_frontmatter(text: str) -> tuple[str | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, None
    name = None
    description = None
    for line in lines[1:end]:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"\'') or None
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"\'') or None
    return name, description


def looks_like_cursor_rule(rel: str) -> bool:
    return rel.startswith(".cursor/rules/") and rel.endswith((".md", ".mdc"))


def looks_like_scoped_rule(rel: str) -> bool:
    return (
        rel.startswith(".claude/rules/")
        or looks_like_cursor_rule(rel)
        or fnmatch.fnmatch(rel, "**/.claude/rules/*.md")
    )


def detect_platforms(paths: set[str]) -> list[str]:
    platforms = []
    if any(p == "CLAUDE.md" or "/CLAUDE.md" in p or p.startswith(".claude/") for p in paths):
        platforms.append("claude-code")
    if any(p == "AGENTS.md" or "/AGENTS.md" in p or p.startswith(".agents/") for p in paths):
        platforms.append("codex")
    if any(p.startswith(".cursor/") for p in paths):
        platforms.append("cursor")
    return platforms


def contains_secret_like_value(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def audit(root: Path) -> dict:
    files = list(walk_files(root))
    rel_paths = {relative(path, root) for path in files}
    tracked = tracked_paths(root)

    instructions: list[FileRecord] = []
    settings_and_enforcement: list[FileRecord] = []
    protected: list[FileRecord] = []
    skills: list[SkillRecord] = []
    warnings: list[dict[str, str]] = []

    for path in files:
        rel = relative(path, root)
        name = path.name
        text = read_text(path)
        lines = line_count(text)
        tracked_state = is_tracked(rel, tracked)

        if name in ROOT_INSTRUCTION_NAMES or looks_like_scoped_rule(rel):
            instructions.append(FileRecord(rel, lines, tracked_state))
            if name in ROOT_INSTRUCTION_NAMES and lines > 200:
                warnings.append({
                    "code": "large-always-on-file",
                    "path": rel,
                    "message": f"{lines} lines; review signal density and scope.",
                })
            if contains_secret_like_value(text):
                warnings.append({
                    "code": "possible-secret",
                    "path": rel,
                    "message": "Potential secret-like assignment detected; inspect locally without printing values.",
                })

        if (
            rel.startswith(".claude/agents/")
            or rel.startswith(".claude/hooks/")
            or rel in {".claude/settings.json", ".claude/settings.local.json"}
            or rel.startswith(".cursor/hooks")
        ):
            settings_and_enforcement.append(FileRecord(rel, lines, tracked_state))

        if name in PROTECTED_DESIGN_NAMES:
            protected.append(FileRecord(rel, lines, tracked_state))

        if name == "SKILL.md":
            skill_name, description = parse_frontmatter(text)
            haystack = " ".join(filter(None, (rel, skill_name, description))).lower()
            design_related = (
                skill_name != "ai-arch-maintainer"
                and any(hint in haystack for hint in DESIGN_SKILL_HINTS)
            )
            skills.append(
                SkillRecord(
                    path=rel,
                    name=skill_name,
                    description=description,
                    lines=lines,
                    design_related=design_related,
                    valid_minimum_frontmatter=bool(skill_name and description),
                )
            )
            if not (skill_name and description):
                warnings.append({
                    "code": "invalid-skill-frontmatter",
                    "path": rel,
                    "message": "SKILL.md is missing a non-empty name or description.",
                })
            if lines > 500:
                warnings.append({
                    "code": "large-skill-body",
                    "path": rel,
                    "message": f"{lines} lines; consider progressive disclosure through references.",
                })

    design_skills = [skill for skill in skills if skill.design_related]
    root_design = next((item for item in protected if item.path == "DESIGN.md"), None)
    root_product = next((item for item in protected if item.path == "PRODUCT.md"), None)

    if design_skills and root_design is None:
        warnings.append({
            "code": "missing-design-source",
            "path": "DESIGN.md",
            "message": "A recognized design skill is present but repository-level DESIGN.md is missing; verify the canonical design-source path.",
        })

    if any((skill.name or "").lower() == "impeccable" for skill in design_skills) and root_product is None:
        warnings.append({
            "code": "missing-product-source",
            "path": "PRODUCT.md",
            "message": "Impeccable is present but repository-level PRODUCT.md is missing; verify whether its context workflow requires it.",
        })

    local_settings = next((item for item in settings_and_enforcement if item.path == ".claude/settings.local.json"), None)
    if local_settings and local_settings.tracked:
        warnings.append({
            "code": "tracked-local-settings",
            "path": local_settings.path,
            "message": "A local settings file is tracked; verify that it contains no personal or machine-specific configuration.",
        })

    return {
        "root": str(root),
        "platforms": detect_platforms(rel_paths),
        "instructions": [asdict(item) for item in sorted(instructions, key=lambda x: x.path)],
        "skills": [asdict(item) for item in sorted(skills, key=lambda x: x.path)],
        "settings_and_enforcement": [
            asdict(item) for item in sorted(settings_and_enforcement, key=lambda x: x.path)
        ],
        "design_persistence": {
            "recognized_design_skills": [asdict(item) for item in design_skills],
            "protected_artifacts": [asdict(item) for item in sorted(protected, key=lambda x: x.path)],
            "root_design_present": root_design is not None,
            "root_product_present": root_product is not None,
        },
        "warnings": warnings,
    }


def tracked_label(value: bool | None) -> str:
    if value is None:
        return "unknown"
    return "yes" if value else "no"


def markdown(report: dict) -> str:
    lines = ["# AI architecture inventory", ""]
    platforms = report["platforms"]
    lines.extend(["## Platforms", "", ", ".join(platforms) if platforms else "No host-specific configuration detected.", ""])

    lines.extend(["## Always-on instructions and scoped rules", ""])
    if report["instructions"]:
        lines.extend(["| Path | Lines | Tracked |", "|---|---:|---|"])
        for item in report["instructions"]:
            lines.append(f"| `{item['path']}` | {item['lines']} | {tracked_label(item['tracked'])} |")
    else:
        lines.append("None detected.")
    lines.append("")

    lines.extend(["## Skills", ""])
    if report["skills"]:
        lines.extend(["| Path | Name | Lines | Design-related | Valid metadata |", "|---|---|---:|---|---|"])
        for item in report["skills"]:
            lines.append(
                f"| `{item['path']}` | `{item['name'] or ''}` | {item['lines']} | "
                f"{'yes' if item['design_related'] else 'no'} | {'yes' if item['valid_minimum_frontmatter'] else 'no'} |"
            )
    else:
        lines.append("None detected.")
    lines.append("")

    design = report["design_persistence"]
    lines.extend(["## Design persistence", ""])
    lines.append(f"Recognized design skills: {len(design['recognized_design_skills'])}")
    lines.append(f"Repository `DESIGN.md`: {'present' if design['root_design_present'] else 'missing'}")
    lines.append(f"Repository `PRODUCT.md`: {'present' if design['root_product_present'] else 'missing'}")
    lines.append("")
    if design["protected_artifacts"]:
        lines.extend(["| Protected artifact | Lines | Tracked |", "|---|---:|---|"])
        for item in design["protected_artifacts"]:
            lines.append(f"| `{item['path']}` | {item['lines']} | {tracked_label(item['tracked'])} |")
        lines.append("")

    lines.extend(["## Settings and enforcement", ""])
    if report["settings_and_enforcement"]:
        for item in report["settings_and_enforcement"]:
            lines.append(f"- `{item['path']}` ({item['lines']} lines, tracked: {tracked_label(item['tracked'])})")
    else:
        lines.append("None detected.")
    lines.append("")

    lines.extend(["## Warnings", ""])
    if report["warnings"]:
        for item in report["warnings"]:
            lines.append(f"- **{item['code']}** — `{item['path']}`: {item['message']}")
    else:
        lines.append("No structural warnings detected.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to inspect")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    report = audit(root)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
