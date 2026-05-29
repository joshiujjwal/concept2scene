# CLAUDE.md — concept2scene

> Context for AI coding assistants. Keep under 200 lines. Update when you discover something non-obvious.

## Project in One Line

FastAPI service that converts abstract concepts into formatted screenplay scenes via LLM.

## Commands

```bash
# Install dependencies (requires uv: https://docs.astral.sh/uv/)
uv sync

# Run dev server (hot reload)
uv run fastapi dev src/api/main.py

# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run a single test file
uv run pytest tests/unit/test_formatter.py -v

# Lint (ruff)
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Type check (mypy)
uv run mypy src/

# Run lint + types + tests in one shot
uv run ruff check src/ tests/ && uv run mypy src/ && uv run pytest
```

## Directory Map

```
src/
├── api/
│   ├── main.py          # FastAPI app factory, middleware registration, router mounts
│   ├── routes/
│   │   └── scenes.py    # All /api/v1/scenes/* route handlers
│   └── middleware.py    # Request ID injection, rate limiting setup
├── core/
│   ├── generator.py     # SceneGenerator: orchestrates prompt → LLM → format → store
│   ├── prompt_builder.py# Builds system + user prompts from ConceptRequest
│   ├── refiner.py       # SceneRefiner: re-prompts with feedback to update a scene
│   └── store.py         # In-memory scene store (UUID → SceneResponse dict)
├── llm/
│   └── client.py        # LLMClient: thin litellm wrapper with retry, timeout, error mapping
├── models/
│   ├── requests.py      # ConceptRequest, RefineRequest, BatchConceptRequest
│   ├── responses.py     # SceneResponse
│   └── enums.py         # Genre, SceneLength enums
└── utils/
    └── formatter.py     # ScreenplayFormatter: raw LLM text → proper screenplay blocks
tests/
├── unit/                # Pure function tests — mock LLM calls, no network
├── integration/         # FastAPI TestClient tests — mock LLM at the client boundary
└── conftest.py          # Shared fixtures (mock LLM, sample requests, test app)
```

## Workflow (Follow This Order Every Session)

1. **Run tests first** — `uv run pytest` — understand what's passing before touching anything
2. **Check TODO.md** — find the next unchecked task in the current phase
3. **Write failing test** — red phase; commit as `test: add failing tests for <feature>`
4. **Implement** — green phase; commit as `feat: implement <feature>`
5. **Lint + type check** — fix before committing
6. **Update this file** if you discovered something non-obvious (add to Gotchas below)

## Non-Obvious Conventions

### LLM Client (`src/llm/client.py`)
- Always use `litellm` — never import `openai` or `anthropic` directly. This keeps the model swappable.
- Model name comes from `settings.MODEL_NAME` (env var), not hardcoded.
- `litellm.completion` is synchronous; `litellm.acompletion` is async. Use async in FastAPI routes.

### Prompt Builder (`src/core/prompt_builder.py`)
- Genre → tone instruction mapping lives in `src/core/prompt_builder.py`, not in the models.
- `SceneLength` maps to `max_tokens`: SHORT=800, MEDIUM=1600, LONG=3200. Do not change without updating tests.

### Scene Store (`src/core/store.py`)
- In-memory only in v0.1 — scenes are lost on restart. This is intentional.
- Store is a module-level singleton dict. Do not import and mutate it from tests — use dependency injection fixtures.

### Screenplay Formatter (`src/utils/formatter.py`)
- The formatter trusts that the LLM outputs valid screenplay structure but normalizes whitespace and casing.
- Character names in dialogue must be uppercase. The formatter enforces this by detecting lines that precede a dialogue block.
- If the LLM doesn't include a slugline, formatter prepends `INT. UNKNOWN LOCATION — DAY`.

### Testing
- All LLM calls must be mocked in tests — never hit real APIs in CI.
- Use `pytest-mock` (`mocker` fixture) for unit tests on generator/refiner.
- Use `httpx.AsyncClient` + `app` fixture for integration tests.
- Fixtures live in `tests/conftest.py`.

### Settings
- All config via environment variables, loaded through a `Settings` class using `pydantic-settings`.
- `.env` file for local dev; never committed. `.env.example` is the reference.
- Access settings via `from src.api.config import get_settings` — not directly from `os.environ`.

## Gotchas

> Add entries here as you discover them.

- (none yet)

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | One of these | — | OpenAI API key |
| `ANTHROPIC_API_KEY` | One of these | — | Anthropic API key |
| `MODEL_NAME` | No | `gpt-4o` | LiteLLM model string |
| `LOG_LEVEL` | No | `INFO` | Python logging level |
| `RATE_LIMIT_PER_MINUTE` | No | `10` | Requests per minute per IP |
