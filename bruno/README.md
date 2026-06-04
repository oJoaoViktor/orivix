# Bruno Collections

API requests organized by domain. Each collection is updated after the corresponding feature is completed.

## Structure

```
bruno/
├── accounts/       # authentication, password flows
├── classrooms/     # classroom CRUD
├── students/       # student CRUD, enrollment, representatives
├── attendance/     # attendance submission and queries
├── observations/   # observation creation and review
├── advisor/        # advisor notes, email sending
└── notifications/  # notification listing and read status
```

## Setup

1. Open Bruno
2. Open collection from this folder
3. Set the `baseUrl` environment variable to your local server (e.g. `http://school1.localhost:8000`)
