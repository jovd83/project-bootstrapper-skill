---
name: project-bootstrapper-skill
description: Bootstrap a new repository skeleton from an approved architecture and implementation task plan. Use when creating the initial project folder, stack scaffold, dotfiles, README, environment sample, docs structure, validation commands, and local development setup while routing to stack-specific bootstrap skills when available.
metadata:
  dispatcher-category: execution
  dispatcher-layer: execution
  dispatcher-lifecycle: draft
  dispatcher-risk: high
  dispatcher-writes-files: true
  dispatcher-capabilities: repository-bootstrap, scaffold-selection, project-setup, stack-adapter-routing
  dispatcher-accepted-intents: bootstrap_project_repository, create_project_skeleton, scaffold_new_repository
  dispatcher-input-artifacts: architecture_plan, implementation_tasks, project_constitution, target_path
  dispatcher-output-artifacts: bootstrapped_repository, setup_summary, validation_commands, scaffold_report
  dispatcher-stack-tags: bootstrap, repository, greenfield, setup
---

# Project Bootstrapper Skill

Use this skill after the user has approved the architecture plan, task plan, target path, and any dependency installation or network actions.

This skill creates the repository skeleton. It should route to stack-specific skills where the portfolio already has a stronger scaffold.

## Outcomes

- Create the initial project directory and source scaffold.
- Reuse stack-specific bootstrap skills when available.
- Add common project files such as `README.md`, `.gitignore`, `.env.example`, docs folders, and validation notes.
- Preserve the project constitution, specs, architecture plan, and task plan inside the new repository.
- Produce a setup summary with commands that were run and commands still required.

## Do Not Use This Skill For

- Choosing architecture. Use `greenfield-architecture-planner`.
- Creating implementation tasks. Use `implementation-task-planner-skill`.
- Implementing feature behavior beyond scaffold-level smoke checks.
- Publishing to GitHub or pushing commits unless explicitly approved.

## Workflow

0. Log telemetry if available:

```bash
%USERPROFILE%\.agents\skills\skill-dispatcher\log-dispatch.cmd --skill project-bootstrapper-skill --intent bootstrap_project_repository --model <model_name> --reason <reason>
```

1. Confirm target path and approval to create files there.
2. Confirm whether dependency installation, network access, Git initialization, or GitHub repository creation is allowed.
3. Read the architecture plan, task plan, and constitution.
4. Select a bootstrap adapter:
   - Angular application: use `angular-new-app`.
   - Angular code inside an existing scaffold: use `angular-developer`.
   - Spring Boot or Java service: use `dr-jskill`.
   - MCP server: use `mcp-builder`.
   - Olakai-monitored AI agent: use `new-project`.
   - API contract first: use `openapi-spec-generation`.
   - Unsupported or minimal stack: create a conservative repository skeleton using native tooling and documented commands.
5. Create or preserve the project artifact folders.
6. Add common repository hygiene files only when they do not conflict with the stack scaffold.
7. Run the lightest available validation command, such as build, test, or framework smoke check.
8. Produce a setup summary.

## Common Artifact Placement

Prefer preserving planning artifacts in:

```text
.agentspec/
specs/
docs/architecture/
docs/api/
docs/testing/
docs/release/
```

If a framework scaffold has strong conventions, keep its source layout and place agent artifacts around it rather than forcing a foreign source layout.

## Adapter Rules

### Angular

Use `angular-new-app` for new Angular applications. After scaffold, use `angular-developer` for components, services, routing, and build validation.

### Spring Boot

Use `dr-jskill` for Java and Spring Boot projects. Preserve its generated structure and validation guidance.

### MCP Server

Use `mcp-builder` for MCP servers. Prefer TypeScript unless the architecture plan justifies Python.

### AI Agent With Olakai Monitoring

Use `new-project` only when the project is specifically an AI agent requiring Olakai workflow, agent, KPI, and SDK setup.

### Minimal Or Unsupported Stack

Create only:

- source directory placeholder appropriate to the architecture
- tests directory placeholder if the stack supports it
- `README.md`
- `.gitignore`
- `.env.example`
- docs and spec folders
- validation notes

Do not invent package managers, frameworks, or CI commands.

## Guardrails

- Do not overwrite an existing non-empty target directory without explicit approval.
- Do not run install commands without approval when they require network or modify global state.
- Do not initialize Git, commit, push, or create a GitHub repository unless explicitly approved.
- Do not hide scaffold failures. Capture the command and failure output.
- Do not create a custom scaffold when a stronger stack-specific skill applies.
- Do not implement feature scope beyond smoke-level scaffolding.

## Final Response

Report:

- repository path
- adapter selected
- files and folders created
- commands run
- validation results
- skipped steps and why
- next implementation skill or chain phase
