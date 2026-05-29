# concept2scene

> Turn abstract concepts, ideas, or text descriptions into full cinematic movie scene scripts.

🚧 **Status: Early Development**

## What It Does

`concept2scene` is an AI-powered concept-to-screenplay converter. Give it an abstract idea — a theme, emotion, philosophical concept, or raw description — and it generates a polished movie scene: scene heading, action lines, dialogue, visual direction, and tone notes. Built for filmmakers, screenwriters, and creatives who want a fast creative spark.

**Input:** `"The loneliness of being the last person on earth who remembers analog photography"`
**Output:** A formatted screenplay scene with INT/EXT heading, atmosphere, character action, dialogue, and director's notes.

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python) |
| LLM Integration | OpenAI / Anthropic (via `litellm`) |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Linting | ruff + mypy |
| Dependency Mgmt | uv |
| CI | GitHub Actions |

## Getting Started

```bash
# Clone
git clone https://github.com/joshiujjwal/concept2scene.git
cd concept2scene

# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env
# Add your OPENAI_API_KEY or ANTHROPIC_API_KEY to .env

# Run dev server
uv run fastapi dev src/api/main.py

# Run tests
uv run pytest
```

## Project Structure

```
concept2scene/
├── src/
│   ├── api/          # FastAPI app, routes, middleware
│   ├── core/         # Scene generation engine, prompt logic
│   ├── llm/          # LLM client abstraction (litellm wrapper)
│   ├── models/       # Pydantic schemas (request/response)
│   └── utils/        # Helpers (formatting, validation)
├── tests/
│   ├── unit/         # Pure function tests (prompt builders, formatters)
│   └── integration/  # API endpoint tests (httpx + TestClient)
├── docs/
│   ├── spec.md       # Feature specification
│   └── adr/          # Architecture Decision Records
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
├── README.md
├── TODO.md
├── CLAUDE.md
├── AGENTS.md
└── pyproject.toml
```

## API Overview

```
POST /api/v1/scenes/generate   — Generate a scene from a concept
GET  /api/v1/scenes/{id}       — Retrieve a generated scene
POST /api/v1/scenes/refine     — Refine an existing scene with feedback
GET  /health                   — Health check
```

## Contributing

- Write failing tests **first** (red), then implement (green)
- PRs must include evidence: test output, curl example, or screenshot
- Keep PRs small and focused — one feature or fix per PR
- Update `CLAUDE.md` / `AGENTS.md` if you discover non-obvious conventions
- No unreviewed AI-generated code merged without human inspection of the diff
