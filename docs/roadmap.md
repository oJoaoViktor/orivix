# Roadmap

## Phase 1 — Foundation
- [ ] Repository setup (GitHub Actions, pre-commit, ruff, SonarCloud)
- [ ] Backend project scaffold (uv, Django, DRF, django-tenants, settings per environment)
- [ ] `BaseModel` and shared utilities
- [ ] `Tenant` and `Domain` models (public schema)
- [ ] `User` model and authentication (JWT, first login, forgot password)
- [ ] Admin role: manage tenants and advisor accounts

## Phase 2 — Classrooms & Students
- [ ] `Classroom` CRUD
- [ ] `Student` CRUD (individual + spreadsheet upload)
- [ ] `ClassMembership` with enrollment constraints
- [ ] Bruno collection: classrooms, students

## Phase 3 — Representatives
- [ ] `Representative` assignment by advisor
- [ ] Automatic User account creation with temporary password email
- [ ] Bruno collection: representatives

## Phase 4 — Attendance
- [ ] `Attendance` and `AttendanceRecord` models
- [ ] Submission flow with week/day validation rules
- [ ] Advisor real-time view
- [ ] Bruno collection: attendance

## Phase 5 — Observations
- [ ] `Observation` creation by representatives
- [ ] Advisor review flow (`is_reviewed`)
- [ ] Bruno collection: observations

## Phase 6 — Notifications
- [ ] Django Channels setup (WebSocket)
- [ ] Real-time notifications to advisors on attendance submission and new observations

## Phase 7 — Advisor Features
- [ ] `AdvisorNote` (private notes)
- [ ] Email sending to individual students or entire classrooms
- [ ] Bruno collection: advisor

## Phase 8 — Frontend
- [ ] Vue 3 + Vite project scaffold
- [ ] Authentication views (login, first login, forgot password)
- [ ] Advisor dashboard and all advisor features
- [ ] Representative attendance and observation views

## Backlog (not scheduled)
- [ ] LGPD compliance (data access, anonymization)
- [ ] Email log
- [ ] Attendance editing with justification
- [ ] Dashboard KPIs for advisors
- [ ] Reports and data export
