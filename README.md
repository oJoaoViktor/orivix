# Orivix

> Digitalize attendance sheets and student observations for vocational school classes.

## Status

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
[![CI](https://github.com/oJoaoViktor/orivix/actions/workflows/ci.yml/badge.svg)](https://github.com/oJoaoViktor/orivix/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=oJoaoViktor_orivix&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=oJoaoViktor_orivix)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=oJoaoViktor_orivix&metric=coverage)](https://sonarcloud.io/summary/new_code?id=oJoaoViktor_orivix)

## Requirements

- Python 3.13+
- PostgreSQL 17+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
# Install dependencies
uv sync

# Copy and fill environment variables
cp .env.example .env

# Run migrations
make migrate

# Start dev server
make run
```

## Development

```bash
make test     # run tests with coverage
make lint     # check linting
make format   # format code
```

## Author

**João Viktor** — [@oJoaoViktor](https://github.com/oJoaoViktor)

## License

Copyright (c) 2026 João Viktor. All rights reserved.
Unauthorized copying, distribution or commercial use of this software is strictly prohibited.
