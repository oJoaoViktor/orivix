# ADR 003 — Multi-tenancy via PostgreSQL Schemas

## Status
Accepted

## Context
Orivix may be sold to multiple schools. Each school's data must be fully isolated — advisors and representatives of one school must never access data from another. Two common approaches exist: shared schema with a `tenant_id` column on every table, or separate PostgreSQL schema per tenant.

## Decision
Use a separate PostgreSQL schema per tenant, managed by `django-tenants`. Each school gets its own schema. The request is routed to the correct schema automatically based on the subdomain (e.g. `school1.orivix.com`).

A public schema holds only `Tenant` and `Domain` models, accessible only by the platform admin.

## Consequences
- True data isolation at the database level — no risk of cross-tenant data leakage
- No `tenant_id` column needed on any model — queries are never polluted with tenant filters
- Adding a new tenant means creating a new schema and running migrations on it
- `django-tenants` handles schema switching transparently per request
- Each tenant subdomain must be configured in DNS
