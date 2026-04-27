from typing import Literal

from pydantic import BaseModel


class FactualClaim(BaseModel):
    """A single verifiable fact extracted from an LLM-generated insight.

    Each claim carries a pointer to the retrieved chunk it must be grounded in,
    enabling deterministic validation without regex or NLP similarity scoring.
    """

    value: str
    source_chunk_id: str
    verified: bool = True


class MatchInsight(BaseModel):
    """Structured LLM output for a single match pair.

    Using structured generation (with_structured_output) ensures every factual
    assertion is explicitly cited — validation becomes a dictionary lookup.
    """

    player_a_outlook: str
    player_b_outlook: str
    key_claims: list[FactualClaim]
    confidence: Literal["high", "medium", "low"]
