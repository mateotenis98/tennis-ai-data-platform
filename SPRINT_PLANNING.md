# Tennis AI Platform - Sprint Planning

> **Note:** This is a living document (Agile workflow). Dates, hours, and specific technologies may be adapted as the project evolves.

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
| **Sprint 4** | Deploy to GCP + mateogrisales.com | 1. Expose prediction pipeline as GCP Cloud Run API. 2. Build minimal React UI in Lovable. 3. Connect frontend to backend API. 4. Deploy live at mateogrisales.com. | Live public demo at mateogrisales.com with the ranking-based model | 8–10 hrs | TBD | 🔄 In Progress |
| **Sprint 5** | LangGraph Agent Architecture | 1. Introduce LangGraph as coordinator layer. 2. Refactor sub-agents (odds, rankings, model, explanation) into LangGraph nodes. 3. Add retry/fallback logic (e.g. ranking fetch fails → cached data). 4. Conditional routing based on data availability or confidence thresholds. | LangGraph coordinator replacing linear Python orchestration; stateful multi-agent graph | 10–12 hrs | TBD | 📅 Planned |
| **Sprint 6** | Data Enrichment & Model Upgrade | 1. Add historical H2H data (Sackmann dataset → BigQuery). 2. Add surface/conditions features. 3. Add news/sentiment agent. 4. Upgrade ranking model to logistic regression. 5. Add `docs/ML_ENGINEER.md` agent persona. | Enriched predictions, trained baseline model — improvements go live immediately | 12–15 hrs | TBD | 📅 Planned |
| **Sprint 7** | Polish & React UI Upgrade | 1. Improve React UI in Lovable (match selection, visualization, recommendation display). 2. Add authentication/rate limiting to backend. 3. Leverage LangGraph checkpointing for async prediction requests. | Polished public demo at mateogrisales.com | 8–10 hrs | TBD | 📅 Planned |

---

## Sprint 4 — Detail

> **Goal:** Go live as fast as possible. A live public demo is more valuable for the portfolio than a local Streamlit app.
> **Decision:** Cloud Run over Cloud Functions — Gemini Flash API call latency + future LangGraph refactor make Cloud Run the right fit.

### Story 1 — Backend API (Cloud Run)
**AC-What:** A `POST /predict` request to the Cloud Run URL returns a JSON array of pre-match ATP matches with model probability, raw implied probability, and value signal for each player.
**AC-Rule:** Only pre-match matches returned — `filter_upcoming()` must be applied. Secrets loaded from GCP Secret Manager, not env vars.
**AC-How-critical:** FastAPI app must return structured JSON (not HTML). Dockerfile must not copy `.env` into the image. Cloud Run service must require authentication (not public by default).

- [x] Wrap pipeline logic into a FastAPI app (`api/main.py`) with a `POST /predict` endpoint
- [x] Write `Dockerfile` and validate image builds and runs locally
- [ ] Push image to GCP Artifact Registry
- [ ] Configure Cloud Run service (env vars wired to Secret Manager, IAM, region)
- [ ] Smoke test deployed endpoint end-to-end

### Story 2 — Frontend (Lovable)
**AC-What:** A visitor to the frontend URL sees a list of current ATP pre-match matches, each with both players, their value signal (value bet / marginal / no bet), model probability, and bookmaker implied probability.
**AC-Rule:** UI must handle the case where no pre-match matches are available (show a friendly empty state, not a crash).
**AC-How-critical:** API call must include the API key in the request header — do not expose it in client-side JS as a plain string; use an environment variable in Lovable.

- [ ] Design minimal UI layout: match cards, value signal badge, odds table
- [ ] Scaffold React app in Lovable
- [ ] Wire `POST /predict` API call with loading and error states

### Story 3 — Integration & Go Live
**AC-What:** Visiting `tennis.mateogrisales.com` loads the React app and successfully fetches and displays live predictions.
**AC-Rule:** CORS must only allow the production frontend origin — not a wildcard `*`.
**AC-How-critical:** API key auth must be validated server-side on Cloud Run before the pipeline executes — a request without a valid key must return 401.

- [ ] Configure CORS on Cloud Run to allow frontend origin
- [ ] Add API key auth to Cloud Run endpoint (not open to the public)
- [ ] Point subdomain (e.g. `tennis.mateogrisales.com`) to Lovable frontend
- [ ] End-to-end smoke test on production URL

### Story 4 — Hardening (Definition of Done)
**AC-What:** The deployed app is observable — errors in the prediction pipeline appear in Cloud Logging and the README documents the live URL and how to redeploy.
**AC-Rule:** No secrets in plain env vars anywhere in the deployed stack.
**AC-How-critical:** Cloud Logging must capture unhandled exceptions from the FastAPI app, not just HTTP access logs.

- [ ] Confirm all secrets are in Secret Manager — no plain env vars
- [ ] Verify Cloud Logging captures errors from the prediction pipeline
- [ ] Update `README.md` with live URL and deployment instructions

---

## Future Backlog (Post-MVP)
- Upgrade ML model to XGBoost / ensemble
- Add weather/altitude/conditions data source
- Add UTR ratings (requires paid API access)
- Pre-compute nightly predictions and cache in BigQuery
- Model performance tracking and retraining pipeline
- Vertex AI integration for model hosting
