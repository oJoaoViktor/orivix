# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Orivix is a web system that digitalizes weekly attendance sheets and student observations for vocational school classes, replacing a paper-based process. Class representatives fill daily attendance and register observations; advisors monitor everything in real time.

## Documentation

- [Requirements](docs/requirements.md) — business rules and features
- [Architecture](docs/architecture.md) — stack, patterns, folder structure
- [Data Model](docs/data-model.md) — entities, fields, constraints
- [Roadmap](docs/roadmap.md) — project phases and progress
- [ADRs](docs/adr/) — architecture decision records
- [Class Diagram](docs/diagrams/class-diagram.puml) — PlantUML diagram

## Stack

- **Backend**: Python 3.13+, Django, Django REST Framework, SimpleJWT, Django Channels, django-tenants
- **Frontend**: Vue 3 + Vite
- **Database**: PostgreSQL
- **Package manager**: uv

## Commands

### Backend
```bash
make run        # start dev server
make test       # run all tests
make test-k k=test_name   # run single test by name
make lint       # check linting
make format     # format code
make migrate    # run migrations
```

## Key Patterns

- **DDD**: code organized by domain under `backend/domains/`
- **Repository Pattern**: ORM queries only inside `repositories.py` — never in views or services
- **Result Pattern**: services return a Result object — no exceptions for expected business failures
- **TDD**: tests are written before implementation (Red → Green → Refactor)
- **Soft delete**: never hard delete — all models have `deleted_at`
- **UUID v7**: all primary keys use UUID v7 (time-ordered)

## Multi-tenancy

Each school is an isolated PostgreSQL schema managed by `django-tenants`. The schema is resolved automatically from the subdomain. See [Architecture](docs/architecture.md) and [ADR 003](docs/adr/003-multi-tenancy-schema.md).

## Architecture

Each domain under `backend/domains/` follows the same structure:

```
domain/
├── models/          # entities
├── services.py      # business logic
├── repositories.py  # ORM queries
├── serializers.py   # input/output (DRF)
├── views.py         # HTTP handlers (thin, no business logic)
├── urls.py
└── exceptions.py
```

See [Architecture](docs/architecture.md) for the full folder tree.

## Bruno

API requests are versioned as Bruno collection files under `bruno/`. After each completed feature, update the corresponding collection. See [bruno/README.md](bruno/README.md).

## Git

Manage commits autonomously — no need to ask for approval. Commit at logical progress points (e.g., after a working scaffold, after a complete feature, after migrations pass). Follow Conventional Commits format. All commit messages must be in English.
