"""LangGraph node: fetch ATP rankings for the players in the current state.

Wraps :func:`src.agents.ranking_agent.fetch_atp_rankings` as a graph node.
Reads the unique player names from ``state["matches"]`` and writes the
resulting rankings dict to ``state["rankings"]``.
"""

import logging

from src.agent.state import GraphState
from src.agents.ranking_agent import fetch_atp_rankings

logger = logging.getLogger(__name__)


def fetch_rankings(state: GraphState) -> dict:
    """Fetch ATP rankings for all unique players in the matches DataFrame.

    Args:
        state: Graph state containing the ``matches`` DataFrame produced by
            the upstream :func:`fetch_odds` node.

    Returns:
        Partial state update with ``rankings`` — a dict mapping each
        odds-API player name to ``{"rank": int, "points": int}``. Returns
        an empty dict when ``state["matches"]`` is empty.
    """
    df = state["matches"]

    if df.empty:
        logger.info("No matches in state — skipping rankings fetch.")
        return {"rankings": {}}

    players = df["outcome_name"].unique().tolist()
    rankings = fetch_atp_rankings(player_names=players)
    return {"rankings": rankings}
