"""LangGraph node: fetch live ATP odds, flatten, and filter to upcoming matches.

Wraps the existing :func:`src.ingestion.extract_odds.fetch_odds`,
:func:`src.processing.transform.flatten_odds`, and
:func:`src.processing.transform.filter_upcoming` pipeline as a single graph node.

Per Sprint 6 Story 2 AC, this is a structural migration only — business logic
is not modified. The pre-filter event count and the in-play drop count are
written to state so the downstream ``format_response`` node (Story 6) can
include them in the API payload without re-fetching.
"""

import logging

import pandas as pd

from src.agent.state import GraphState
from src.ingestion.extract_odds import fetch_odds as _fetch_odds_raw
from src.processing.transform import filter_upcoming, flatten_odds

logger = logging.getLogger(__name__)


def fetch_odds(state: GraphState) -> dict:
    """Fetch live ATP odds, flatten, and filter to upcoming matches.

    This is the entry node of the graph — ``state`` is unused on entry. The
    node populates the ``matches`` DataFrame plus the two metadata counters
    needed by the response layer.

    Args:
        state: Current graph state (ignored — entry node).

    Returns:
        Partial state update with ``matches`` (DataFrame), ``matches_total``,
        and ``matches_filtered_inplay``. ``matches`` is an empty DataFrame
        when the API returns no events.

    Raises:
        Exception: Any exception from the underlying odds fetch propagates
            unchanged so the graph runtime can surface it.
    """
    raw = _fetch_odds_raw()

    if not raw:
        logger.info("Odds API returned no events.")
        return {
            "matches": pd.DataFrame(),
            "matches_total": 0,
            "matches_filtered_inplay": 0,
        }

    df = flatten_odds(raw)
    matches_total = int(df["event_id"].nunique())

    df = filter_upcoming(df)
    matches_filtered_inplay = matches_total - int(df["event_id"].nunique())

    return {
        "matches": df,
        "matches_total": matches_total,
        "matches_filtered_inplay": matches_filtered_inplay,
    }
