from langgraph.graph import END, StateGraph

from src.agent.nodes.fetch_odds import fetch_odds
from src.agent.nodes.fetch_rankings import fetch_rankings
from src.agent.state import GraphState

# ---------------------------------------------------------------------------
# Node stubs — replaced with real implementations in Stories 3–6
# (fetch_odds and fetch_rankings are live as of Story 2.)
# ---------------------------------------------------------------------------

def build_rag_context(state: GraphState) -> dict:
    """Stub: populated in Story 3 with SemanticChunker + FAISS index build."""
    return {
        "faiss_index": None,
        "retrieved_docs_by_id": {},
        "retrieved_docs": [],
    }


def generate_insight(state: GraphState) -> dict:
    """Stub: populated in Story 4 with structured LLM call (with_structured_output)."""
    return {
        "llm_insights": state.get("llm_insights", []),
        "retrieved_docs": state.get("retrieved_docs", []),
    }


def validate_output(state: GraphState) -> dict:
    """Stub: populated in Story 5 with deterministic claim-level validation."""
    return {
        "validation_passed": True,
        "retry_count": state.get("retry_count", 0),
    }


def format_response(state: GraphState) -> dict:
    """Stub: populated in Story 6 when merged with model probabilities."""
    return {"predictions": state.get("predictions", [])}


# ---------------------------------------------------------------------------
# Conditional edge router — lives here, NOT inside validate_output node
# ---------------------------------------------------------------------------

def _validation_router(state: GraphState) -> str:
    """Route after validation: retry generation or accept and format.

    Retry limit is enforced here so the node stays side-effect-free.
    """
    if not state["validation_passed"] and state["retry_count"] < 2:
        return "generate_insight"
    return "format_response"


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    """Compile and return the prediction StateGraph.

    Node execution order:
        fetch_odds → fetch_rankings → build_rag_context → generate_insight
        → validate_output →(conditional)→ generate_insight (retry)
                                       → format_response  (accept/flag)
        → END
    """
    graph = StateGraph(GraphState)

    graph.add_node("fetch_odds", fetch_odds)
    graph.add_node("fetch_rankings", fetch_rankings)
    graph.add_node("build_rag_context", build_rag_context)
    graph.add_node("generate_insight", generate_insight)
    graph.add_node("validate_output", validate_output)
    graph.add_node("format_response", format_response)

    graph.set_entry_point("fetch_odds")
    graph.add_edge("fetch_odds", "fetch_rankings")
    graph.add_edge("fetch_rankings", "build_rag_context")
    graph.add_edge("build_rag_context", "generate_insight")
    graph.add_edge("generate_insight", "validate_output")
    graph.add_conditional_edges(
        "validate_output",
        _validation_router,
        {
            "generate_insight": "generate_insight",
            "format_response": "format_response",
        },
    )
    graph.add_edge("format_response", END)

    return graph.compile()


# Compiled graph instance — imported by the FastAPI handler in Story 6
graph = build_graph()
