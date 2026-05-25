# Changelog

All notable changes to `repository-bootstrapper-skill` are documented here.

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
