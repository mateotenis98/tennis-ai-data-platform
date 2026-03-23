# Tennis AI Platform - Sprint Planning

> **Note:** This is a living document (Agile workflow). Dates, hours, and specific technologies may be adapted as the project evolves.

## Phase 1: GCP Data Pipeline

| Sprint | Primary Objective | Key Tasks | Functional Deliverable | Est. Hours | Dates | Status |
|---|---|---|---|---|---|---|
| **Sprint 1** | Raw Data Ingestion (Data Lake) | 1. Set up GCP project & Service Account. 2. Write Python script to extract The-Odds-API. 3. Save raw JSONs to GCS. | `extract_odds.py`, `requirements.txt`, `.env.example` | 5–7 hrs | Mar 6–Mar 18 | ✅ Done (4.5 hrs) |
| **Sprint 2** | ETL & Data Warehousing (BigQuery) | 1. Read JSON from GCS. 2. Flatten nested structure with Pandas. 3. Load structured data into BigQuery. | `transform.py`, `etl_gcs_to_bq.py`, confirmed schema in `docs/MIAMI_OPEN_SCHEMA.md` | 8–10 hrs | Mar 20–Apr 2 | ✅ Done |

---

## Phase 2: Prediction Engine + UI (MVP)

| Sprint | Primary Objective | Key Tasks | Functional Deliverable | Est. Hours | Dates | Status |
|---|---|---|---|---|---|---|
| **Sprint 3** | End-to-End Prediction MVP | 1. Update `extract_odds.py` to support general `tennis_atp` sport key. 2. Build ranking agent (Gemini Flash + web search for ATP rankings). 3. Build implied probability converter from odds. 4. Build ranking-based probability calculator. 5. Build comparison & recommendation logic. 6. Wire into local Streamlit UI. | Working demo: user selects match → agent fetches rankings → probability calculated → compared vs odds → recommendation displayed | 10–12 hrs | TBD | 🔄 Current |
| **Sprint 4** | Agent Layer & Data Enrichment | 1. Add historical H2H data (Sackmann dataset → BigQuery). 2. Add surface/conditions features. 3. Add news/sentiment agent. 4. Upgrade simple ranking model to logistic regression. 5. Add `docs/ML_ENGINEER.md` agent persona. | Multi-agent coordinator, enriched predictions, trained baseline model | 12–15 hrs | TBD | 📅 Planned |
| **Sprint 5** | Backend API (GCP) | 1. Expose prediction pipeline as Cloud Functions API. 2. Add authentication/rate limiting. 3. Validate end-to-end from API call to prediction response. | Deployed Cloud Functions endpoint serving predictions | 8–10 hrs | TBD | 📅 Planned |
| **Sprint 6** | Frontend (Lovable → mateogrisales.com) | 1. Build React UI in Lovable. 2. Connect to Cloud Functions API. 3. Display upcoming matches, prediction results, and recommendation. 4. Deploy to mateogrisales.com. | Live public demo at mateogrisales.com | 8–10 hrs | TBD | 📅 Planned |

---

## Future Backlog (Post-MVP)
- Upgrade ML model to XGBoost / ensemble
- Add weather/altitude/conditions data source
- Add UTR ratings (requires paid API access)
- Pre-compute nightly predictions and cache in BigQuery
- Model performance tracking and retraining pipeline
- Vertex AI integration for model hosting
