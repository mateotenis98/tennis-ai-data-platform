# Miami Open – Odds Data Schema

> **Status:** Confirmed after EDA in `notebooks/01_miami_open_eda.ipynb`.

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
        ├── sport_title         (str)  "ATP Miami Open"
        ├── commence_time       (str)  ISO 8601 UTC timestamp
        ├── home_team           (str)  player name → player_1
        ├── away_team           (str)  player name → player_2
        └── bookmakers          (list)
              └── bookmaker
                    ├── key         (str)   bookmaker identifier
                    ├── title       (str)   bookmaker display name
                    ├── last_update (str)   ISO 8601 UTC timestamp
                    └── markets     (list)
                          └── market (key = "h2h")
                                └── outcomes (list, always 2 for h2h)
                                      └── outcome
                                            ├── name  (str)   player name
                                            └── price (float) decimal odds
```

## Final Flat Schema (confirmed)

One row per match per bookmaker. **69 rows for 12 matches across 7 bookmakers.**

| Column | Type | Notes |
|---|---|---|
| `event_id` | STRING | Unique per match |
| `commence_time` | TIMESTAMP | Parse from ISO 8601 UTC |
| `bookmaker` | STRING | Display name (e.g. "DraftKings") |
| `player_1` | STRING | home_team from raw event |
| `price_1` | FLOAT | Decimal odds for player_1 |
| `player_2` | STRING | away_team from raw event |
| `price_2` | FLOAT | Decimal odds for player_2 |

## Key Findings from EDA
- **Zero nulls** across all fields — very clean data
- **Prices are decimal odds** (e.g. 1.42 = 1.42x stake), not American odds
- **3–7 bookmakers per match** (avg 5.8): BetRivers, DraftKings, FanDuel, Bovada, LowVig, BetOnline, BetUS
- `home_team` / `away_team` always map cleanly to the two h2h outcomes
- `commence_time` and `last_update` need to be parsed to TIMESTAMP for BigQuery
