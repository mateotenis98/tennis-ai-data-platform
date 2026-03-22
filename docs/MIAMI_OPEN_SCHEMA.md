# Miami Open – Odds Data Schema

> **Status:** Draft — to be confirmed after running `notebooks/01_miami_open_eda.ipynb` on real data.
> Update this document with actual findings before building `src/processing/transform.py`.

## Source
- **API:** The-Odds-API v4
- **Sport key:** `tennis_atp_miami_open`
- **Market:** `h2h` (head-to-head win/lose odds)
- **Region:** `us`
- **Raw files:** `data/raw/tennis_odds_<timestamp>.json` (local sandbox) → `gs://<bucket>/raw/` (GCP)

## Raw JSON Structure

```
[ event, event, ... ]
  └── event
        ├── id                  (str)  unique event ID
        ├── sport_key           (str)  "tennis_atp_miami_open"
        ├── sport_title         (str)  human-readable sport name
        ├── commence_time       (str)  ISO 8601 UTC timestamp
        ├── home_team           (str)  player name
        ├── away_team           (str)  player name
        └── bookmakers          (list)
              └── bookmaker
                    ├── key         (str)  bookmaker identifier
                    ├── title       (str)  bookmaker display name
                    ├── last_update (str)  ISO 8601 UTC timestamp
                    └── markets     (list)
                          └── market
                                ├── key      (str)  "h2h"
                                └── outcomes (list)
                                      └── outcome
                                            ├── name  (str)   player name
                                            └── price (float) American or decimal odds
```

## Target Flat Schema (BigQuery)

> Confirm column names, types, and nullability after EDA.

| Column | Type | Notes |
|---|---|---|
| `event_id` | STRING | Unique per match |
| `commence_time` | TIMESTAMP | Parse from ISO 8601 |
| `home_team` | STRING | |
| `away_team` | STRING | |
| `bookmaker_key` | STRING | |
| `bookmaker_title` | STRING | |
| `last_update` | TIMESTAMP | Parse from ISO 8601 |
| `market_key` | STRING | Always `h2h` for this pipeline |
| `outcome_name` | STRING | Player name (matches home_team or away_team) |
| `price` | FLOAT | Odds value |

## Transform Decisions
> Fill in after EDA:
> - Timestamp parsing approach
> - Null handling strategy
> - Any anomalies found (missing bookmakers, duplicate outcomes, etc.)
