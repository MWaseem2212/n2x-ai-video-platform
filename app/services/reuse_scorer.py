from app.models.assets import VideoBrief
from app.services.rag_search import find_best_avatar, find_best_voice, find_best_background

COMPONENT_WEIGHTS = {
    "avatar": 0.4,
    "voice": 0.3,
    "background": 0.3,
}


def get_asset_label(component_name: str, asset: dict | None) -> str | None:
    if not asset:
        return None
    if component_name == "voice":
        return f"{asset.get('tone')} ({asset.get('accent')})"
    return asset.get("name") or asset.get("category")


def calculate_reuse_score(brief: VideoBrief) -> dict:
    avatar_result = find_best_avatar(brief)
    voice_result = find_best_voice(brief)
    background_result = find_best_background(brief)

    components = {
        "avatar": avatar_result,
        "voice": voice_result,
        "background": background_result,
    }

    total_reuse = 0.0
    breakdown = {}

    for name, result in components.items():
        weight = COMPONENT_WEIGHTS[name]
        if result["found"]:
            contribution = weight * result["score"]
            status = "Existing"
        else:
            contribution = 0.0
            status = "New Generation Required"

        total_reuse += contribution
        breakdown[name] = {
            "status": status,
            "score": round(result["score"], 3),
            "asset_name": get_asset_label(name, result["asset"]),
        }

    reuse_score = round(total_reuse * 100)
    new_generation_required = 100 - reuse_score

    return {
        "reuse_score": reuse_score,
        "new_generation_required": new_generation_required,
        "breakdown": breakdown,
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
        description="Adult social care video for UK care workers explaining the five signs of safeguarding concern",
    )

    result = calculate_reuse_score(test_brief)

    print(f"Reuse Score: {result['reuse_score']}% Existing Assets")
    print(f"New Generation Required: {result['new_generation_required']}%")
    print("\nBreakdown:")
    for component, info in result["breakdown"].items():
        print(f"  {component}: {info['status']} (score={info['score']}, asset={info['asset_name']})")