# Security Architecture

## API Key on the Frontend (Known Limitation)

The React frontend sends an `X-API-Key` header with every `POST /predict` request.
This key (`VITE_API_KEY`) is stored as an environment variable in the hosting platform
(Netlify/Vercel) and is **not hardcoded in source code**.

However, `VITE_` prefixed variables in Vite are **embedded into the compiled JavaScript
bundle at build time**. This means:

- The key does not appear in the GitHub repository.
- The key **is** visible to anyone who opens DevTools → Sources in their browser.
- This is a fundamental browser limitation — there is no way to fully hide an API key
  in a public client-side React application.

### Why this is acceptable for this project

The real protection lives on the server side:

| Control | Implementation |
|---|---|
| Strong key | 64-char hex key generated via `openssl rand -hex 32` |
| Server-side validation | FastAPI rejects any request without a valid `X-API-Key` |
| CORS restriction | Cloud Run only accepts requests from `tennis.mateogrisales.com` |
| Cost ceiling | Cloud Run capped at 3 max instances — limits blast radius of any abuse |
| Secrets in Secret Manager | `TENNIS_API_KEY`, `THE_ODDS_API_KEY` stored in GCP Secret Manager, not plain env vars |

### Truly secure alternative (not implemented)

For apps where the API key must never be exposed, the pattern is a **backend proxy**:
- Frontend calls your own backend (no API key needed client-side)
- Backend holds the key server-side and forwards the request
- Adds latency and infrastructure complexity — not justified for a portfolio project

### Key rotation

If the key is ever compromised:
1. Generate a new key: `openssl rand -hex 32`
2. Update in GCP Secret Manager: `echo -n "<new_key>" | gcloud secrets versions add TENNIS_API_KEY --data-file=- --project=tennis-data-487809`
3. Update `VITE_API_KEY` in Netlify/Vercel env var settings and trigger a redeploy

---

## Secrets Management

All server-side secrets are stored in **GCP Secret Manager** and injected into Cloud Run
at runtime via secret references — never as plain environment variables.

| Secret | Secret Manager Name | Used by |
|---|---|---|
| Tennis API key | `TENNIS_API_KEY` | FastAPI `X-API-Key` validation |
| The Odds API key | `THE_ODDS_API_KEY` | Odds ingestion pipeline |
| Gemini API key | `GEMINI_API_KEY` | Reserved — Gemini agent replaced by ATP scraper |

> `GEMINI_API_KEY` is retained in Secret Manager but is currently unused.
> The Gemini ranking agent was replaced by a live `atptour.com` scraper in Sprint 4.
> Remove this secret once Sprint 5 LangGraph refactor confirms it is not needed.
