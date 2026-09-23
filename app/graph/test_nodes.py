from app.graph.nodes import plan_video_node, reuse_search_node, provider_selection_node, cost_estimation_node
from app.models.assets import VideoBrief, Sector


if __name__ == "__main__":
    test_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining safeguarding",
    )

    state = {"brief": test_brief, "video_plan": None, "reuse_result": None, "provider_decision": None, "cost_estimate": None}

    print("Testing plan_video_node...")
    result = plan_video_node(state)
    print(f"  video_plan title: {result['video_plan'].title}\n")

    print("Testing reuse_search_node...")
    result = reuse_search_node(state)
    print(f"  reuse_score: {result['reuse_result']['reuse_score']}%\n")

    print("Testing provider_selection_node...")
    result = provider_selection_node(state)
    print(f"  recommended: {result['provider_decision']['recommended']}\n")

    print("Testing cost_estimation_node...")
    result = cost_estimation_node(state)
    print(f"  estimated_total: £{result['cost_estimate']['estimated_total']}\n")