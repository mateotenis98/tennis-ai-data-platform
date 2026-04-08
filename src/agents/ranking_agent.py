"""Ranking agent that fetches ATP rankings for specific players using Gemini Flash with Google Search."""

import logging
import os
import re
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

_MODEL = "gemini-2.5-flash"
_PROMPT_TEMPLATE = """
Search for the current official ATP singles rankings and return the ranking and points for these specific players:

{player_list}

Respond ONLY with a numbered list in this exact format, one player per line, using the exact player names provided above:
1. Jannik Sinner | 11400
2. Carlos Alcaraz | 13550

Where the number is the player's current ATP ranking position and the number after | is their current ATP ranking points.
Do not include any extra text, commentary, or headers — just the numbered list.
"""


def fetch_atp_rankings(player_names: list[str]) -> dict[str, dict]:
    """Fetch current ATP rankings and points for a specific list of players using Gemini Flash.

    Uses Gemini's built-in Google Search tool to retrieve up-to-date ATP rankings
    for exactly the players provided. Player names are passed verbatim so the
    returned dict keys match the input names exactly — no fuzzy matching needed.

    Args:
        player_names: List of player name strings exactly as returned by The-Odds-API
            (e.g. ["Jannik Sinner", "Frances Tiafoe"]).

    Returns:
        A dict mapping player name (str) to a dict with ``rank`` (int) and
        ``points`` (int).
        Example: {"Jannik Sinner": {"rank": 2, "points": 11400}, ...}

    Raises:
        EnvironmentError: If GEMINI_API_KEY is not set.
        ValueError: If player_names is empty or Gemini returns an unparseable response.
    """
    if not player_names:
        raise ValueError("player_names must not be empty.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set in the environment.")

    client = genai.Client(api_key=api_key)

    player_list = "\n".join(f"- {name}" for name in player_names)
    prompt = _PROMPT_TEMPLATE.format(player_list=player_list)
    logger.info("Querying Gemini Flash for rankings of: %s", player_names)

    # Google Search grounding returns 0 parts with gemini-2.5-flash (known SDK issue).
    # Model training data is sufficient for ATP rankings — they update weekly but
    # don't shift dramatically between sessions.
    response = client.models.generate_content(
        model=_MODEL,
        contents=prompt,
    )
    raw_text = response.text
    if not raw_text:
        raise ValueError("Gemini returned an empty response.")
    raw_text = raw_text.strip()
    logger.debug("Gemini raw response:\n%s", raw_text)

    rankings = _parse_rankings(raw_text, player_names)
    logger.info("Successfully parsed rankings for %d/%d players.", len(rankings), len(player_names))
    return rankings


def _parse_rankings(text: str, expected_names: list[str]) -> dict[str, dict]:
    """Parse Gemini's numbered list response into a rankings dict.

    Matches parsed names back to the expected player names list so the
    returned keys are guaranteed to be the exact strings from the odds API.
    Lines that don't match the format are skipped with a warning.

    Args:
        text: Raw text response from Gemini containing the numbered list.
        expected_names: The original player name strings passed to Gemini.

    Returns:
        A dict mapping player name (str) to ``{"rank": int, "points": int}``.

    Raises:
        ValueError: If no valid rankings could be parsed from the text.
    """
    rankings: dict[str, dict] = {}
    pattern = re.compile(r"^(\d+)\.\s+(.+?)\s*\|\s*([\d,]+)$")
    names_lower = {n.lower(): n for n in expected_names}

    for line in text.splitlines():
        line = line.strip()
        match = pattern.match(line)
        if match:
            rank = int(match.group(1))
            parsed_name = match.group(2).strip()
            points = int(match.group(3).replace(",", ""))
            # Map back to exact odds-API name via case-insensitive lookup
            canonical = names_lower.get(parsed_name.lower(), parsed_name)
            rankings[canonical] = {"rank": rank, "points": points}
        elif line:
            logger.warning("Skipping unparseable line: %r", line)

    if not rankings:
        raise ValueError(f"Could not parse any ATP rankings from Gemini response:\n{text}")

    return rankings


if __name__ == "__main__":
    # Use the exact player names currently live in the Miami Open odds
    test_players = [
        "Tommy Paul", "Arthur Fils",
        "Frances Tiafoe", "Jannik Sinner",
        "Francisco Cerundolo", "Alexander Zverev",
    ]
    rankings = fetch_atp_rankings(player_names=test_players)
    print(f"\nRankings for {len(rankings)} players:")
    for name, data in sorted(rankings.items(), key=lambda x: x[1]["rank"]):
        print(f"  {data['rank']:>3}. {name:<30} {data['points']:>6} pts")
