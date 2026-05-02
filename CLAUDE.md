# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the development server
uv run uvicorn app.main:app --reload

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_appointments.py

# Run a single test by name
uv run pytest tests/test_appointments.py::test_create_appointment

# Run tests with coverage report
uv run pytest --cov=app --cov-report=term-missing
```

Tests require a minimum of **80% coverage**. Always verify coverage when adding or modifying features.

## Architecture

This is a FastAPI + SQLAlchemy CRUD API for managing appointments, backed by SQLite.

**Request flow:** HTTP request → router (`app/routers/`) → CRUD function (`app/crud/`) → SQLAlchemy ORM → SQLite (`appointments.db`)

### Key layers

- **`app/main.py`** — FastAPI app creation, database table auto-creation on startup, router registration.
- **`app/database.py`** — SQLAlchemy engine, `SessionLocal` factory, `DeclarativeBase`, and the `get_db()` FastAPI dependency that provides a scoped session per request.
- **`app/models/`** — SQLAlchemy ORM models. `AppointmentStatus` is a string-backed Python enum mapped to the DB.
- **`app/schemas/`** — Pydantic v2 schemas. `AppointmentCreate` for POST, `AppointmentUpdate` for PATCH (all fields optional), `AppointmentResponse` for output. All use `model_config = ConfigDict(from_attributes=True)` for ORM compatibility.
- **`app/crud/`** — Plain functions that accept a `db: Session` and a schema; they never touch HTTP concerns. `update_appointment` uses `exclude_unset=True` for true partial updates.
- **`app/routers/`** — FastAPI routers. All appointment endpoints live under the `/appointments` prefix.

### Testing approach

Use `httpx.AsyncClient` with a FastAPI `TestClient` (or override the `get_db` dependency) to test endpoints. Keep a separate in-memory SQLite database for tests so they never touch `appointments.db`.
