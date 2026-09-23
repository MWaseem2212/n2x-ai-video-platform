from langgraph.graph import StateGraph, START, END

from app.graph.state import VideoCreationState
from app.graph.nodes import (
    plan_video_node,
    reuse_search_node,
    provider_selection_node,
    cost_estimation_node,
)


def build_video_creation_graph():
    graph = StateGraph(VideoCreationState)

    graph.add_node("plan_video", plan_video_node)
    graph.add_node("reuse_search", reuse_search_node)
    graph.add_node("select_provider", provider_selection_node)
    graph.add_node("estimate_cost", cost_estimation_node)

    graph.add_edge(START, "plan_video")
    graph.add_edge("plan_video", "reuse_search")
    graph.add_edge("reuse_search", "select_provider")
    graph.add_edge("select_provider", "estimate_cost")
    graph.add_edge("estimate_cost", END)

    return graph.compile()