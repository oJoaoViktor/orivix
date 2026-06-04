# Data Model

## Public Schema

Managed by `django-tenants`. Only the admin accesses these models.

### Tenant

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `name` | string | school name |
| `schema_name` | string | unique — PostgreSQL schema identifier |
| `created_at` | datetime | |

### Domain

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `tenant` | FK → Tenant | |
| `domain` | string | e.g. `school1.orivix.com` |
| `is_primary` | bool | |

---

## Tenant Schemas

All models below exist within each tenant's isolated schema.

---

### BaseModel (abstract)

All tenant models extend `BaseModel` unless stated otherwise.

| Field | Type | Notes |
|---|---|---|
| `created_at` | datetime | |
| `updated_at` | datetime | |
| `created_by` | FK → User | nullable (no user on bootstrap) |
| `updated_by` | FK → User | nullable |
| `deleted_at` | datetime | nullable — soft delete |

---

## accounts

### User
Extends `BaseModel` without `deleted_at` — uses `is_active` for deactivation.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `email` | string | unique |
| `username` | string | unique |
| `password` | string | hashed |
| `role` | ENUM | `admin`, `advisor`, `representative` |
| `is_active` | bool | |
| `force_password_change` | bool | `true` on first access |

---

## classrooms

### Classroom

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `name` | string | |
| `description` | string | nullable |
| `status` | ENUM | `active`, `closed` |
| `start_date` | date | |
| `end_date` | date | nullable |

---

## students

### Student

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `name` | string | |
| `email` | string | unique |

### ClassMembership

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `student` | FK → Student | |
| `classroom` | FK → Classroom | |

**Constraint**: a student cannot have more than one `ClassMembership` in classrooms with `status = active`.

### Representative

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `user` | FK → User | |
| `student` | FK → Student | |
| `classroom` | FK → Classroom | |

**Constraints**:
- Maximum 2 active representatives per classroom
- A student cannot be representative of more than one active classroom

---

## attendance

### Attendance

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `classroom` | FK → Classroom | |
| `representative` | FK → User | |
| `date` | date | |
| `status` | ENUM | `draft`, `submitted` |
| `submitted_at` | datetime | nullable |

**Constraint**: one `Attendance` per classroom per date.

### AttendanceRecord

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `attendance` | FK → Attendance | |
| `student` | FK → Student | |
| `status` | ENUM | `present`, `absent`, `justified_absence` |
| `justification` | text | nullable — required when `status = justified_absence` |
| `arrival_time` | time | nullable — filled if student arrived late |
| `departure_time` | time | nullable — filled if student left early |

**Constraint**: one `AttendanceRecord` per student per `Attendance`.

---

## observations

### Observation

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `classroom` | FK → Classroom | |
| `student` | FK → Student | |
| `representative` | FK → User | |
| `category` | ENUM | `behavior`, `health`, `conflict`, `performance`, `other` |
| `description` | text | |
| `is_reviewed` | bool | default `false` |
| `reviewed_by` | FK → User | nullable |
| `reviewed_at` | datetime | nullable |

---

## advisor

### AdvisorNote

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `advisor` | FK → User | |
| `content` | text | |

---

## notifications

### Notification
Does not extend `BaseModel` — immutable record.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID v7 | |
| `recipient` | FK → User | |
| `type` | ENUM | `attendance_submitted`, `observation_created` |
| `related_id` | UUID v7 | id of the related object |
| `is_read` | bool | default `false` |
| `created_at` | datetime | |
