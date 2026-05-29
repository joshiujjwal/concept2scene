# concept2scene — Task Breakdown

## How to Use This File

Workflow per task:
1. Write tests FIRST — red phase (failing tests define the contract)
2. Implement until tests pass — green phase
3. Review the diff manually before committing
4. Commit with a descriptive message referencing the task
5. If you discover something non-obvious, add it to `CLAUDE.md` → compound loop

---

## Phase 0: Foundation ⬜

- [ ] Initialize `pyproject.toml` with `uv` — add fastapi, pydantic, litellm, httpx, pytest, ruff, mypy
- [ ] Configure `ruff` (line length 100, enable I + E + F rules) and `mypy` (strict mode)
- [ ] Create `.env.example` with `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `MODEL_NAME`, `LOG_LEVEL`
- [ ] Write smoke test: `tests/unit/test_smoke.py` — assert `1 == 1`, confirm pytest runs
- [ ] GitHub Actions CI: `.github/workflows/ci.yml` — lint (ruff), type-check (mypy), test (pytest)
- [ ] Review all AI config files (CLAUDE.md, AGENTS.md, copilot-instructions.md) before first real commit

**Gate:** CI passes on first push. All checks green.

---

## Phase 1: Core Scene Generation ⬜

- [ ] Define Pydantic models: `ConceptRequest` (concept: str, genre: str?, tone: str?, length: SceneLength), `SceneResponse` (id, concept, scene_text, metadata, created_at)
  - Write model validation tests first: empty concept rejected, genre enum validated
- [ ] Build LLM client wrapper in `src/llm/client.py` — thin litellm wrapper with retry logic
  - Write unit tests with mocked `litellm.completion` calls
- [ ] Build `ScreenplayFormatter` in `src/utils/formatter.py` — converts raw LLM text to formatted screenplay (INT./EXT., sluglines, action blocks, character cues, dialogue)
  - Write unit tests for each formatting rule with fixture strings
- [ ] Build `ScenePromptBuilder` in `src/core/prompt_builder.py` — constructs system + user prompt from `ConceptRequest`
  - Write unit tests: verify prompt contains concept, genre affects tone instruction, length maps to word target
- [ ] Build `SceneGenerator` in `src/core/generator.py` — orchestrates prompt → LLM → formatter → `SceneResponse`
  - Write unit tests with mocked LLM client
- [ ] Create `POST /api/v1/scenes/generate` endpoint
  - Write integration tests: valid request returns 200 + SceneResponse, empty concept returns 422
- [ ] Manual test: `curl -X POST .../generate -d '{"concept": "the silence after a goodbye"}'` — capture output as evidence

**Gate:** All unit + integration tests pass. Manual curl evidence committed to PR.

---

## Phase 2: Scene Refinement & Retrieval ⬜

- [ ] Add in-memory scene store (`src/core/store.py`) — dict keyed by UUID, stores `SceneResponse`
  - Write unit tests: store/retrieve/missing key
- [ ] Create `GET /api/v1/scenes/{id}` endpoint
  - Write integration tests: known ID returns 200, unknown returns 404
- [ ] Build `SceneRefiner` in `src/core/refiner.py` — takes `SceneResponse` + feedback string, re-prompts LLM to adjust tone/dialogue/pacing
  - Write unit tests with mocked LLM
- [ ] Create `POST /api/v1/scenes/refine` endpoint (body: `scene_id`, `feedback`)
  - Write integration tests: valid refinement updates scene, returns new version
- [ ] Add `version` field to `SceneResponse` — increment on each refinement
- [ ] Manual test full loop: generate → retrieve → refine → verify diff — capture as evidence

**Gate:** All tests pass. Retrieval and refinement verified with curl evidence.

---

## Phase 3: Quality & Configurability ⬜

- [ ] Add genre presets: THRILLER, DRAMA, COMEDY, SCI_FI, HORROR, ROMANCE — each maps to tone adjectives and pacing guidance in prompts
  - Write unit tests: each genre generates a distinct system prompt slice
- [ ] Add `SceneLength` enum: SHORT (1 page), MEDIUM (2–3 pages), LONG (5+ pages) — maps to LLM token targets
  - Write unit tests: length enum maps to expected max_tokens
- [ ] Add structured director's notes block to output — separated section with camera angles, lighting mood, sound design hints
  - Write formatter unit tests for director's notes extraction
- [ ] Add `POST /api/v1/scenes/batch` — accepts list of concepts (max 5), returns list of scenes
  - Write integration tests: batch of 2 returns 2 scenes, batch of 6 returns 422
- [ ] Add request ID middleware + structured JSON logging (no secrets in logs)
- [ ] Manual test with 3 varied concepts — verify genre and length differences in output

**Gate:** All tests pass. Genre and length variations verified with side-by-side output evidence.

---

## Phase 4: Polish & Harden ⬜

- [ ] Add rate limiting middleware (slowapi) — 10 req/min per IP
  - Write integration test: 11th request in 60s returns 429
- [ ] Add async support to LLM client — use `litellm.acompletion`
  - Confirm no blocking I/O in request path
- [ ] Write `docs/adr/0002-litellm-for-llm-abstraction.md` — document why litellm over direct SDK
- [ ] Add `/health` endpoint with model availability ping
  - Write integration test: health returns 200 with model status
- [ ] Error handling hardening: LLM timeout → 503, LLM refusal → 422 with user message, malformed LLM output → retry once then 500
  - Write unit tests for each error branch
- [ ] Final review: remove all TODO stubs, confirm no secrets in code, run full test suite

**Gate:** All tests pass. Rate limiting verified. No unhandled exceptions in happy + error paths.

---

## Phase 5: Ship ⬜

- [ ] Write `Dockerfile` — multi-stage build, non-root user, health check
- [ ] Write `docker-compose.yml` for local dev
- [ ] Add `README.md` deployment section (Docker, env vars, port mapping)
- [ ] Tag `v0.1.0` and create GitHub Release with changelog
- [ ] Deploy to target (Railway / Fly.io / TODO: decide)

**Gate:** Docker build passes. Container starts, health check responds, generate endpoint works.

---

## Parking Lot 🅿️

- Streaming response support (`text/event-stream`) for real-time scene generation
- Scene export to Final Draft `.fdx` format
- Web UI (React) — separate repo or Next.js in `frontend/`
- Fine-tuned model on actual screenplays (WGA-cleared corpus)
- Webhook support: async generation + callback URL
- Scene comparison view: side-by-side original vs refined
- User accounts + scene history persistence (PostgreSQL)

---

## Lessons Learned 📝

> Add discoveries here as you build — non-obvious gotchas, LLM quirks, FastAPI conventions.
> This section is the compound loop: every session should add at least one entry if something surprised you.

- (none yet — first session)
