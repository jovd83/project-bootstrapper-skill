# Repository Bootstrapper Skill

[![version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![status](https://img.shields.io/badge/status-stable-3fb950)](SKILL.md)
[![category](https://img.shields.io/badge/category-execution-0a7ea4)](SKILL.md)
[![validation](https://img.shields.io/badge/validation-GitHub%20Actions-2088ff)](.github/workflows/validate.yml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/jovd83)

`repository-bootstrapper-skill` helps an AI coding agent create the first usable repository scaffold for an approved greenfield project.

It is intentionally conservative: it routes to stack-specific bootstrap skills when they exist, writes only within approved boundaries, preserves planning artifacts locally, and reports exactly what was created, validated, skipped, or left for the next phase.

## What This Skill Does

Use `repository-bootstrapper-skill` to turn approved planning artifacts into a safe, auditable repository scaffold.

- Creates an initial repository folder or monorepo skeleton from approved architecture and task plans.
- Selects stack-specific adapters such as `angular-new-app`, `dr-jskill`, `mcp-builder`, `openapi-spec-generation`, and `new-project`.
- Adds baseline files such as `README.md`, `.gitignore`, `.env.example`, `.agentspec/`, `docs/`, and `specs/`.
- Preserves approved architecture, implementation plan, and project constitution artifacts in the generated repository.
- Runs light validation when approved and records validation commands for later execution.
- Produces a setup summary and scaffold report.

## When To Use It

Use this skill when:

- The architecture plan, implementation task plan, and target path are already approved.
- A new repository or monorepo skeleton needs to be created before feature implementation begins.
- The project needs stack-aware scaffolding but should still preserve common agent planning artifacts.
- Bootstrap work must respect explicit approval boundaries for file writes, dependency installation, network access, Git, and remotes.
- A chain such as `project-genesis-chain` reaches its repository-bootstrap phase.

Do not use it for architecture selection, backlog creation, feature implementation, release publishing, or unsafe writes into an existing non-empty directory.

## What This Skill Does Not Do

- It does not choose the architecture.
- It does not create the implementation backlog.
- It does not implement product features beyond scaffold-level smoke checks.
- It does not install dependencies, initialize Git, create remotes, commit, push, or publish unless explicitly approved.
- It does not overwrite existing non-empty directories without explicit approval.

## Install

Install by copying or cloning this folder into an Agent Skills directory supported by your agent.

With the Skills CLI, after this repository is published to GitHub:

```powershell
npx skills add jovd83/project-bootstrapper-skill
```

For a fork, replace `jovd83` with the GitHub owner or organization that hosts the repository.

For Codex-style local skills:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\repository-bootstrapper-skill"
```

For repository-local sharing:

```powershell
New-Item -ItemType Directory -Force .agents\skills
Copy-Item -Recurse . .agents\skills\repository-bootstrapper-skill
```

The skill follows the Agent Skills convention of a required `SKILL.md` file with optional supporting folders.

## Usage

Example prompt:

```text
Use $repository-bootstrapper-skill to create C:/projects/taskify from the approved architecture plan and implementation task list below. You may create files, but do not install dependencies or initialize Git.
```

Best results come from providing:

- Target path.
- Approved architecture or technical plan.
- Approved implementation task plan.
- Project constitution or non-negotiable constraints.
- Explicit approvals for network access, dependency installation, Git initialization, and remote repository creation.

## Adapter Preference

| Project type | Preferred adapter |
| --- | --- |
| New Angular application | `angular-new-app` |
| Angular code inside an existing scaffold | `angular-developer` |
| Spring Boot or Java service | `dr-jskill` |
| MCP server | `mcp-builder` |
| API contract-first project | `openapi-spec-generation` |
| Olakai-monitored AI agent | `new-project` |
| Unsupported or minimal stack | Conservative fallback scaffold |

If an adapter is unavailable, the skill falls back to a minimal scaffold and reports the adapter gap.

## Output Contract

The agent should finish with:

- Repository path.
- Adapter selected for each component.
- Files and folders created or changed.
- Commands run and their results.
- Validation status.
- Preserved planning artifact locations.
- Skipped steps and reasons.
- Recommended next implementation skill or command.

The generated repository should also include `.agentspec/scaffold-report.md` when files were created.

## Memory and Artifact Boundaries

The skill uses a deliberately scoped memory model:

- Runtime memory: temporary decisions, command results, and validation state for the active bootstrap task.
- Project-local memory: durable artifacts written into the generated repository, usually under `.agentspec/` and `docs/`.
- Shared memory: out of scope unless the user explicitly delegates to a separate shared-memory workflow.

Runtime notes are not automatically persisted. Project-local artifacts are not automatically promoted to shared memory.

## Repository Layout

```text
repository-bootstrapper-skill/
|-- .github/
|   `-- workflows/
|       `-- validate.yml
|-- SKILL.md
|-- README.md
|-- CHANGELOG.md
|-- LICENSE
|-- agents/
|   `-- openai.yaml
|-- evals/
|   |-- evals.json
|   |-- fixtures/
|   `-- forward-test-report.md
`-- scripts/
    `-- validate_skill.py
```

## Evaluation

The eval suite in `evals/evals.json` covers:

- Multi-stack happy path routing.
- Existing non-empty target directory protection.
- Unsupported stack fallback behavior.
- Network and dependency installation denial.
- Missing required planning artifacts.

The eval prompts reference concrete fixtures under `evals/fixtures/` so reviewers can test behavior against realistic architecture and task artifacts.

Run the repository-local static validator:

```powershell
python scripts/validate_skill.py .
```

The same validator runs in GitHub Actions through `.github/workflows/validate.yml`.

Run your preferred Agent Skills evaluation harness against the eval prompts, then update the evals when real bootstrap failures reveal new edge cases. The local forward-test trace in `evals/forward-test-report.md` records a documentation-first fallback scaffold scenario.

## Maintainer Notes

- Keep `SKILL.md` concise and procedural; move only genuinely reusable detail into supporting files.
- Update `agents/openai.yaml` when the skill name, description, or default prompt changes.
- Add evals for every meaningful guardrail or adapter behavior change.
- Run `python scripts/validate_skill.py .` before opening a pull request.
- Validate frontmatter after edits with a compatible Agent Skills validator when available.

## License

MIT. See [LICENSE](LICENSE).
