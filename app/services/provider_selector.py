import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.models.assets import VideoBrief
from app.providers import PROVIDERS

load_dotenv()

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


# --- LLM Explanation Layer ---

class ProviderExplanation(BaseModel):
    explanation: str


llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
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