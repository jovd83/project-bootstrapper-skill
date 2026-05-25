# Contract Service Architecture

## Summary

Contract Service is an API contract-first Java service. The bootstrap should establish a place for OpenAPI artifacts before service implementation begins.

## Components

- `contracts/openapi`: OpenAPI source documents and generated previews when approved.
- `services/api`: Java service scaffold.
- `docs/api`: endpoint rationale and compatibility notes.
- `.agentspec`: architecture, implementation plan, and scaffold report.

## Constraints

- Network access is denied during the initial bootstrap.
- Dependency installation is denied during the initial bootstrap.
- The bootstrap should provide exact follow-up commands instead of running package-manager or generator commands that require downloads.
