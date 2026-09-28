---
name: project-bootstrapper-skill
description: Create a new repository scaffold from approved architecture and implementation plans. Use when the user asks to bootstrap, scaffold, initialize, or create the initial project repository, including stack adapter selection, baseline files, planning artifact preservation, validation commands, setup summary, and safe handling of file-writing approvals.
license: MIT
metadata:
  version: "2.0.0"
  maturity: "stable"
  dispatcher-category: "execution"
  dispatcher-layer: "execution"
  dispatcher-risk: "high"
  dispatcher-writes-files: "true"
  dispatcher-capabilities: "repository-bootstrap, scaffold-selection, project-setup, stack-adapter-routing"
  dispatcher-accepted-intents: "bootstrap_project_repository, create_project_skeleton, scaffold_new_repository, initialize_project_repo"
  dispatcher-input-artifacts: "architecture_plan, implementation_tasks, project_constitution, target_path"
  dispatcher-output-artifacts: "bootstrapped_repository, setup_summary, validation_commands, scaffold_report"
  dispatcher-stack-tags: "bootstrap, repository, greenfield, setup"
---

# Repository Bootstrapper

Bootstrap the first usable repository structure for an already-approved project. Treat this as a high-risk file-writing skill: be explicit about target paths, approvals, adapter choices, generated files, commands, and skipped work.

Assume a Codex-style agent that can read and write local files and invoke available stack-specific skills. Network installs, Git operations, and GitHub actions require explicit approval.

## Scope

Use this skill to:

- Create an initial project folder or monorepo skeleton from an approved architecture plan and implementation task plan.
- Route known stacks to stronger stack-specific bootstrap skills when available.
- Add baseline repository hygiene files such as `README.md`, `.gitignore`, `.env.example`, docs folders, and setup notes.
- Preserve approved planning artifacts inside the new repository.
- Run the lightest reasonable validation or produce exact validation commands when execution is not approved.

Do not use this skill to:

- Choose the architecture. Use `greenfield-architecture-planner` or the user's approved architecture artifact.
- Create the implementation backlog. Use `implementation-task-planner`.
- Implement feature behavior beyond scaffold-level smoke checks.
- Install dependencies, initialize Git, create remote repositories, commit, push, or publish without explicit approval.
- Overwrite an existing non-empty target directory without explicit approval.

## Required Inputs

Before writing files, establish:

- Target path, resolved to an absolute path when possible.
- Approved architecture or technical plan.
- Approved implementation task plan.
- Project constitution, constraints, or non-negotiables if provided.
- Approval boundaries for file creation, dependency installation, network access, Git initialization, GitHub or remote repository creation, and destructive cleanup.

If any required input is missing or ambiguous, ask for the smallest clarification needed. If the user has already approved the target path and plans in the current thread, proceed within those boundaries.

## Memory Model

- Runtime memory: keep adapter decisions, command results, validation status, and unresolved questions only for the current task.
- Project-local memory: persist stable project artifacts inside the generated repository, preferably under `.agentspec/` and `docs/`, with clear filenames and provenance when available.
- Shared memory: do not write cross-agent shared memory from this skill. If a user asks to promote reusable project facts, record them in the agent's own memory (for example CLAUDE.md or AGENTS.md) as an explicit step.

Runtime notes must not automatically become persistent files. Project-local artifacts must not automatically become shared memory.

## Preflight Checklist

1. Resolve the target path and inspect whether it exists.
2. If the target directory exists and is non-empty, stop unless the user explicitly approved writing into it.
3. Identify stack components from the approved plan: frontend, backend, API contract, database, worker, agent, MCP server, infrastructure, or documentation-only project.
4. Select adapters before creating files. For multi-stack systems, create a root structure that cleanly contains each component instead of letting one adapter dominate the repository layout.
5. Decide which actions are allowed now and which must be reported as skipped.
6. Prefer a short scaffold plan before writes when the target is non-empty, the architecture is multi-stack, or approvals are narrow.

## Adapter Selection

Use the strongest available stack skill for scaffold work:

| Project need | Preferred adapter |
| --- | --- |
| New Angular application | `angular-new-app` |
| Angular code inside an existing scaffold | `angular-developer` |
| Spring Boot or Java service | `dr-jskill` |
| MCP server | `mcp-builder` |
| API contract-first project | `openapi-spec-generation` |
| Olakai-monitored AI agent | `new-project` |

Adapter rules:

- Use `new-project` only when the approved plan explicitly calls for an Olakai-monitored AI agent.
- Use `openapi-spec-generation` for contract artifacts; do not treat it as a full application scaffold unless the plan says so.
- If a preferred adapter is unavailable, create a conservative fallback scaffold and report the missing adapter.
- Do not invent package managers, framework versions, deployment platforms, or CI systems that are not present in the approved plan.

## Conservative Fallback Scaffold

For unsupported stacks or when dependency/network actions are not approved, create only the minimum useful repository structure:

```text
target/
|-- README.md
|-- .gitignore
|-- .env.example
|-- .agentspec/
|   |-- architecture.md
|   |-- implementation-plan.md
|   `-- scaffold-report.md
|-- docs/
|   |-- architecture/
|   |-- api/
|   |-- testing/
|   `-- release/
|-- specs/
|-- src/              # only when the architecture implies source code
`-- tests/            # only when the stack supports automated tests
```

Keep placeholders lightweight. Prefer `.gitkeep` or a short README in empty directories only when needed to make intent clear.

## Execution Workflow

1. Confirm inputs and approvals.
2. Inspect the target path and existing contents.
3. Choose adapters and fallback areas.
4. Create the target directory and scaffold root files.
5. Invoke stack-specific adapters where applicable and allowed.
6. Preserve planning artifacts under `.agentspec/`:
   - `architecture.md`
   - `implementation-plan.md`
   - `constitution.md` when provided
   - `scaffold-report.md`
7. Add common repository hygiene files only when they do not conflict with generated stack files.
8. Run the lightest approved validation command for each component.
9. Update `scaffold-report.md` with adapter choices, files created, commands run, validation results, skipped actions, and next recommended skill or phase.
10. Finalize with a concise setup summary.

## Validation Guidance

Prefer fast, local, deterministic checks:

- Framework smoke test or build command from the selected adapter.
- Package manager validation only if dependency installation is approved or dependencies already exist.
- Static checks for generated specs or config when available.
- README/setup command review when executable validation is not possible.

If validation cannot run, explain why and provide exact commands for the user or next agent. Do not claim the scaffold works without evidence.

## Error Handling

When a scaffold or validation command fails:

- Capture the command, working directory, exit status, and the useful portion of the error.
- Fix obvious local scaffold mistakes within the approved scope.
- Stop before destructive cleanup, global changes, network installs, or retries that require fresh approval.
- Leave a readable `scaffold-report.md` even for partial scaffolds, clearly marking incomplete areas.

## Final Response Contract

Report in this order:

```markdown
Repository: [absolute path]
Adapters: [adapter per component, or fallback]
Created/changed: [high-signal file and folder summary]
Commands run: [commands and results]
Validation: [passed, failed, skipped with reason]
Planning artifacts: [where architecture/tasks/constitution were preserved]
Skipped: [actions not approved or not applicable]
Next: [recommended implementation skill or next manual command]
```

Keep the final response factual. Mention approvals that limited the work, missing adapters, and unresolved risks.
