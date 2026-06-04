# ADR 002 — UUID v7 as Primary Keys

## Status
Accepted

## Context
Primary keys must be globally unique and suitable for a multi-tenant system where records may eventually be referenced across contexts. Auto-increment integers expose sequential IDs and perform poorly in distributed scenarios. UUID v4 is random, causing B-tree index fragmentation on large tables.

## Decision
Use UUID v7 for all primary keys. UUID v7 is time-ordered (monotonically increasing), which maintains B-tree index locality and allows chronological sorting by ID. It is available natively in Python 3.13+ via `uuid.uuid7()`.

## Consequences
- Better database index performance compared to UUID v4
- IDs are sortable by creation time without an extra `created_at` sort
- IDs are opaque — no sequential enumeration risk
- Requires Python 3.13+ (already the minimum version for this project)
