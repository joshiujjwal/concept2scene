# concept2scene — Feature Specification

**Version:** 0.1.0-draft  
**Status:** Pre-implementation  
**Last updated:** Phase 0

---

## 1. Overview

### Problem Statement

Screenwriters and filmmakers often have abstract concepts — themes, emotions, philosophical ideas, or raw images — but face a blank page when translating these into concrete scene work. The ideation-to-draft gap is slow and creatively expensive.

### Solution

`concept2scene` takes a free-text concept as input and generates a complete, formatted screenplay scene using an LLM. The output follows standard screenplay format (slugline, action lines, dialogue, parentheticals) and includes optional director's notes covering suggested camera work, lighting, and sound design.

### Target Users

- Screenwriters needing a fast first draft or creative unblock
- Filmmakers sketching visual concepts
- Creatives using scenes as writing prompts
- AI/LLM developers building creative tooling

---

## 2. Functional Requirements

### Core Generation
- [ ] Accept a free-text `concept` (1–2000 characters) as the primary input
- [ ] Accept optional `genre` (THRILLER | DRAMA | COMEDY | SCI_FI | HORROR | ROMANCE | DEFAULT)
- [ ] Accept optional `tone` override as free text (e.g., "melancholic", "tense", "whimsical")
- [ ] Accept optional `length` (SHORT ~1 page | MEDIUM ~2–3 pages | LONG ~5+ pages)
- [ ] Return a structured `SceneResponse` with scene text in standard screenplay format
- [ ] Return scene ID (UUID) with each response for future retrieval/refinement

### Scene Format
- [ ] Scene must begin with a proper slugline: `INT. / EXT. LOCATION — DAY/NIGHT`
- [ ] Include action/description blocks in present tense
- [ ] Include at least one character with dialogue (unless concept implies no dialogue)
- [ ] Include parentheticals where needed for performance direction
- [ ] Optionally include a `DIRECTOR'S NOTES` block at the end (camera, lighting, sound)

### Refinement
- [ ] Accept a `scene_id` + `feedback` string to refine an existing scene
- [ ] Preserve original concept intent while applying feedback (tone, pacing, dialogue changes)
- [ ] Track `version` number on each refinement

### Retrieval
- [ ] Retrieve a generated scene by its UUID
- [ ] Return 404 for unknown IDs with a clear error message

### Batch Generation
- [ ] Accept up to 5 concepts in a single batch request
- [ ] Return array of `SceneResponse` objects, one per concept
- [ ] Reject batches of 6+ with 422

---

## 3. Non-Functional Requirements

- [ ] P95 response time < 30s for MEDIUM scenes (LLM latency dominated)
- [ ] API returns structured JSON error bodies on all 4xx/5xx responses
- [ ] No secrets (API keys) logged or returned in responses
- [ ] Rate limiting: 10 requests/min per IP
- [ ] All endpoints covered by automated tests
- [ ] Code passes ruff lint and mypy strict type checking

---

## 4. Data Model

### `ConceptRequest`

```python
class ConceptRequest(BaseModel):
    concept: str                         # Required. 1–2000 chars.
    genre: Genre = Genre.DEFAULT         # Optional. Enum.
    tone: str | None = None              # Optional. Free text. Max 100 chars.
    length: SceneLength = SceneLength.MEDIUM
    include_directors_notes: bool = True
```

### `SceneResponse`

```python
class SceneResponse(BaseModel):
    id: UUID
    concept: str                         # Original input concept
    scene_text: str                      # Formatted screenplay scene
    directors_notes: str | None          # Optional director's notes block
    genre: Genre
    tone: str | None
    length: SceneLength
    version: int                         # 1 = original, 2+ = refined
    model_used: str                      # e.g. "gpt-4o"
    created_at: datetime
    updated_at: datetime
```

### `RefineRequest`

```python
class RefineRequest(BaseModel):
    scene_id: UUID
    feedback: str                        # 1–1000 chars. Natural language direction.
```

### `BatchConceptRequest`

```python
class BatchConceptRequest(BaseModel):
    concepts: list[ConceptRequest]       # Min 1, max 5
```

### Enums

```python
class Genre(str, Enum):
    DEFAULT = "default"
    THRILLER = "thriller"
    DRAMA = "drama"
    COMEDY = "comedy"
    SCI_FI = "sci_fi"
    HORROR = "horror"
    ROMANCE = "romance"

class SceneLength(str, Enum):
    SHORT = "short"    # ~600 tokens target
    MEDIUM = "medium"  # ~1200 tokens target
    LONG = "long"      # ~2400 tokens target
```

---

## 5. API Design

### `POST /api/v1/scenes/generate`

**Request body:** `ConceptRequest`  
**Response:** `SceneResponse` (201)  
**Errors:** 422 (validation), 503 (LLM unavailable), 500 (unexpected)

```json
// Request
{
  "concept": "The moment a lighthouse keeper realizes the ships have stopped coming",
  "genre": "drama",
  "length": "medium",
  "include_directors_notes": true
}

// Response
{
  "id": "3f2a1b4c-...",
  "concept": "The moment a lighthouse keeper...",
  "scene_text": "INT. LIGHTHOUSE KEEPER'S LOG ROOM — NIGHT\n\n...",
  "directors_notes": "CAMERA: Open on tight close-up...",
  "genre": "drama",
  "tone": null,
  "length": "medium",
  "version": 1,
  "model_used": "gpt-4o",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### `GET /api/v1/scenes/{id}`

**Response:** `SceneResponse` (200)  
**Errors:** 404 (not found)

### `POST /api/v1/scenes/refine`

**Request body:** `RefineRequest`  
**Response:** `SceneResponse` (200) — updated scene, version incremented  
**Errors:** 404 (scene not found), 422 (validation)

### `POST /api/v1/scenes/batch`

**Request body:** `BatchConceptRequest`  
**Response:** `list[SceneResponse]` (201)  
**Errors:** 422 (too many concepts or validation failure)

### `GET /health`

**Response:** `{"status": "ok", "model": "gpt-4o", "version": "0.1.0"}` (200)

---

## 6. Prompt Design

### System Prompt Template

```
You are an expert Hollywood screenwriter with credits across {genre} films.
Your task is to write a single, complete movie scene based on the concept provided.

Follow these rules:
- Use standard screenplay format (slugline, action lines, dialogue)
- Write in present tense
- The scene should feel like it belongs in a {genre} feature film
- Tone: {tone_instruction}
- Target length: {length_instruction}
- Action lines should be visual and specific — write for the camera
- Dialogue should feel natural and subtext-rich — avoid on-the-nose lines
- End with a clear scene out (action, cut, or emotional beat)

{directors_notes_instruction}
```

### Tone Instructions by Genre

| Genre | Default Tone Instruction |
|---|---|
| THRILLER | Tense, paranoid, every detail feels loaded with threat |
| DRAMA | Emotionally grounded, quiet intensity, truth in subtext |
| COMEDY | Timing-aware, absurdist or dry, character flaws drive humor |
| SCI_FI | Conceptually bold, visual wonder, human stakes inside big ideas |
| HORROR | Dread builds slowly, mundane details made sinister |
| ROMANCE | Longing in restraint, charged silences, emotional vulnerability |
| DEFAULT | Cinematic and character-driven, let the concept determine tone |

---

## 7. Test Plan

### Unit Tests

| Module | Test Cases |
|---|---|
| `models/` | Empty concept rejected, concept >2000 chars rejected, genre enum coerced, invalid genre raises error |
| `utils/formatter.py` | Slugline correctly formatted, action blocks separated by blank line, character names uppercased, dialogue indented |
| `core/prompt_builder.py` | Genre maps to correct tone instruction, length maps to token target, tone override replaces genre default, directors_notes flag toggles instruction block |
| `llm/client.py` | Successful completion returned, timeout raises `LLMTimeoutError`, API error raises `LLMError`, retry logic fires on 503 |
| `core/generator.py` | Happy path returns `SceneResponse`, LLM error propagates correctly, formatter called with LLM output |
| `core/store.py` | Store and retrieve by UUID, missing key raises `SceneNotFoundError` |

### Integration Tests

| Endpoint | Test Cases |
|---|---|
| `POST /generate` | Valid request → 201 + SceneResponse, empty concept → 422, missing body → 422, LLM mock returns scene |
| `GET /{id}` | Known ID → 200, unknown ID → 404 |
| `POST /refine` | Valid refinement → 200 + version=2, unknown scene_id → 404 |
| `POST /batch` | 2 concepts → 201 + list of 2, 6 concepts → 422 |
| `GET /health` | → 200 + status ok |

### Edge Cases

- Concept that is a single word ("loneliness")
- Concept that is already a scene description (should still wrap in format)
- Very long concept (2000 chars) — verify truncation or handling
- LLM returns incomplete scene (no slugline) — formatter must handle gracefully
- Concurrent requests — no shared mutable state issues

---

## 8. Open Questions

- [ ] **Persistence:** For v0.1, in-memory store only. Should we add Redis or SQLite for v0.2?
- [ ] **Model selection:** Default to `gpt-4o` or `claude-3-5-sonnet`? Make it configurable?
- [ ] **Screenplay format strictness:** Should we validate that output is properly formatted or just pass through?
- [ ] **Copyright:** Do we need to add usage terms preventing commercial use without review?
- [ ] **Streaming:** Worth adding SSE streaming in v0.1 or park for v0.2?
- [ ] **Frontend:** Ship API-only first, or include a minimal HTML form for demos?
