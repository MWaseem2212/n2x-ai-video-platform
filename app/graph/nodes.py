from app.graph.state import VideoCreationState
from app.services.video_planner import generate_video_plan
from app.services.reuse_scorer import calculate_reuse_score
from app.services.provider_selector import select_best_provider
from app.services.cost_estimator import calculate_cost_estimate


def plan_video_node(state: VideoCreationState) -> dict:
    brief = state["brief"]
    video_plan = generate_video_plan(brief)
    return {"video_plan": video_plan}


def reuse_search_node(state: VideoCreationState) -> dict:
    brief = state["brief"]
    reuse_result = calculate_reuse_score(brief)
    return {"reuse_result": reuse_result}


def provider_selection_node(state: VideoCreationState) -> dict:
    brief = state["brief"]
    provider_decision = select_best_provider(brief)
    return {"provider_decision": provider_decision}


def cost_estimation_node(state: VideoCreationState) -> dict:
    brief = state["brief"]
    cost_estimate = calculate_cost_estimate(brief)
    return {"cost_estimate": cost_estimate}