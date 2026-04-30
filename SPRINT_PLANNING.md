# Tennis AI Platform - Sprint Planning

> **Note:** This is a living document (Agile workflow). Dates, hours, and specific technologies may be adapted as the project evolves.

## In Flight

> Long-lived feature branches not yet merged to `main`. Updated when a branch is created or merged so this file always reflects what's cooking, even if you're working on `main`. Empty when no branches are open.

- **Sprint 6 — LangGraph Agent Architecture** · branch `feature/sprint6-langgraph` · started 2026-04-26
  - ✅ Story 1: scaffold LangGraph graph (state, models, graph stubs)
  - ✅ Story 2: migrate odds + rankings nodes — live fetch nodes integrated, end-to-end smoke test passed
  - 🔄 Stories 3–7 pending — next: RAG layer (semantic chunking + FAISS). See "Sprint 6 — Detail" below for full AC breakdown.

## Phase 1: GCP Data Pipeline

| Sprint | Primary Objective | Key Tasks | Functional Deliverable | Est. Hours | Dates | Status |
|---|---|---|---|---|---|---|
| **Sprint 1** | Raw Data Ingestion (Data Lake) | 1. Set up GCP project & Service Account. 2. Write Python script to extract The-Odds-API. 3. Save raw JSONs to GCS. | `extract_odds.py`, `requirements.txt`, `.env.example` | 5–7 hrs | Fri Mar 6–Wed Mar 18 | ✅ Done (4h 30m) |
| **Sprint 2** | ETL & Data Warehousing (BigQuery) | 1. Read JSON from GCS. 2. Flatten nested structure with Pandas. 3. Load structured data into BigQuery. | `transform.py`, `etl_gcs_to_bq.py`, confirmed schema in `docs/MIAMI_OPEN_SCHEMA.md` | 8–10 hrs | Fri Mar 20–Mon Mar 23 | ✅ Done (2h 50m) |

---

## Phase 2: Prediction Engine + UI (MVP)

| Sprint | Primary Objective | Key Tasks | Functional Deliverable | Est. Hours | Dates | Status |
|---|---|---|---|---|---|---|
| **Sprint 3** | End-to-End Prediction MVP | ✓ 1. Dynamic ATP sport key discovery via `/v4/sports/`. ✓ 2. `raw_implied` + `true_implied` columns in `transform.py`. ✓ 3. `data/processed/` CSV output for local sandbox. ✓ 4. Build ranking agent (Gemini Flash + web search) — refactored to accept exact player names from odds API, eliminating name-matching ambiguity. ✓ 5. Build ranking-based probability calculator. ✓ 6. Build comparison & recommendation logic. ✓ 7. Filter in-play matches (`filter_upcoming()`) — live odds reflect score, not pre-match probability. ✓ 8. Wire into local Streamlit UI (`app.py`). | Working local demo: pipeline fetches live ATP odds, filters in-play matches, fetches rankings via Gemini, computes probabilities, displays match cards with value bet signals | 10–12 hrs | Mon Mar 23–Wed Mar 25 | ✅ Done (4h 50m) |
| **Sprint 4** | Deploy to GCP + mateogrisales.com | 1. Expose prediction pipeline as GCP Cloud Run API. 2. Build minimal React UI in Lovable. 3. Connect frontend to backend API. 4. Deploy live at mateogrisales.com. | Live public demo at [tennis.mateogrisales.com](https://tennis.mateogrisales.com) with the ranking-based model | 8–10 hrs | Thu Mar 26–Wed Apr 15 | ✅ Done (7h) |
| **Sprint 5** | UI Showcase | 1. Match card redesign — probability bars, ranking points, edge % highlighted. 2. App context layer — hero section, methodology explainer, tech stack callout, data freshness timestamp. 3. Polish & edge cases — empty/error states, disclaimer, mobile layout. | Recruiter-ready UI at tennis.mateogrisales.com that communicates the Data/AI/ML stack and model reasoning without needing a README | 8–10 hrs | Wed Apr 15–Thu Apr 16 | ✅ Done (1h 50m) |
| **Sprint 6** | LangGraph Agent Architecture + Ops | 1. Scaffold `GraphState` + `StateGraph` with conditional retry edge. 2. Migrate odds + rankings nodes into graph. 3. RAG layer: semantic chunking + FAISS vector store. 4. Structured LLM generation with citation anchors (`MatchInsight` Pydantic model). 5. Deterministic hallucination validation node (dictionary lookup, not regex). 6. Expose via versioned `POST /v2/predict` endpoint — existing `/predict` untouched. 7. Weekly cost review agent. | LangGraph coordinator with cyclic validation loop; RAG-grounded structured output; `POST /v2/predict` alongside live `/predict` | 16–23 hrs | Sun Apr 26 | 🔄 In Progress (branch `feature/sprint6-langgraph`, Story 1 done) |
| **Sprint 7** | Data Enrichment & Model Upgrade | 1. Add historical H2H data (Sackmann dataset → BigQuery). 2. Add surface/conditions features. 3. Add news/sentiment agent. 4. Upgrade ranking model to logistic regression. 5. Add `docs/ML_ENGINEER.md` agent persona. | Enriched predictions, trained baseline model — improvements go live immediately | 12–15 hrs | TBD | 📅 Planned |
| **Sprint 8** | Advanced UI & Auth | 1. Improve React UI in Lovable (match selection, visualization, recommendation display). 2. Add authentication/rate limiting to backend. 3. Leverage LangGraph checkpointing for async prediction requests. | Polished public demo at mateogrisales.com | 8–10 hrs | TBD | 📅 Planned |

---

## Sprint 4 — Detail

> **Goal:** Go live as fast as possible. A live public demo is more valuable for the portfolio than a local Streamlit app.
> **Decision:** Cloud Run over Cloud Functions — Gemini Flash API call latency + future LangGraph refactor make Cloud Run the right fit.

### Story 1 — Backend API (Cloud Run + API Gateway)
**AC-What:** A `POST /predict` request to the public API Gateway URL returns a JSON array of pre-match ATP matches with model probability, raw implied probability, and value signal for each player.
**AC-Rule:** Only pre-match matches returned — `filter_upcoming()` must be applied. Cloud Run must remain private — never exposed directly to the internet. Public access is via API Gateway only.
**AC-How-critical:** FastAPI app must return structured JSON (not HTML). Dockerfile must not copy `.env` into the image. Cloud Run requires IAM auth — `api-gateway-invoker` service account is the only invoker. `X-API-Key` auth is validated by FastAPI, not the gateway.

**Key architecture decision:** Cloud Run kept private due to `grisalogic.com` org policy (`iam.allowedPolicyMemberDomains`) blocking `allUsers` IAM binding. API Gateway fronts Cloud Run using service account `api-gateway-invoker` — the standard enterprise pattern for exposing private Cloud Run services.

- [x] Wrap pipeline logic into a FastAPI app (`api/main.py`) with a `POST /predict` endpoint
- [x] Write `Dockerfile` and validate image builds and runs locally
- [x] Build and push image to GCP Artifact Registry via Cloud Build (no local Docker needed)
- [x] Deploy Cloud Run service (private, `--no-allow-unauthenticated`, `us-central1`)
- [x] Create `api-gateway-invoker` service account with `roles/run.invoker` on the Cloud Run service
- [x] Deploy GCP API Gateway (`tennis-gateway`) with OpenAPI spec (`api-gateway.yaml`) as public-facing layer
- [x] Smoke test full chain: API Gateway → Cloud Run → prediction pipeline
- **Public gateway URL:** `https://tennis-gateway-agmlnd9p.uc.gateway.dev`
- **Cloud Run URL (private):** `https://tennis-api-er2jgzyldq-uc.a.run.app`

### Story 2 — Frontend (Lovable)
**AC-What:** A visitor to the frontend URL sees a list of current ATP pre-match matches, each with both players, their value signal (value bet / marginal / no bet), model probability, and bookmaker implied probability.
**AC-Rule:** UI must handle the case where no pre-match matches are available (show a friendly empty state, not a crash).
**AC-How-critical:** API call must include the API key in the request header — do not expose it in client-side JS as a plain string; use an environment variable in Lovable.

- [x] Design minimal UI layout: match cards, value signal badge, odds table
- [x] Scaffold React app in Lovable — clay orange (#E8650A), Roland Garros inspired, tennis ball spinner
- [x] Wire `POST /predict` API call with loading and error states
- [x] Fix CORS preflight — add `OPTIONS /predict` to `api-gateway.yaml`, deploy `tennis-api-config-v3`
- [x] Fix ranking agent — remove Google Search grounding (gemini-2.5-flash SDK incompatibility), model training data sufficient
- [x] Confirm end-to-end working in Lovable preview — Monte Carlo Masters predictions loading
- [x] Fix stale rankings — replace Gemini agent with live `atptour.com` scraper (Alcaraz now correctly #1)

### Story 3 — Integration & Go Live
**AC-What:** Visiting `tennis.mateogrisales.com` loads the React app and successfully fetches and displays live predictions.
**AC-Rule:** CORS must only allow the production frontend origin — not a wildcard `*`.
**AC-How-critical:** API key auth must be validated server-side on Cloud Run before the pipeline executes — a request without a valid key must return 401.

- [x] Configure CORS on Cloud Run to allow frontend origin — `CORS_ORIGINS` set to `https://orange-court-ai.lovable.app,https://tennis.mateogrisales.com`
- [x] Add API key auth to Cloud Run endpoint (not open to the public) — validated by FastAPI `_require_api_key` dependency
- [x] Point subdomain (`tennis.mateogrisales.com`) to Lovable frontend — DNS configured in GoDaddy, propagation pending (up to 72h)
- [x] End-to-end smoke test on production URL — `tennis.mateogrisales.com` confirmed live

### Story 4 — Hardening (Definition of Done)
**AC-What:** The deployed app is observable — errors in the prediction pipeline appear in Cloud Logging, cost overruns trigger email alerts before they grow, and the README documents the live URL and how to redeploy.
**AC-Rule:** No secrets in plain env vars anywhere in the deployed stack. No unbounded Cloud Run scaling. Budget alerts must actually reach a human via email.
**AC-How-critical:** Cloud Logging must capture unhandled exceptions from the FastAPI app, not just HTTP access logs. Budget `notificationsRule` must not be empty.

- [x] Move `TENNIS_API_KEY` and `THE_ODDS_API_KEY` and `GEMINI_API_KEY` from plain Cloud Run env vars to GCP Secret Manager — wire via Cloud Run secret references
- [x] Verify Cloud Logging captures errors from the prediction pipeline — Cloud Run captures all stdout/stderr automatically; FastAPI unhandled exceptions log to stderr by default
- [x] Update `README.md` with live URL and deployment instructions
- [x] Fix GCP budget alert: scope to `tennis-data-487809` only + attach email notification channel so alerts actually fire
- [x] Cap Cloud Run max instances to 3 — hard ceiling against traffic attacks
- [x] Add `docs/COST_CONTROLS.md` documenting all cost protection measures

### Story 5 — Weekly Cost Review Agent
> **Moved to Sprint 6.**

---

## Sprint 5 — Detail

> **Goal:** Make `tennis.mateogrisales.com` self-explanatory to a recruiter or hiring manager. The UI must communicate the Data/AI/ML engineering behind the app — model logic, data sources, stack — without needing a README. No backend changes in this sprint.

### Story 1 — Match Card Redesign
**AC-What:** Each match card shows both players inline (no expand/collapse) with: ranking position + points, model probability (%), bookmaker raw implied probability (%), edge (model − raw_implied, in pp), and value signal badge per player. Model vs implied shown as side-by-side progress bars. Positive edge is green, negative/zero is grey.
**AC-Rule:** No backend changes — all fields already in the `/predict` response. Use `raw_implied` (1/price) for the bookmaker bar — NOT `true_implied`. `raw_implied` is what the bookie actually charges; it's the correct threshold for a value bet. `true_implied` has the vig removed and would overstate the edge.
**AC-How-critical:** Remove `PredictionPanel.tsx` and the expand/collapse `selectedIdx` state — all info is now inline. Match time and tournament context go at the bottom of each card.

- [x] Rewrite `MatchCard.tsx` — both players inline, prob bars, edge %, signal badge per player
- [x] Delete `PredictionPanel.tsx` — no longer needed
- [x] Update `Index.tsx` — remove `selectedIdx` expand/collapse state, pass `fetched_at` down
- [x] Confirm `raw_implied` (not `true_implied`) is used for bookmaker bar and edge display

### Story 2 — App Context Layer
**AC-What:** A visitor who knows nothing about tennis betting or ML can read the page and understand: what the app does, how the model works, where the data comes from, and what stack powers it — all without leaving the page.
**AC-Rule:** HowItWorks must describe the 4-step pipeline: ATP scraper → rank-based model → raw implied extraction → value signal. TechStackBar must list: GCP Cloud Run · API Gateway · BigQuery · Python · Gemini API. DataFreshness must use `fetched_at` from the API response.
**AC-How-critical:** HeroSection disclaimer must be visible above the fold without scrolling on desktop. Keep all sections scannable — this is a portfolio demo, not a blog post.

- [x] Create `HeroSection.tsx` — purpose statement + portfolio disclaimer badge above the fold
- [x] Create `HowItWorks.tsx` — 4-step pipeline (Scrape → Model → Compare → Signal), 2×2 grid on tablet, single column on mobile
- [x] ~~Create `TechStackBar.tsx`~~ — removed; stack is visible on GitHub, UI kept clean
- [x] Create `DataFreshness.tsx` — "Last updated · H:MM AM/PM GMT±X" using `fetched_at`, positioned above match list with Refresh button
- [x] Compose new layout in `Index.tsx`: Hero → HowItWorks → DataFreshness → MatchList

### Story 3 — Polish & Edge Cases
**AC-What:** Empty state, error state, and per-match error all render with friendly copy and no raw error text. Mobile layout is usable at 375px. Error state renders inside the Layout (with header/footer) — currently it renders outside.
**AC-Rule:** Empty state must explain *why* (no upcoming ATP matches) and give context ("Pre-match odds are available 24–48h before tournament days"). Error state must have a Retry button. No raw stack traces or API error strings shown to the user.
**AC-How-critical:** Error state currently renders outside `Layout` (no header/footer) — fix this so the app stays branded even on failure.

- [x] Rewrite empty state — illustration + friendly headline + context subtext
- [x] Rewrite error state — move inside `Layout`, friendly copy, Retry button, no raw error text
- [x] Verify mobile layout at 375px — MatchCard, HowItWorks steps all readable
- [x] Verify `SignalBadge.tsx` and `TennisBallLoader.tsx` unchanged

---

## Sprint 6 — Detail

> **Goal:** Replace the linear prediction pipeline with a stateful LangGraph graph. Introduces a RAG layer (semantic chunking + FAISS), structured LLM output with citation anchors, and a deterministic hallucination validation node with a cyclic retry edge. Exposed via a versioned `POST /v2/predict` endpoint — the existing `/predict` endpoint is never modified.
>
> **Branch:** `feature/sprint6-langgraph` — merged to `main` only after end-to-end validation of `/v2/predict`.
> **Deployment rule:** Both `/predict` and `/v2/predict` run simultaneously on Cloud Run post-merge. Frontend cutover to `/v2/predict` is a separate, independently-reversible change.

---

### Epic 1 — LangGraph Foundation

#### Story 1 — Graph Scaffold + State Definition
**AC-What:** A `StateGraph` compiles and `graph.invoke()` runs end-to-end using stub node functions that return hardcoded fixtures. No real API calls are made. All nodes, edges, and the conditional retry edge are wired.
**AC-Rule:** `GraphState` must use `TypedDict`. `llm_insights` field must be typed as `list[MatchInsight]` (not `list[str]`) from the start — no interim string type. Conditional edge must use `add_conditional_edges`, not an `if/else` inside a node body.
**AC-How-critical:** `retry_count` must be tracked in `GraphState` and incremented by the `validate_output` stub — not in a local variable. The graph must enforce `retry_count <= 2` in the conditional edge router function, not inside the node.

- [x] Define `src/agent/state.py` — `GraphState` TypedDict with all fields including `llm_insights: list[MatchInsight]`
- [x] Define `src/agent/models.py` — `FactualClaim` and `MatchInsight` Pydantic models
- [x] Scaffold `src/agent/graph.py` — `StateGraph`, all node stubs registered, edges wired
- [x] Wire conditional retry edge: `validate_output` → `generate_insight` (retry) or `format_response` (accept/flag)
- [x] Unit test: `graph.invoke({})` with stub nodes runs without error and returns a `GraphState`

#### Story 2 — Migrate Odds + Rankings Nodes
**AC-What:** `fetch_odds` and `fetch_rankings` are live graph nodes. Running the graph with these two nodes real (rest stubbed) produces the same match list and rankings dict as the current `/predict` pipeline.
**AC-Rule:** No business logic changes to the odds or rankings logic — this is a structural migration only. `api/main.py` existing `/predict` route must not be touched.
**AC-How-critical:** Nodes must read from and write to `GraphState` exclusively — no return values, no side effects outside state.

- [x] Create `src/agent/nodes/fetch_odds.py` — migrated from `api/main.py`, writes `matches` (DataFrame) + `matches_total` + `matches_filtered_inplay` to state
- [x] Create `src/agent/nodes/fetch_rankings.py` — migrated from ATP scraper, writes `rankings` (`dict[str, dict[str, int]]`) to state
- [ ] Remove duplicated logic from `api/main.py` — deferred to Story 6 (cannot remove until `/v2/predict` is wired up; AC-Rule forbids touching the existing `/predict` route)
- [x] Integration test: live graph invocation with real fetch nodes, rest stubbed — Madrid Open smoke test passed (2 events, 4 players, 100% ranking match, all stub fields populated downstream)

---

### Epic 2 — RAG Layer

#### Story 3 — Document Builder + Semantic Chunker + FAISS Index
**AC-What:** Given populated `matches` and `rankings` in state, `build_rag_context` produces a FAISS index and a `retrieved_docs_by_id: dict[str, str]` map stored in state. Each chunk ID is stable and unique within a request.
**AC-Rule:** Chunking must use `SemanticChunker` (embedding-based boundary detection) — not `RecursiveCharacterTextSplitter` or fixed token size. Each chunk document must be formatted as: `"[Player] (Rank #N, P pts) vs [Player] (Rank #N, P pts) — [Tournament] — Odds: A@{price}, B@{price}"`. FAISS index is in-memory only — no persistence to disk.
**AC-How-critical:** `retrieved_docs_by_id` must be keyed by a deterministic chunk ID (e.g. `f"match_{i}_chunk_{j}"`) so the validator can look up by ID. The FAISS index and the ID map must stay in sync — same order, same keys.

- [ ] Create `src/agent/nodes/build_rag_context.py`
- [ ] Implement match + player document construction from `GraphState`
- [ ] Wire `SemanticChunker` for embedding-based boundary splitting
- [ ] Embed chunks and load into FAISS in-memory index
- [ ] Store `faiss_index` and `retrieved_docs_by_id` in state
- [ ] Unit test: N matches → index contains ≥ N chunks, all chunk IDs present in `retrieved_docs_by_id`

#### Story 4 — Structured LLM Generation with Citation Anchors
**AC-What:** `generate_insight` produces one `MatchInsight` per match pair, stored in `state["llm_insights"]`. Each `MatchInsight.key_claims` contains one `FactualClaim` per factual assertion, with a valid `source_chunk_id` referencing a key in `retrieved_docs_by_id`.
**AC-Rule:** LLM call must use `llm.with_structured_output(MatchInsight)` — no free-form string generation, no post-hoc JSON parsing. The grounding prompt must explicitly instruct the LLM to use only the provided context and cite the `source_chunk_id` for every factual claim.
**AC-How-critical:** `retrieved_docs` (the list of chunks returned by the retriever for this match) must be stored in state alongside `retrieved_docs_by_id` — the validator needs both. If `with_structured_output` raises a `ValidationError`, the node must set `validation_passed = False` and write an empty `MatchInsight` — never let a `ValidationError` propagate unhandled to the graph runtime.

- [ ] Create `src/agent/nodes/generate_insight.py`
- [ ] Retrieve top-K chunks from FAISS index per match pair
- [ ] Store retrieved chunks in `state["retrieved_docs"]`
- [ ] Construct grounding prompt with retrieved context
- [ ] Call `llm.with_structured_output(MatchInsight)` and store result in `state["llm_insights"]`
- [ ] Handle `ValidationError` — write empty `MatchInsight`, set `validation_passed = False`
- [ ] Unit test: mock LLM returns valid `MatchInsight` JSON → stored correctly in state

---

### Epic 3 — Hallucination Validation

#### Story 5 — `validate_output` Node + Conditional Retry Edge
**AC-What:** For each `MatchInsight` in state, every `FactualClaim.value` is cross-referenced against the chunk at `retrieved_docs_by_id[claim.source_chunk_id]`. If any claim value is not found in its source chunk, `validation_passed` is set to `False`. After N=2 failed retries, the insight is accepted but each unverified claim is flagged with `verified: False` — never silently passed through.
**AC-Rule:** Validation must be a dictionary lookup — `claim.value in retrieved_docs_by_id[claim.source_chunk_id]` — no regex, no NLP similarity scoring. The retry limit is `N=2` (maximum 3 total generation attempts). On retry, `generate_insight` must receive a stricter prompt variant instructing it to reduce the number of factual claims.
**AC-How-critical:** The conditional edge router must live in `graph.py`, not inside the `validate_output` node. The node sets state; the router reads state and returns the next node name. A missing `source_chunk_id` key in `retrieved_docs_by_id` must be treated as a failed validation (not a `KeyError`).

- [ ] Create `src/agent/nodes/validate_output.py`
- [ ] Implement claim-level dictionary lookup against `retrieved_docs_by_id`
- [ ] Set `validation_passed` and increment `retry_count` in state
- [ ] Flag unverified claims with `verified: False` on retry exhaustion
- [ ] Add conditional edge router function in `graph.py`
- [ ] Unit test: inject a `FactualClaim` with a value not present in its source chunk → `validation_passed = False`
- [ ] Unit test: `retry_count >= 2` with failed validation → router returns `format_response`, claims flagged

---

### Epic 4 — API Integration + Ops

#### Story 6 — Versioned `POST /v2/predict` Endpoint
**AC-What:** `POST /v2/predict` returns a JSON array structurally identical to `/predict`, with two additional fields per match: `insight` (string, the grounded LLM narrative) and `validation_passed` (bool). The existing `POST /predict` route is byte-for-byte unchanged.
**AC-Rule:** `/predict` must not be touched — no refactoring, no shared helper extraction that changes its behavior. `/v2/predict` invokes `graph.invoke()` internally. The Pydantic response model for v2 must extend (not replace) the existing model.
**AC-How-critical:** `graph.invoke()` must be called with a fully initialized `GraphState` — all optional fields defaulted, `retry_count` set to `0`. Unhandled exceptions from the graph must return HTTP 500 with a structured error body, not a raw Python traceback.

- [ ] Add `POST /v2/predict` route to `api/main.py` — existing `/predict` untouched
- [ ] Define `PredictionV2` Pydantic response model extending existing model with `insight` and `validation_passed`
- [ ] Wire `graph.invoke()` inside the v2 handler
- [ ] Add graph-level exception handling → HTTP 500 structured response
- [ ] Smoke test: `POST /v2/predict` against local server returns valid structured response
- [ ] End-to-end test on Cloud Run: both `/predict` and `/v2/predict` return 200

#### Story 7 — Weekly Cost Review Agent
**AC-What:** A scheduled agent runs weekly, queries Cloud Monitoring for Cloud Run invocation count and estimated cost for the past 7 days, and sends a digest email to `mateo@grisalogic.com`. If cost exceeds a configured threshold, the email subject line is prefixed with `[ALERT]`.
**AC-Rule:** Threshold must be configurable via an env var (`COST_ALERT_THRESHOLD_USD`), not hardcoded. Agent must use the existing GCP service account — no new IAM roles.
**AC-How-critical:** If the Cloud Monitoring query returns no data (e.g. no invocations that week), the email must still send with a "No activity" message — not silently skip.

- [ ] Implement `scripts/cost_review_agent.py` — Cloud Monitoring query + email digest
- [ ] Add `COST_ALERT_THRESHOLD_USD` env var to `config.yaml`
- [ ] Schedule via Cloud Scheduler (weekly, Monday 09:00 America/Bogota)
- [ ] Test: manual invocation produces a correctly formatted email

---

## Future Backlog (Post-MVP)
- Upgrade ML model to XGBoost / ensemble
- Add weather/altitude/conditions data source
- Add UTR ratings (requires paid API access)
- Pre-compute nightly predictions and cache in BigQuery
- Model performance tracking and retraining pipeline
- Vertex AI integration for model hosting
- **Cost kill switch:** Budget alert → Pub/Sub topic → Cloud Function → set Cloud Run `max-instances=0` automatically when spend threshold is crossed. Currently not worth the complexity — `X-API-Key` auth + 3 instance cap + email alerts are sufficient for portfolio traffic.
