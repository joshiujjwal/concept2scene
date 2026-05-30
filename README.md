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

---

## 🚀 Improvement Proposals

### First-Principles Analysis

- **The core value is conquering the blank page, not finishing the script.** Screenwriters don't need AI to write their story — they need a fast, low-stakes starting point. The output quality bar is "good enough to react to," not "good enough to shoot."
- **LLM-generated scripts have a homogeneous voice.** Without style controls, every generated scene will sound like a mid-budget drama; this makes the tool useful once but boring on repeated use.
- **The `refine` endpoint is the most important endpoint.** Creative work is iterative; the generate → feedback → refine loop is where real value is created, and it needs more design attention than the initial generation.
- **There is no state continuity.** Each scene generation is stateless; a feature film needs scene-to-scene character and tone consistency that a single-endpoint API cannot provide.

### Key Risks & Assumptions

- **Input specificity variance:** abstract inputs ("loneliness") produce wildly different quality than specific inputs ("a soldier returning home to find his town changed"); no guidance or prompt engineering exists to help users get better inputs.
- **Output format correctness:** screenplay format has strict conventions (slug lines, action blocks, parentheticals) — a single formatting error makes the output look amateurish to professionals.
- **LLM cost per generation:** a polished scene may require 1,000–2,000 output tokens; at scale or with heavy refinement loops, API costs can be significant.
- **No export path:** the API returns markdown/text, but screenwriters need Final Draft (.fdx), PDF, or at minimum proper Fountain format.

### Concrete Improvement Ideas

1. **Add genre and tone presets** (noir, psychological thriller, romantic comedy, Tarantino-esque) as a required or optional request parameter; presets inject style constraints into the prompt and dramatically increase output variety and quality. (Highest impact on reuse and delight.)
2. **Implement a character registry for multi-scene projects** — let users define characters (name, voice, backstory) that persist across multiple `generate` and `refine` calls, enabling consistent character voice across a script.
3. **Add Fountain format export** — Fountain is the plain-text screenwriting standard; outputting valid Fountain means the scene can be imported into Final Draft, Highland, or Fade In immediately.
4. **Build a web UI with a split-pane editor** — left pane shows the generated scene in formatted screenplay style, right pane has a feedback input and a "refine" button; this is the natural UX for iterative creative work and removes the need for curl/API clients.
5. **Add input quality guidance** — analyze the concept input before generation and return a short "your concept is very abstract — consider adding [character, conflict, setting]" prompt to help users get better outputs.

