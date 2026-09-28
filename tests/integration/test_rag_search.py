from app.services.rag_search import find_best_avatar, find_best_voice, find_best_background
from app.models.assets import VideoBrief, Sector


def test_rag_search_returns_results_for_all_sectors():
    for sector in Sector:
        brief = VideoBrief(
            sector=sector,
            country="UK",
            audience="General",
            tone="Professional",
            video_type="Training",
            duration_seconds=60,
            description=f"test video for {sector.value}",
        )

        avatar_result = find_best_avatar(brief)
        assert avatar_result["found"] is True, f"No avatar found for sector: {sector.value}"


def test_find_best_avatar_returns_valid_structure(sample_brief):
    result = find_best_avatar(sample_brief)

    assert "found" in result
    assert "score" in result
    assert "asset" in result