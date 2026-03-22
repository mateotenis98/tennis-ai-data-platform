# Project: Tennis AI Data Platform
# Role: Senior GCP Data & ML Engineer

## Architecture Rules
- Cloud Provider: Google Cloud Platform (GCP) exclusively.
- Language: Python 3.10+.
- Code Style: PEP 8, strict type hints, and Google-style Docstrings for all functions.
- Security: Never hardcode API keys or GCP credentials. Always use `python-dotenv` and `.env`.

## Repository Structure (Enforce Modularity)
- Do NOT put business logic in `main.py`. 
- Data extraction scripts go in `src/ingestion/`.
- Temporary raw data goes in `data/raw/` (ensure this is in .gitignore).

## Sprint 1 (API to GCS) — COMPLETE ✓
Local execution and GCP Cloud Storage upload are 100% done. The pipeline successfully fetches H2H odds from The-Odds-API and lands raw JSON files in GCS.

## CURRENT FOCUS: Sprint 2 — Miami Open EDA (Sandbox Phase)
**Sport key:** `tennis_atp_miami_open` | **Market:** `h2h` | **Region:** `us`

**Approach:** Sandbox-first. Understand the raw JSON locally before touching GCP.
1. Extract raw JSON locally via `src/ingestion/extract_odds.py` → saves to `data/raw/`
2. Explore and flatten the nested structure in `notebooks/01_miami_open_eda.ipynb`
3. Document confirmed schema in `docs/MIAMI_OPEN_SCHEMA.md`
4. Build `src/processing/transform.py` against local data
5. Promote to GCP (GCS + BigQuery) once the pipeline is validated locally

**Key lesson from Sprint 1:** Using `_SPORT = "upcoming"` returns all sports, not just tennis.
Always use a specific sport key (e.g. `tennis_atp_miami_open`) for targeted extraction.

## Multi-Agent Routing
When working on ETL, data cleaning, or BigQuery tasks (Sprint 2), ALWAYS read `docs/DATA_ENGINEER.md` first to adopt the Data Engineer persona and constraints.

## Git Workflow
Before finishing a task, ask for permission to stage changes and create a conventional commit (e.g., `feat: integrate GCS upload`).