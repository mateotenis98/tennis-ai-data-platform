# Tennis AI Data Platform

> End-to-End AI & Data Engineering platform for extracting, processing, and predicting ATP tennis match outcomes using Google Cloud Platform (GCP), ML models, and a multi-agent AI layer.

## Project Overview
This platform ingests live ATP tennis odds from The-Odds-API, transforms and stores them in BigQuery, and feeds them into a prediction engine that combines ML models with AI agents to generate match outcome probabilities. Results are displayed in a web interface and compared against bookmaker odds to surface potential value.

> **Purpose:** Showcase of AI, ML, and Data Engineering skills — not financial or betting advice.

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Cloud Provider | Google Cloud Platform (GCP) |
| Data Lake | Cloud Storage (GCS) |
| Data Warehouse | BigQuery |
| Data Source | The-Odds-API v4 |
| LLM / Agents | Google Gemini Flash |
| Frontend | Lovable (React) → mateogrisales.com |
| Backend API | GCP Cloud Functions |

## Current Status

### ✅ Sprint 1 — Raw Data Ingestion
- GCP infrastructure set up (GCS, IAM, billing)
- `extract_odds.py` fetches H2H odds from The-Odds-API
- Raw JSON uploaded to GCS

### ✅ Sprint 2 — ETL & Data Warehousing
- Nested JSON flattened with Pandas (`transform.py`)
- Confirmed schema: one row per match per bookmaker
- Data loaded into BigQuery (`etl_gcs_to_bq.py`)
- Schema documented in `docs/MIAMI_OPEN_SCHEMA.md`

### 🔄 Sprint 3 — End-to-End Prediction MVP (Current)
- General ATP upcoming matches endpoint
- Gemini Flash agent fetches ATP rankings
- Implied probability converter + ranking-based predictor
- Comparison logic: model probability vs bookmaker implied probability
- Local Streamlit UI demo

### 📅 Sprint 4 — Agent Layer & Data Enrichment
### 📅 Sprint 5 — Backend API (Cloud Functions)
### 📅 Sprint 6 — Frontend (Lovable → mateogrisales.com)

## Repository Structure
```
src/
  ingestion/      # Data extraction scripts (The-Odds-API → GCS)
  processing/     # ETL: flatten, transform, load to BigQuery
notebooks/        # EDA and exploration
docs/             # Schema docs and agent persona files
data/raw/         # Local sandbox data (gitignored)
```

---
*Developed by Mateo Grisales*
