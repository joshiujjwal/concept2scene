# AGENTS.md — concept2scene

AI coding agent instructions for this repository.

## Setup

```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies
uv sync

# Set up environment
cp .env.example .env
# Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env
```

## Running the Service

```bash
uv run fastapi dev src/api/main.py   # Dev (hot reload, port 8000)
uv run fastapi run src/api/main.py   # Prod
```

## Testing

**Always run tests before making changes:**

```bash
uv run pytest                              # All tests
uv run pytest tests/unit/ -v              # Unit tests only
uv run pytest tests/integration/ -v       # Integration tests only
uv run pytest --cov=src -q                # With coverage
```

**Test rules:**
- Write failing tests FIRST (red), then implement (green)
- All LLM calls must be mocked — use `pytest-mock` or `unittest.mock`
- Integration tests use FastAPI `TestClient` or `httpx.AsyncClient`
- Test filenames: `test_<module>.py` mirroring `src/` structure
- Never test implementation details — test behavior and contracts

## Code Style

**Stack:** Python 3.12+, FastAPI, Pydantic v2, litellm, uv

```bash
uv run ruff check src/ tests/    # Lint
uv run ruff format src/ tests/   # Format
uv run mypy src/                 # Type check (strict)
```

**Rules:**
- Line length: 100 characters
- All functions must have type annotations
- Use `str | None` not `Optional[str]` (Python 3.10+ union syntax)
- Pydantic models use `model_validator` and `field_validator`, not `@validator`
- FastAPI route functions must be `async def`
- No bare `except:` — always catch specific exceptions
- Never `import openai` or `import anthropic` directly — always go through `src/llm/client.py`
- Settings from `src/api/config.py` via `get_settings()`, never `os.environ` directly

## Architecture Rules

- `src/api/routes/` — HTTP layer only; no business logic in route handlers
- `src/core/` — All business logic; no FastAPI imports here
- `src/llm/` — LLM abstraction only; no prompt construction here
- `src/models/` — Pure Pydantic schemas; no logic
- `src/utils/` — Stateless utility functions

## PR Instructions

Every PR must include:
1. **Test evidence** — paste `pytest` output showing tests pass
2. **Lint evidence** — paste `ruff check` output (clean)
3. **Type evidence** — paste `mypy` output (no errors)
4. For API changes: **curl example** showing the endpoint working
5. Description of what changed and why

**PR checklist:**
- [ ] Tests written before implementation (TDD)
- [ ] No new `# type: ignore` without explanation comment
- [ ] No secrets, no `.env` committed
- [ ] `CLAUDE.md` updated if a non-obvious convention was discovered
- [ ] `TODO.md` tasks checked off that this PR completes

## Error Handling Contract

| Situation | HTTP Status | Response |
|---|---|---|
| Validation failure (Pydantic) | 422 | FastAPI default detail |
| Scene not found | 404 | `{"error": "scene_not_found", "id": "..."}` |
| LLM timeout | 503 | `{"error": "llm_timeout"}` |
| LLM API error | 503 | `{"error": "llm_error", "detail": "..."}` |
| Unexpected exception | 500 | `{"error": "internal_error"}` (no stack trace in prod) |
