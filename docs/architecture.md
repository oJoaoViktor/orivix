# Architecture

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13+, Django, Django REST Framework |
| Authentication | SimpleJWT |
| Real-time | Django Channels (WebSockets) |
| Multi-tenancy | django-tenants (schema per tenant) |
| Frontend | Vue 3 + Vite |
| Database | PostgreSQL |
| Package manager | uv |
| Linter / Formatter | ruff |
| Testing | pytest, pytest-django, factory_boy, faker |
| Pre-commit | ruff |
| CI/CD | GitHub Actions |
| Quality gate | SonarCloud (minimum 80% coverage) |
| Deployment | Rancher |
| API client | Bruno |

---

## Multi-tenancy

Each school is an isolated tenant with its own PostgreSQL schema, managed by `django-tenants`. The correct schema is resolved automatically from the request subdomain.

```
admin.orivix.com   → public schema  (Tenant, Domain — admin only)
school1.orivix.com → schema school1 (all other models)
school2.orivix.com → schema school2 (all other models, fully isolated)
```

- **Public schema**: `Tenant`, `Domain`. Only the admin accesses this.
- **Tenant schemas**: all domain models (Classroom, Student, Attendance, etc.). Completely isolated between tenants.
- No `tenant_id` column on any model — isolation is enforced at the schema level.

---

## Backend Structure

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── shared/
│   ├── models.py            # BaseModel (abstract)
│   ├── exceptions.py        # base exceptions
│   └── utils.py
│
└── domains/
    ├── accounts/            # User, authentication
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── user.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    ├── classrooms/          # Classroom
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── classroom.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    ├── students/            # Student, ClassMembership, Representative
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── student.py
    │   │   ├── class_membership.py
    │   │   └── representative.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    ├── attendance/          # Attendance, AttendanceRecord
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── attendance.py
    │   │   └── attendance_record.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    ├── observations/        # Observation
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── observation.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    ├── advisor/             # AdvisorNote
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── advisor_note.py
    │   ├── services.py
    │   ├── repositories.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── exceptions.py
    │
    └── notifications/       # Notification, WebSocket consumers
        ├── models/
        │   ├── __init__.py
        │   └── notification.py
        ├── consumers.py
        ├── services.py
        ├── repositories.py
        ├── serializers.py
        ├── views.py
        ├── urls.py
        └── exceptions.py
```

---

## Frontend Structure

```
frontend/
└── src/
    ├── shared/              # shared components and utilities
    └── domains/
        ├── accounts/
        │   ├── views/
        │   ├── components/
        │   ├── store/
        │   ├── api/
        │   └── composables/
        ├── classrooms/
        ├── students/
        ├── attendance/
        ├── observations/
        ├── advisor/
        └── notifications/
```

---

## Bruno Collections

API requests are documented as Bruno collection files, versioned in the repository. Collections are updated after each feature is completed.

```
bruno/
├── accounts/
├── classrooms/
├── students/
├── attendance/
├── observations/
├── advisor/
└── notifications/
```

---

## Key Patterns

### Repository Pattern
ORM queries live exclusively in `repositories.py`. Services and views never access the ORM directly.

### Result Pattern
Services return a `Result` object instead of raising exceptions for expected business failures. This keeps error handling explicit and predictable.

### TDD
All features are implemented following Red → Green → Refactor. Tests live inside each domain under `domains/<domain>/tests/`.

### Soft Delete
Nothing is ever hard deleted. All models inherit `deleted_at` from `BaseModel`. Querysets filter out soft-deleted records by default.

### UUID v7
All primary keys use UUID v7 (time-ordered). Available natively in Python 3.13+ via `uuid.uuid7()`.

### Clean Code & SRP
Each file has a single responsibility. Views are thin — they call services and return responses. Business logic belongs exclusively in services.

---

## Development Flow

### Branching
GitHub Flow: `main` is always deployable. Features and fixes are developed on `feature/<name>` or `fix/<name>` branches and merged via pull request.

### Commit messages
Conventional Commits format: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.

### Versioning
Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`.

### Pull request pipeline (GitHub Actions)
Every PR to `main` runs:
1. `commitlint` — validates commit message format
2. `ruff check` — linting
3. `ruff format --check` — formatting
4. `pytest` — test suite
5. Coverage check — minimum 80%
6. SonarCloud analysis — quality gate

---

## API

All endpoints are prefixed with `/api/v1/`.

---

## WebSocket Authentication

WebSocket connections do not support custom HTTP headers on the initial handshake. Authentication is handled by passing the JWT token as a query parameter:

```
ws://school1.orivix.com/ws/?token=<access_token>
```

A custom Django Channels middleware intercepts the connection, validates the token, and attaches the authenticated user before the consumer is invoked. Unauthenticated connections are rejected immediately.

---

## Admin Interface

The `admin` role has a dedicated interface within the platform (not Django Admin). Django Admin is used only to bootstrap the first admin user. All subsequent user and tenant management happens through the platform's own admin views.
