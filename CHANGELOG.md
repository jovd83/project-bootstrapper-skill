# Changelog

All notable changes to `project-bootstrapper-skill` are documented here.

## 2.1.0 - 2026-09-28

### Changed

- Invoke-only: `disable-model-invocation: true` for Claude Code and `allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. The skill writes files and is phase 9 of `project-genesis-chain`, which the `project-genesis` agent runs; it no longer competes for automatic selection. Run it with `/project-bootstrapper-skill` or `$project-bootstrapper-skill`.
- `metadata` carries the author.

## 2.0.0 - 2026-09-27

### Changed

- **BREAKING:** the skill is named `project-bootstrapper-skill` again, matching its folder and repository. The trigger is now `$project-bootstrapper-skill`. README, `agents/openai.yaml`, evals and the validator follow.
- `project-genesis-chain` phase 9 calls it by this name.

### Fixed

- The validator expected a `<github-owner>` placeholder in the README's install command, while the README has the real `npx skills add jovd83/project-bootstrapper-skill`, so CI failed.

## 1.0.0 - 2026-05-25

### Added

- Enterprise-grade repository bootstrap execution contract in `SKILL.md`.
- Approval-gated workflow for target paths, installs, network access, Git, remotes, and destructive cleanup.
- Explicit adapter routing for Angular, Spring Boot/Java, MCP servers, API contract-first projects, and monitored AI agents.
- Conservative fallback scaffold for unsupported stacks or denied dependency/network actions.
- Runtime, project-local, and shared-memory boundary model.
- Repository-local validator in `scripts/validate_skill.py`.
- GitHub Actions validation workflow in `.github/workflows/validate.yml`.
- Codex/OpenAI UI metadata in `agents/openai.yaml`.
- Expanded eval suite with realistic fixtures and a recorded forward-test report.
- GitHub-ready README with install, usage, validation, evaluation, and maintainer guidance.

### Changed

- Renamed the skill identity from `project-bootstrapper-skill` to `repository-bootstrapper-skill`.
- Promoted maturity from beta to stable.
- Updated `project-genesis-chain` integration guidance to use `repository-bootstrapper-skill` for repository bootstrap.

### Validation

- `python scripts/validate_skill.py .`
- Agent Skills quick validator for `SKILL.md` frontmatter.
- JSON parse checks for eval metadata.
- `git diff --check`.

## 0.2.0 - 2026-05-24

### Added

- Stronger skill contract, README, eval fixtures, validation script, GitHub Actions workflow, and forward-test report.

## 0.1.0 - 2026-05-24

### Added

- Initial draft skill for bootstrapping repository skeletons from approved architecture and task plans.
