# Requirements

## Users & Roles

Three distinct roles exist in the system — no overlap between them.

### Admin
- Manages platform users: creates advisors, activates and deactivates accounts
- Does not access school data (classrooms, attendance, observations)
- First admin is bootstrapped via Django admin

### Advisor
- Manages classrooms and students
- Monitors attendance and observations across all classrooms in real time
- Sends emails to students
- Writes private personal notes
- Receives real-time notifications for submitted attendance and new observations
- Cannot deactivate another advisor — only the admin manages user accounts
- Each advisor's notes are private and not visible to others
- Multiple advisors are allowed; all share the same access level

### Representative
- Is a student with system access
- Each classroom has exactly 2 representatives
- Cannot be representative of more than one active classroom simultaneously
- Both representatives have identical permissions within their classroom
- When removed from the role, the associated User account is deactivated

### Representative access creation
- The advisor selects representatives from the classroom's student list
- The system creates a User account and sends a temporary password to the student's institutional email
- The student must change their password on first login

---

## Authentication

- Login via email or username + password
- JWT: access token expires in 1 hour, refresh token expires in 7 days
- Forgot password flow available
- First login forces password change (`force_password_change = true`)

---

## Classrooms

- Fields: name, description, status, start_date, end_date
- Status values: `active`, `closed`
- Transition `active → closed` is irreversible — a closed classroom cannot be reopened
- All data (attendance, observations) remains accessible after a classroom is closed
- No new attendance can be submitted for a closed classroom
- Students are added via spreadsheet upload (name + email) or individually

---

## Students

- A student cannot be enrolled in more than one active classroom simultaneously

---

## Attendance

### Filling rules
- One `Attendance` record per classroom per day
- A representative can fill attendance for any day of the current week, up to and including today
- Future days and past weeks cannot be filled

### Submission
- The representative selects statuses for all students and clicks "Submit"
- Submission locks the attendance (`status = submitted`) — editing is not supported
- Either representative can submit; the attendance service validates that it has not already been submitted
- If no attendance is submitted for a day, it is simply not recorded — calculations are based only on submitted records

### Student statuses
- `present`
- `absent`
- `justified_absence` — requires a justification text
- `arrival_time` (nullable) — filled if the student arrived late
- `departure_time` (nullable) — filled if the student left early
- `arrival_time` and `departure_time` can both be filled on the same day

---

## Observations

- Exclusive to representatives — advisors cannot create observations
- Always tied to a specific student
- Categories: `behavior`, `health`, `conflict`, `performance`, `other`
- Cannot be edited or deleted after creation
- The advisor can mark an observation as reviewed (`is_reviewed`, `reviewed_by`, `reviewed_at`)

---

## Advisor Notes

- Exclusive to advisors
- Completely free text, no categories
- Private: each advisor sees only their own notes

---

## Notifications

- Delivered in real time via WebSocket to all active advisors
- Triggers:
  - Attendance submitted
  - Observation created
- Stored indefinitely with an `is_read` flag

---

## Email

- The advisor can send free-form emails (subject + body)
- Recipients: individual student or an entire classroom
- No email log for now

---

## Data & Audit

- **Soft delete**: nothing is hard deleted — all models have `deleted_at`
- **Data retention**: 5 years
- **Audit fields on all records**: `created_at`, `updated_at`, `created_by`, `updated_by`
