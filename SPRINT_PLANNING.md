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
| **Sprint 3** | End-to-End Prediction MVP | ✓ 1. Dynamic ATP sport key discovery via `/v4/sports/`. ✓ 2. `raw_implied` + `true_implied` columns in `transform.py`. ✓ 3. `data/processed/` CSV output for local sandbox. ✓ 4. Build ranking agent (Gemini Flash + web search). ✓ 5. Build ranking-based probability calculator. ✓ 6. Build comparison & recommendation logic. 7. Wire into local Streamlit UI. | Working demo: user selects match → agent fetches rankings → probability calculated → compared vs odds → recommendation displayed | 10–12 hrs | Mon Mar 23– | 🔄 Current |
| **Sprint 4** | Deploy to GCP + mateogrisales.com | 1. Expose prediction pipeline as GCP Cloud Functions / Cloud Run API. 2. Build minimal React UI in Lovable. 3. Connect frontend to backend API. 4. Deploy live at mateogrisales.com. | Live public demo at mateogrisales.com with the ranking-based model | 8–10 hrs | TBD | 📅 Planned |
| **Sprint 5** | LangGraph Agent Architecture | 1. Introduce LangGraph as coordinator layer. 2. Refactor sub-agents (odds, rankings, model, explanation) into LangGraph nodes. 3. Add retry/fallback logic (e.g. ranking fetch fails → cached data). 4. Conditional routing based on data availability or confidence thresholds. | LangGraph coordinator replacing linear Python orchestration; stateful multi-agent graph | 10–12 hrs | TBD | 📅 Planned |
| **Sprint 6** | Data Enrichment & Model Upgrade | 1. Add historical H2H data (Sackmann dataset → BigQuery). 2. Add surface/conditions features. 3. Add news/sentiment agent. 4. Upgrade ranking model to logistic regression. 5. Add `docs/ML_ENGINEER.md` agent persona. | Enriched predictions, trained baseline model — improvements go live immediately | 12–15 hrs | TBD | 📅 Planned |
| **Sprint 7** | Polish & React UI Upgrade | 1. Improve React UI in Lovable (match selection, visualization, recommendation display). 2. Add authentication/rate limiting to backend. 3. Leverage LangGraph checkpointing for async prediction requests. | Polished public demo at mateogrisales.com | 8–10 hrs | TBD | 📅 Planned |

---

## Future Backlog (Post-MVP)
- Upgrade ML model to XGBoost / ensemble
- Add weather/altitude/conditions data source
- Add UTR ratings (requires paid API access)
- Pre-compute nightly predictions and cache in BigQuery
- Model performance tracking and retraining pipeline
- Vertex AI integration for model hosting
