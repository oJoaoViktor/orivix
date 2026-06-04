# ADR 001 — DDD Architecture

## Status
Accepted

## Context
The system has multiple distinct domains (classrooms, students, attendance, observations, notifications) with different business rules and lifecycles. A flat structure would mix concerns and make the codebase harder to navigate and maintain as the system grows.

## Decision
Adopt Domain-Driven Design (DDD) as the organizing principle for the backend. Each domain lives under `backend/domains/` and contains its own models, services, repositories, serializers, views, and URLs.

Within each domain, models are split into individual files under a `models/` package to allow granular navigation without losing domain cohesion.

## Consequences
- Business logic is isolated per domain — changes in one domain do not bleed into others
- Each domain can be understood independently
- Slightly more files and folders than a flat structure, but navigation remains straightforward
- Cross-domain dependencies must be explicit (import from another domain's models or services)
