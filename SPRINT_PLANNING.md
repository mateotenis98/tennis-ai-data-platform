# 🗺️ Tennis AI Platform - Sprint Planning

> **Note:** This is a living document (Agile workflow). Dates, hours, and specific technologies may be adapted as the project evolves.

## Phase 1: Google Cloud Platform (GCP) Pipeline


| Sprint (Week) | Primary Objective                 | Key Tasks (Jira / GitHub Projects)                                                                                                                      | Functional Deliverable (GitHub)                                | Est. Hours  | Dates          | Status           |
| ------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ----------- | -------------- | ---------------- |
| **Sprint 1**  | Raw Data Ingestion (Data Lake)    | 1. Set up GCP project & Service Account. 2. Write Python script to extract The-Odds-API. 3. Save raw JSONs to Google Cloud Storage (GCS).               | Script `extract_odds.py`, `requirements.txt`, `.env.example`.  | 5 - 7 hrs   | Mar 6 - Mar 18 | ✅ Done (4.5 hrs) |
| **Sprint 2**  | ETL & Data Warehousing (BigQuery) | 1. Read JSON files from GCS. 2. Clean and flatten data using Pandas. 3. Load structured data into BigQuery.                                             | Script `etl_gcs_to_bq.py`, SQL DDL/table creation queries.     | 8 - 10 hrs  | Mar 20 - Apr 2 | 🔄 Current       |
| **Sprint 3**  | Predictive Modeling (Vertex AI)   | 1. Extract data from BigQuery to Vertex AI Workbench. 2. Train XGBoost model (winner prediction). 3. Deploy model to Vertex AI Endpoints.               | `notebooks/` folder with EDA, script `train_deploy_vertex.py`. | 10 - 12 hrs | TBD            | 📅 Planned       |
| **Sprint 4**  | GenAI Layer & UI Deployment       | 1. Integrate LangChain with Gemini API. 2. Create an agent to compare ML prediction vs. actual odds. 3. Build and deploy web dashboard using Streamlit. | Script `agent_gemini.py`, deployed `app.py` (Streamlit).       | 6 - 8 hrs   | TBD            | 📅 Planned       |


