from app.graph.builder import build_video_creation_graph
from app.models.assets import VideoBrief, Sector


def run_video_creation(brief: VideoBrief) -> dict:
    app = build_video_creation_graph()

    initial_state = {
        "brief": brief,
        "video_plan": None,
        "reuse_result": None,
        "provider_decision": None,
        "cost_estimate": None,
    }

    final_state = app.invoke(initial_state)
    return final_state


def print_result(label: str, result: dict):
    print("=" * 50)
    print(label)
    print("=" * 50)
    print(f"\nVideo Plan: {result['video_plan'].title}")
    print(f"Structure: {len(result['video_plan'].proposed_structure)} scenes")
    print(f"\nReuse Score: {result['reuse_result']['reuse_score']}%")
    print(f"New Generation Required: {result['reuse_result']['new_generation_required']}%")
    print(f"\nRecommended Provider: {result['provider_decision']['recommended']}")
    print(f"\nEstimated Total Cost: £{result['cost_estimate']['estimated_total']}")
    print(f"RAG Saving: £{result['cost_estimate']['rag_saving_amount']} ({result['cost_estimate']['rag_saving_percentage']}%)")
    print()


if __name__ == "__main__":
    # --- Test 1: Happy Path (assets available) ---
    happy_path_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining safeguarding",
    )

    happy_result = run_video_creation(happy_path_brief)
    print_result("TEST 1: HAPPY PATH (Adult Care — Assets Available)", happy_result)

    # --- Test 2: Edge Case (no assets for this sector) ---
    edge_case_brief = VideoBrief(
        sector=Sector.LEAVING_CARE,  
        country="United Kingdom",
        audience="Young People",
        tone="Supportive",
        video_type="Advice",
        duration_seconds=45,
        description="Advice video for young people leaving care about independent living",
    )

    try:
        edge_result = run_video_creation(edge_case_brief)
        print_result("TEST 2: EDGE CASE (Leaving Care — No Assets Available)", edge_result)
    except Exception as e:
        print(f"\nERROR in edge case: {type(e).__name__}: {e}")