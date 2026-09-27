from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.models.assets import VideoBrief
from app.providers import PROVIDERS
from app.config import settings

SCORING_WEIGHTS = {
    "avatar_available": 0.5,
    "cost": 0.5,
}


def score_provider(provider_name: str, brief: VideoBrief) -> dict:
    provider = PROVIDERS[provider_name]

    avatars = provider.list_avatars()
    has_avatar = len(avatars) > 0
    cost = provider.estimate_cost(brief)

    # Reasoning: avatar available = 1.0, na ho to 0.0
    avatar_score = 1.0 if has_avatar else 0.0

    return {
        "provider": provider_name,
        "has_avatar": has_avatar,
        "avatar_count": len(avatars),
        "cost": cost,
        "avatar_score": avatar_score,
    }


def select_best_provider(brief: VideoBrief) -> dict:
    scores = [score_provider(name, brief) for name in PROVIDERS]

    eligible = [s for s in scores if s["has_avatar"]]

    if not eligible:
        return {"recommended": None, "reason": "No provider has a suitable avatar", "all_scores": scores}

    best = min(eligible, key=lambda s: s["cost"])

    return {"recommended": best["provider"], "cost": best["cost"], "all_scores": scores}



def select_provider_with_fallback(brief: VideoBrief) -> dict:
    scores = [score_provider(name, brief) for name in PROVIDERS]
    eligible = [s for s in scores if s["has_avatar"]]

    if not eligible:
        return {
            "recommended": None,
            "reason": "No provider has a suitable avatar",
            "fallback_log": [],
        }

    sorted_eligible = sorted(eligible, key=lambda s: s["cost"])

    fallback_log = []

    for candidate in sorted_eligible:
        provider_name = candidate["provider"]
        provider = PROVIDERS[provider_name]

        if provider.is_available:
            fallback_log.append({
                "provider": provider_name,
                "status": "selected",
                "reason": "Available and lowest cost among remaining eligible providers",
            })
            return {
                "recommended": provider_name,
                "cost": candidate["cost"],
                "all_scores": scores,
                "fallback_log": fallback_log,
            }
        else:
            fallback_log.append({
                "provider": provider_name,
                "status": "unavailable",
                "reason": "Provider marked unavailable — checking next eligible provider",
            })

    return {
        "recommended": None,
        "reason": "All eligible providers are currently unavailable",
        "all_scores": scores,
        "fallback_log": fallback_log,
    }


# --- LLM Explanation Layer ---

class ProviderExplanation(BaseModel):
    explanation: str


llm = ChatGroq(model="openai/gpt-oss-120b", api_key=settings.GROQ_API_KEY)
structured_llm = llm.with_structured_output(ProviderExplanation, method="json_mode")


def explain_recommendation(brief: VideoBrief, decision: dict) -> str:
    if decision["recommended"] is None:
        return "No suitable provider found for this request."

    prompt = f"""
In one or two sentences, explain why "{decision['recommended']}" was selected
as the best AI video provider for a {brief.sector.value} sector video,
given it has an available avatar and the lowest cost (£{decision['cost']})
among eligible providers. Be concise and professional.

Respond in JSON format with a single key "explanation".
"""
    result = structured_llm.invoke(prompt)
    return result.explanation


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

    decision = select_best_provider(test_brief)
    print(f"Recommended Provider: {decision['recommended']}")
    print(f"Cost: £{decision['cost']}")
    print("\nAll scores:")
    for s in decision["all_scores"]:
        print(f"  {s['provider']}: avatar={s['has_avatar']}, cost=£{s['cost']}")

    explanation = explain_recommendation(test_brief, decision)
    print(f"\nExplanation: {explanation}")