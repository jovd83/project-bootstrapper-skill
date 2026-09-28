#!/usr/bin/env python3
"""Repository-local validation for project-bootstrapper-skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT_REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "agents/openai.yaml",
    "evals/evals.json",
]

SKILL_REQUIRED_SECTIONS = [
    "# Repository Bootstrapper",
    "## Scope",
    "## Required Inputs",
    "## Memory Model",
    "## Preflight Checklist",
    "## Adapter Selection",
    "## Conservative Fallback Scaffold",
    "## Execution Workflow",
    "## Validation Guidance",
    "## Error Handling",
    "## Final Response Contract",
]


def fail(message: str) -> str:
    return f"FAIL: {message}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> tuple[dict[str, str], str | None]:
    if not content.startswith("---\n"):
        return {}, "SKILL.md must start with YAML frontmatter"

    try:
        _, frontmatter, _ = content.split("---\n", 2)
    except ValueError:
        return {}, "SKILL.md frontmatter must be closed with ---"

    values: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("\t"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values, None


def validate_skill_md(root: Path) -> list[str]:
    errors: list[str] = []
    content = read_text(root / "SKILL.md")
    frontmatter, parse_error = parse_frontmatter(content)
    if parse_error:
        errors.append(fail(parse_error))
        return errors

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name != "project-bootstrapper-skill":
        errors.append(fail("SKILL.md frontmatter name must be project-bootstrapper-skill"))
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append(fail("SKILL.md frontmatter name must be lowercase hyphen-case"))
    if not description:
        errors.append(fail("SKILL.md frontmatter description is required"))
    if len(description) > 1024:
        errors.append(fail("SKILL.md frontmatter description must be <= 1024 characters"))
    if "<" in description or ">" in description:
        errors.append(fail("SKILL.md frontmatter description must not contain angle brackets"))

    missing_sections = [section for section in SKILL_REQUIRED_SECTIONS if section not in content]
    for section in missing_sections:
        errors.append(fail(f"SKILL.md missing required section: {section}"))

    return errors


def validate_openai_yaml(root: Path) -> list[str]:
    errors: list[str] = []
    content = read_text(root / "agents/openai.yaml")
    required_fragments = [
        'display_name: "Repository Bootstrapper"',
        "short_description:",
        'default_prompt: "Use $project-bootstrapper-skill',
        "allow_implicit_invocation: false",
    ]
    for fragment in required_fragments:
        if fragment not in content:
            errors.append(fail(f"agents/openai.yaml missing expected fragment: {fragment}"))
    return errors


def validate_release_docs(root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = read_text(root / "SKILL.md")
    readme = read_text(root / "README.md")
    changelog = read_text(root / "CHANGELOG.md")

    expected_fragments = [
        (skill_md, 'version: "2.1.0"', "SKILL.md must declare version 2.1.0"),
        (skill_md, 'maturity: "stable"', "SKILL.md must declare stable maturity"),
        (readme, "version-2.1.0-blue", "README.md must show the 2.1.0 version badge"),
        (readme, "Buy%20Me%20a%20Coffee", "README.md must include the Buy Me a Coffee badge"),
        (readme, "validation-GitHub%20Actions", "README.md must include the validation badge"),
        (readme, "## What This Skill Does", "README.md must describe what the skill does"),
        (readme, "## When To Use It", "README.md must describe when to use the skill"),
        (readme, "npx skills add jovd83/project-bootstrapper-skill", "README.md must include npx skills install guidance"),
        (changelog, "## 1.0.0 - 2026-05-25", "CHANGELOG.md must include the 1.0.0 release entry"),
    ]
    for content, fragment, message in expected_fragments:
        if fragment not in content:
            errors.append(fail(message))
    return errors


def validate_evals(root: Path) -> list[str]:
    errors: list[str] = []
    evals_path = root / "evals/evals.json"
    try:
        payload = json.loads(read_text(evals_path))
    except json.JSONDecodeError as exc:
        return [fail(f"evals/evals.json is invalid JSON: {exc}")]

    if payload.get("skill_name") != "project-bootstrapper-skill":
        errors.append(fail("evals/evals.json skill_name must be project-bootstrapper-skill"))

    evals = payload.get("evals")
    if not isinstance(evals, list) or len(evals) < 5:
        errors.append(fail("evals/evals.json must contain at least 5 eval cases"))
        return errors

    ids = set()
    for index, case in enumerate(evals, start=1):
        if not isinstance(case, dict):
            errors.append(fail(f"eval case {index} must be an object"))
            continue
        case_id = case.get("id")
        if case_id in ids:
            errors.append(fail(f"duplicate eval id: {case_id}"))
        ids.add(case_id)
        for key in ["prompt", "expected_output", "files"]:
            if key not in case:
                errors.append(fail(f"eval id {case_id} missing key: {key}"))
        if not str(case.get("prompt", "")).startswith("Use $project-bootstrapper-skill"):
            errors.append(fail(f"eval id {case_id} prompt must explicitly invoke the skill"))
        files = case.get("files", [])
        if not isinstance(files, list):
            errors.append(fail(f"eval id {case_id} files must be a list"))
            continue
        for relative_file in files:
            if not isinstance(relative_file, str):
                errors.append(fail(f"eval id {case_id} file entries must be strings"))
                continue
            if not (root / relative_file).exists():
                errors.append(fail(f"eval id {case_id} references missing file: {relative_file}"))
    return errors


def validate_ascii(root: Path) -> list[str]:
    errors: list[str] = []
    text_files = [
        "SKILL.md",
        "README.md",
        "CHANGELOG.md",
        "agents/openai.yaml",
        "evals/evals.json",
        "scripts/validate_skill.py",
    ]
    text_files.extend(str(path.relative_to(root)).replace("\\", "/") for path in (root / "evals").glob("**/*.md"))
    text_files.extend(str(path.relative_to(root)).replace("\\", "/") for path in (root / ".github").glob("**/*.yml"))

    for relative_file in sorted(set(text_files)):
        path = root / relative_file
        if not path.exists():
            continue
        content = read_text(path)
        for line_number, line in enumerate(content.splitlines(), start=1):
            if any(ord(char) > 127 for char in line):
                errors.append(fail(f"{relative_file}:{line_number} contains non-ASCII text"))
                break
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for relative_file in ROOT_REQUIRED_FILES:
        if not (root / relative_file).exists():
            errors.append(fail(f"missing required file: {relative_file}"))

    if not errors:
        errors.extend(validate_skill_md(root))
        errors.extend(validate_openai_yaml(root))
        errors.extend(validate_release_docs(root))
        errors.extend(validate_evals(root))
        errors.extend(validate_ascii(root))

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Skill repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
