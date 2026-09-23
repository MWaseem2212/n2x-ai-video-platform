from app.models.assets import VideoBrief
from app.services.provider_selector import select_best_provider
from app.services.reuse_scorer import calculate_reuse_score

INTERNAL_PROCESSING_COST = 0.10


def calculate_cost_estimate(brief: VideoBrief) -> dict:
    reuse_result = calculate_reuse_score(brief)
    provider_decision = select_best_provider(brief)

    if provider_decision["recommended"] is None:
        return {"error": "No suitable provider available"}

    full_regeneration_cost = provider_decision["cost"]

    new_generation_fraction = reuse_result["new_generation_required"] / 100
    actual_generation_cost = round(full_regeneration_cost * new_generation_fraction, 2)

    estimated_total = round(actual_generation_cost + INTERNAL_PROCESSING_COST, 2)
    estimated_cost_without_reuse = round(full_regeneration_cost + INTERNAL_PROCESSING_COST, 2)

    saving_amount = round(estimated_cost_without_reuse - estimated_total, 2)
    saving_percentage = round((saving_amount / estimated_cost_without_reuse) * 100) if estimated_cost_without_reuse > 0 else 0

    return {
        "provider": provider_decision["recommended"],
        "reuse_score": reuse_result["reuse_score"],
        "new_generation_required": reuse_result["new_generation_required"],
        "provider_generation_cost": actual_generation_cost,
        "internal_processing_cost": INTERNAL_PROCESSING_COST,
        "estimated_total": estimated_total,
        "estimated_cost_without_reuse": estimated_cost_without_reuse,
        "rag_saving_amount": saving_amount,
        "rag_saving_percentage": saving_percentage,
    }


if __name__ == "__main__":
    from app.models.assets import Sector

    test_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining safeguarding",
    )

    result = calculate_cost_estimate(test_brief)

    print(f"Provider: {result['provider']}")
    print(f"Reuse Score: {result['reuse_score']}% | New Generation: {result['new_generation_required']}%")
    print(f"\nEstimated Cost:")
    print(f"  Provider generation: £{result['provider_generation_cost']}")
    print(f"  Internal processing: £{result['internal_processing_cost']}")
    print(f"  Estimated Total: £{result['estimated_total']}")
    print(f"\nRAG Saving:")
    print(f"  Cost without reuse: £{result['estimated_cost_without_reuse']}")
    print(f"  Estimated Saving: £{result['rag_saving_amount']} ({result['rag_saving_percentage']}%)")