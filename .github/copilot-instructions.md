---
applyTo: "**"
---

# GitHub Copilot Instructions — concept2scene

## Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI with async route handlers
- **Validation:** Pydantic v2
- **LLM:** litellm (multi-provider abstraction)
- **Testing:** pytest + pytest-mock + httpx
- **Linting:** ruff (line length 100, rules: I + E + F + B)
- **Types:** mypy strict mode
- **Dependencies:** managed with `uv`

## Coding Conventions

- Always use `async def` for FastAPI route functions
- Use Python 3.10+ union syntax: `str | None`, not `Optional[str]`
- All functions must have full type annotations including return types
- Pydantic v2 validators use `@field_validator` and `@model_validator`, not `@validator`
- Use `from __future__ import annotations` in all files for deferred evaluation
- Settings loaded via `get_settings()` from `src/api/config.py` — never `os.environ` directly
- LLM calls go through `src/llm/client.py` only — never import `openai`/`anthropic` directly
- Use `uuid.UUID` type for IDs, not plain strings
- Use `datetime` with timezone: `datetime.now(UTC)` not `datetime.utcnow()`

## File Structure Rules

- Route handlers in `src/api/routes/` contain HTTP logic only (request parsing, response shaping)
- Business logic lives exclusively in `src/core/`
- `src/models/` contains only Pydantic schemas — no methods with side effects
- `src/utils/` contains pure, stateless functions

## Testing Conventions

- Write tests BEFORE implementing features (red/green TDD)
- Mock LLM calls in ALL tests — no real API calls
- Unit tests: mock at the `LLMClient` level using `pytest-mock`
- Integration tests: use `TestClient` or `httpx.AsyncClient` with app
- Test file mirrors source: `tests/unit/test_generator.py` ↔ `src/core/generator.py`
- Use descriptive test names: `test_generate_scene_returns_formatted_slugline_for_drama_genre`

## Do Not

- Do NOT refactor working code unless explicitly asked
- Do NOT remove existing tests even if they seem redundant
- Do NOT add `# type: ignore` without an explanatory comment on the same line
- Do NOT hardcode model names — always use `settings.MODEL_NAME`
- Do NOT log request bodies that may contain user content without redaction
- Do NOT commit `.env` files — `.env.example` only
- Do NOT use synchronous `litellm.completion` in FastAPI route handlers — use `acompletion`
