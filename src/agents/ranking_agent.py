"""Ranking agent that fetches current ATP singles rankings using Gemini Flash with Google Search."""

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
_TOP_N_DEFAULT = 100
_PROMPT_TEMPLATE = """
Search for the current official ATP singles rankings and return the top {top_n} players.

Respond ONLY with a numbered list in this exact format, one player per line:
1. Jannik Sinner | 9710
2. Carlos Alcaraz | 9255
3. Alexander Zverev | 7430
...

Where the number after | is the player's current ATP ranking points.
Do not include any extra text, commentary, or headers — just the numbered list.
"""


def fetch_atp_rankings(top_n: int = _TOP_N_DEFAULT) -> dict[str, dict]:
    """Fetch current ATP singles rankings and points using Gemini Flash with Google Search.

    Uses Gemini's built-in Google Search tool to retrieve up-to-date ATP rankings
    and points in real time. Returns a mapping of player name to rank and points
    for use in the probability calculator.

    Args:
        top_n: Number of top-ranked players to retrieve. Defaults to 100.

    Returns:
        A dict mapping player name (str) to a dict with ``rank`` (int) and
        ``points`` (int).
        Example: {"Jannik Sinner": {"rank": 1, "points": 9710}, ...}

    Raises:
        EnvironmentError: If GEMINI_API_KEY is not set.
        ValueError: If Gemini returns a response that cannot be parsed.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set in the environment.")

    client = genai.Client(api_key=api_key)

    prompt = _PROMPT_TEMPLATE.format(top_n=top_n)
    logger.info("Querying Gemini Flash for top %d ATP rankings...", top_n)

    response = client.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    raw_text = response.text.strip()
    logger.debug("Gemini raw response:\n%s", raw_text)

    rankings = _parse_rankings(raw_text)
    logger.info("Successfully parsed %d ATP rankings.", len(rankings))
    return rankings


def _parse_rankings(text: str) -> dict[str, dict]:
    """Parse a numbered list of player names and points into a rankings dict.

    Expects lines in the format ``N. Player Name | Points``,
    e.g. ``1. Jannik Sinner | 9710``.
    Lines that don't match are skipped with a warning.

    Args:
        text: Raw text response from Gemini containing the numbered list.

    Returns:
        A dict mapping player name (str) to ``{"rank": int, "points": int}``.

    Raises:
        ValueError: If no valid rankings could be parsed from the text.
    """
    rankings: dict[str, dict] = {}
    pattern = re.compile(r"^(\d+)\.\s+(.+?)\s*\|\s*([\d,]+)$")

    for line in text.splitlines():
        line = line.strip()
        match = pattern.match(line)
        if match:
            rank = int(match.group(1))
            name = match.group(2).strip()
            points = int(match.group(3).replace(",", ""))
            rankings[name] = {"rank": rank, "points": points}
        elif line:
            logger.warning("Skipping unparseable line: %r", line)

    if not rankings:
        raise ValueError(f"Could not parse any ATP rankings from Gemini response:\n{text}")

    return rankings


if __name__ == "__main__":
    rankings = fetch_atp_rankings(top_n=20)
    print(f"\nTop {len(rankings)} ATP Rankings:")
    for name, data in sorted(rankings.items(), key=lambda x: x[1]["rank"]):
        print(f"  {data['rank']:>3}. {name:<30} {data['points']:>6} pts")
