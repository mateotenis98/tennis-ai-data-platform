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

## Sprint 2 (ETL & BigQuery) — COMPLETE ✓
Nested JSON flattened with Pandas, schema confirmed via EDA (see `docs/MIAMI_OPEN_SCHEMA.md`), data loaded into BigQuery. One row per match per bookmaker.

## CURRENT FOCUS: Sprint 3 — End-to-End Prediction MVP

**Goal:** A fully working prediction pipeline (simple model, full stack) before adding complexity.

**Sport key:** `tennis_atp` (general upcoming ATP matches) | **Market:** `h2h` | **Region:** `us`

**Approach:** Sandbox-first. Build and validate locally, then promote to GCP.
1. Update `extract_odds.py` to use general `tennis_atp` sport key for upcoming matches
2. Build ranking agent using **Gemini Flash** to fetch ATP rankings via web search
3. Build implied probability converter (math from decimal odds)
4. Build ranking-based probability calculator
5. Build comparison & recommendation logic (model prob vs implied prob)
6. Wire into local Streamlit UI for demo

**Key architectural decisions:**
- **LLM:** Google Gemini Flash (free tier, GCP-native) — NOT Claude API (separate billing)
- **Frontend (future):** Lovable (React) deployed to mateogrisales.com
- **Backend (future):** GCP Cloud Functions
- **Prediction:** Real-time per user request (no pre-computation for now)
- **Agent pattern:** Coordinator agent → sub-agents (odds, rankings, model, explanation)

**Key lesson from Sprint 1:** Using `_SPORT = "upcoming"` returns all sports, not just tennis.
Always use a specific sport key (e.g. `tennis_atp`) for targeted extraction.

## Multi-Agent Routing
When working on ETL, data cleaning, or BigQuery tasks (Sprint 2), ALWAYS read `docs/DATA_ENGINEER.md` first to adopt the Data Engineer persona and constraints.

## Git Workflow
Before finishing a task, ask for permission to stage changes and create a conventional commit (e.g., `feat: integrate GCS upload`).