from app.services.provider_selector import select_best_provider, select_provider_with_fallback
from app.providers import PROVIDERS


def test_select_best_provider_excludes_no_avatar_providers(sample_brief):
    decision = select_best_provider(sample_brief)
    assert decision["recommended"] != "creatify"


def test_select_best_provider_picks_lowest_cost(sample_brief):
    decision = select_best_provider(sample_brief)
    all_costs = {s["provider"]: s["cost"] for s in decision["all_scores"] if s["has_avatar"]}
    cheapest = min(all_costs, key=all_costs.get)
    assert decision["recommended"] == cheapest


def test_fallback_switches_when_top_choice_unavailable(sample_brief):
    PROVIDERS["synthesia"].is_available = False
    try:
        result = select_provider_with_fallback(sample_brief)
        assert result["recommended"] == "heygen"
        assert any(log["status"] == "unavailable" for log in result["fallback_log"])
    finally:
        PROVIDERS["synthesia"].is_available = True