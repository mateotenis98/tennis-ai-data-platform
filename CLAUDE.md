# Project: Tennis AI Data Platform
# Role: Senior GCP Data & ML Engineer

## Architecture Rules
- Cloud Provider: Google Cloud Platform (GCP) exclusively.
- Language: Python 3.10+.
- Code Style: PEP 8, strict type hints, and Google-style Docstrings for all functions.
- Security: Never hardcode API keys or GCP credentials. Use `python-dotenv` and `.env` for local dev. All secrets are stored in **GCP Secret Manager** — use `scripts/push_secrets.sh` to upload and `scripts/setup_env.sh` to restore on a new machine.
- Config: Non-sensitive config (`GCP_PROJECT_ID`, `GCP_BUCKET_NAME`) lives in `config.yaml` (tracked in git). Load via `src/config.py`. Only true secrets (API keys, service account JSON) go in `.env` and Secret Manager.

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
1. ✓ Update `extract_odds.py` to dynamically discover active ATP sport keys via `/v4/sports/` — no hardcoding
2. ✓ Build ranking agent using **Gemini Flash** to fetch ATP rankings via web search
3. ✓ Add `raw_implied` (1/price) and `true_implied` (vig-removed) columns to `transform.py`
4. Build ranking-based probability calculator
5. ✓ Build comparison & recommendation logic (model prob vs raw implied prob)
6. Wire into local Streamlit UI for demo

**Key architectural decisions:**
- **LLM:** Google Gemini Flash (free tier, GCP-native) — NOT Claude API (separate billing)
- **Frontend (future):** Lovable (React) deployed to mateogrisales.com
- **Backend (future):** GCP Cloud Functions
- **Prediction:** Real-time per user request (no pre-computation for now)
- **Agent pattern:** Coordinator agent → sub-agents (odds, rankings, model, explanation)

**Local data flow:**
- `data/raw/tennis_odds_<timestamp>.json` — raw API response (mirrors GCS)
- `data/processed/tennis_odds_processed_<timestamp>.csv` — flat transformed data (mirrors BigQuery)

**Key lesson from Sprint 1:** Using `_SPORT = "upcoming"` returns all sports, not just tennis.
**Key lesson from Sprint 3:** Never hardcode tournament sport keys — use `/v4/sports/` to discover active `tennis_atp_*` keys dynamically.
**Key lesson from Sprint 3:** Betting advice must compare model prob vs `raw_implied` (1/price), NOT `true_implied`. The vig is already baked into the raw price — that's the real threshold for a value bet.

## Sprint 4 (Planned) — LangGraph Agent Architecture

**Goal:** Refactor the linear Sprint 3 pipeline into a proper coordinator → sub-agent graph.

**Trigger:** Introduce LangGraph when the pipeline stops being linear — i.e., when the coordinator needs to make routing decisions, not just call functions in order.

**Planned work:**
1. Introduce LangGraph as the coordinator layer
2. Refactor sub-agents (odds, rankings, model, explanation) into LangGraph nodes
3. Add retry/fallback logic (e.g., ranking fetch fails → use cached data)
4. Conditional routing based on data availability or confidence thresholds
5. Begin wiring toward GCP Cloud Functions (stateful graph becomes valuable here)

**Key decision:** Do NOT introduce LangGraph in Sprint 3. The MVP pipeline is linear — plain Python orchestration is sufficient and simpler to debug.

## Sprint 5+ (Planned) — Production on GCP

**Goal:** Deploy the LangGraph coordinator as a Cloud Function or Cloud Run service.

**Planned work:**
1. Deploy backend to GCP Cloud Functions / Cloud Run
2. Connect Lovable (React) frontend at mateogrisales.com to backend API
3. Leverage LangGraph checkpointing for async/long-running prediction requests

## Multi-Agent Routing
When working on ETL, data cleaning, or BigQuery tasks, ALWAYS read `docs/DATA_ENGINEER.md` first to adopt the Data Engineer persona and constraints.

## Git Workflow
Before finishing a task, ask for permission to stage changes and create a conventional commit (e.g., `feat: integrate GCS upload`).