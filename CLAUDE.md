# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Tarrot

A Shamanic astrology application rooted in Turkic and Central Asian cosmological tradition. Built as a **Modular Monolith** using **Python 3.13** and **FastAPI**.

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
pytest

# Run a single test
pytest tests/path/to/test_file.py::test_function_name -v

# Lint and format
ruff check .
ruff format .

# Type check
mypy .
```

---

## Architecture

**Modular Monolith** — modules enforce domain boundaries but share a single process and database connection.

```
api/v1/           ← FastAPI versioned routers and request/response schemas
core/             ← Config, database session factory, shared middleware
services/
  astronomy/      ← Deterministic Swiss Ephemeris calculations (sole source of astronomical truth)
  ai_persona/     ← LLM interpretive layer (Claude API); reads chart data, never computes it
  rituals/        ← Ritual timing and ceremonial calendar derived from pre-computed astronomy data
models/           ← SQLAlchemy ORM models and Pydantic schemas
tests/            ← pytest suites mirroring the above structure
```

**Data flow:** HTTP request → `api/v1/` router → service layer → (Swiss Ephemeris OR LLM) → Pydantic response

**Database:** Supabase/PostgreSQL. Row-Level Security (RLS) is enforced at the PostgreSQL level for all `birth_profiles` rows. Never use the Supabase service-role key in user-facing code paths; always use the anon/user-scoped key so RLS applies.

---

## Mandatory Terminology

These are non-negotiable across all code, comments, docstrings, and logs:

| Forbidden | Required | Notes |
|-----------|----------|-------|
| Planet | **Yultuz** | Turkic for "star"; used for all planetary bodies |
| Mercury | **Arzu Tilek** | |
| Venus | **Altun Yultuz** | Turkic for "golden star" |
| Sun | **Kun** | |
| Moon | **Ay** | |

Use Shamanic and Turkic metaphors in docstrings and logic comments — e.g., *"the sky-reader"*, *"the great wheel"*, *"the ancestral path"*, *"the steppe oracle"*.

---

## Deterministic Layer Rule

**Swiss Ephemeris is the only permitted source for astronomical calculations.** The LLM must never estimate, approximate, or compute:
- Yultuz (planet) positions or longitudes
- House cusps
- Aspect angles or orbs
- Any degree/minute astronomical value

All such values originate in `services/astronomy/ephemeris.py` and are passed as pre-computed data into `services/ai_persona/` and `services/rituals/`.

---

## Turkic 12-Animal Cycle

The canonical formula for deriving the Turkic calendar animal from a birth year:

```python
def turkic_animal_index(year: int) -> int:
    return (year - 3) % 12
```

Animal order (index 0–11): Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Sheep, Monkey, Rooster, Dog, Pig.

This formula lives in `services/astronomy/ephemeris.py` and must not be reimplemented elsewhere.
