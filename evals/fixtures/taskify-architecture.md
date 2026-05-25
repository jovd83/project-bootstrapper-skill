# Taskify Architecture

## Summary

Taskify is a small task management application with an Angular web client and a Spring Boot REST API. The project should use a two-component repository layout so frontend and backend tooling stay isolated.

## Components

- `apps/web`: Angular application for task boards, task detail, and account settings.
- `services/api`: Spring Boot API for users, projects, tasks, comments, and audit events.
- `docs/api`: OpenAPI contract drafts and endpoint notes.
- `.agentspec`: approved planning artifacts and scaffold report.

## Constraints

- Do not initialize Git during bootstrap.
- Do not install dependencies unless the user explicitly approves network access.
- Prefer stack-specific skills for Angular and Java scaffolding.
- Keep validation to local smoke checks that do not require dependency downloads.
