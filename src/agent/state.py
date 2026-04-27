from typing import Any

from typing_extensions import TypedDict

from src.agent.models import MatchInsight


class GraphState(TypedDict):
    """Shared state passed between all nodes in the prediction graph.

    Fields are written by specific nodes and read by downstream nodes —
    no node should mutate a field it does not own.
    """

    # --- Epic 1: fetched data ---
    matches: list[dict]           # raw upcoming matches from The-Odds-API
    rankings: dict[str, int]      # player name → ATP rank position

    # --- Epic 2: RAG layer ---
    faiss_index: Any              # in-memory FAISS index (built per request)
    retrieved_docs_by_id: dict[str, str]  # chunk_id → chunk text (for validation lookup)
    retrieved_docs: list[str]     # ordered chunks returned by retriever for current match

    # --- Epic 3: generation + validation ---
    llm_insights: list[MatchInsight]  # structured output, one per match pair
    validation_passed: bool
    retry_count: int              # incremented by validate_output; capped at 2 by router

    # --- Epic 4: final output ---
    predictions: list[dict]       # merged model probabilities + grounded insights
