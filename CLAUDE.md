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

## CURRENT FOCUS: Sprint 2
Ready to begin Sprint 2. Awaiting scope definition.

## Git Workflow
Before finishing a task, ask for permission to stage changes and create a conventional commit (e.g., `feat: integrate GCS upload`).