# Tennis AI Data Platform

> End-to-End AI & Data Engineering platform for extracting, processing, and predicting ATP tennis match outcomes using Google Cloud Platform (GCP), ML models, and a multi-agent AI layer.

**Live demo:** [tennis.mateogrisales.com](https://tennis.mateogrisales.com)

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
| LLM / Agents | Google Gemini Flash (Sprint 3) → ATP scraper (Sprint 4+) |
| Frontend | Lovable (React) → mateogrisales.com |
| Backend API | GCP Cloud Run (private) + API Gateway (public) |

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

### ✅ Sprint 3 — End-to-End Prediction MVP
- Dynamic ATP sport key discovery via `/v4/sports/` — no hardcoded tournament names
- `filter_upcoming()` strips in-play matches — live odds reflect score state, not pre-match probability
- Ranking-based probability model: `P(A) = points_A / (points_A + points_B)`
- Comparison logic: model prob vs bookmaker `raw_implied` (1/price) to surface value bets
- Local Streamlit demo (`app.py`) — full pipeline behind a single button, results cached in session state

### ✅ Sprint 4 — Deploy to GCP + mateogrisales.com
- FastAPI prediction API on Cloud Run (private) fronted by GCP API Gateway — enterprise pattern for `grisalogic.com` org policy
- Docker image built via Cloud Build → Artifact Registry — no local Docker required
- React UI (Lovable) deployed at **[tennis.mateogrisales.com](https://tennis.mateogrisales.com)** — live end-to-end
- Live ATP rankings scraped from `atptour.com` on every request — no staleness
- All secrets in GCP Secret Manager — no plain env vars on Cloud Run
- CORS locked to production origins; Cloud Run capped at 3 max instances; GCP budget alert wired to email
- Security rationale documented in `docs/SECURITY.md`; cost controls in `docs/COST_CONTROLS.md`

### ✅ Sprint 5 — UI Showcase
- Match cards redesigned: inline probability bars (model vs bookmaker implied), edge %, ranking points, signal badge per player
- Hero section with purpose statement and portfolio disclaimer above the fold
- How It Works: 4-step pipeline explainer (Scrape → Model → Compare → Signal)
- Data freshness timestamp with manual Refresh button — inline loader keeps existing cards visible
- Warm brand background (`#FFF8F4`) separates cards visually — confirmed on mobile at 375px

### 📅 Sprint 6 — LangGraph Agent Architecture + Ops
### 📅 Sprint 7 — Data Enrichment & Model Upgrade
### 📅 Sprint 8 — Advanced UI & Auth

## Repository Structure
```
src/
  ingestion/      # Data extraction scripts (The-Odds-API → GCS)
  processing/     # ETL: flatten, transform, load to BigQuery
  agents/         # AI agents (rankings, model, explanation)
scripts/          # Dev setup and secret management utilities
notebooks/        # EDA and exploration
docs/             # Schema docs and agent persona files
data/raw/         # Local sandbox data (gitignored)
data/processed/   # Transformed CSVs (gitignored)
```

## Local Setup (New Machine)

**Prerequisites:** `gcloud` CLI installed, authenticated, and project set.

```bash
# 1. Clone the repo
git clone <repo-url> && cd tennis-ai-data-platform

# 2. Pull all secrets from GCP Secret Manager and recreate .env
./scripts/setup_env.sh

# 3. Activate virtual environment
source .venv/bin/activate
```

> First time pushing secrets from the source machine? Run `./scripts/push_secrets.sh` first.

## Secrets Management

All secrets (API keys, service account JSON) are stored in **GCP Secret Manager** — never in the repo.
Non-sensitive config (`project_id`, `bucket_name`) lives in `config.yaml`, which is tracked in git.

| Script | Purpose |
|---|---|
| `scripts/push_secrets.sh` | Push local `.env` + service account JSON → GCP Secret Manager |
| `scripts/setup_env.sh` | Pull secrets from GCP Secret Manager → recreate `.env` on a new machine |

### Secrets stored in GCP Secret Manager

| Secret Name | Description |
|---|---|
| `THE_ODDS_API_KEY` | The-Odds-API authentication key |
| `GEMINI_API_KEY` | Google AI Studio API key (Gemini Flash) |
| `GCP_SERVICE_ACCOUNT_JSON` | Full contents of the service account JSON key file |

> GCP Project: `tennis-data-487809`
> Console: GCP Console → Secret Manager
> The service account `tennis-uploader` must have the **Secret Manager Secret Accessor** role to read secrets.

### Config tracked in git

| Key | File | Value |
|---|---|---|
| `gcp.project_id` | `config.yaml` | `tennis-data-487809` |
| `gcp.bucket_name` | `config.yaml` | `raw-tennis-data` |

---
*Developed by Mateo Grisales*
