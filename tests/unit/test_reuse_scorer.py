from app.services.reuse_scorer import calculate_reuse_score, get_asset_label


def test_reuse_score_returns_valid_percentage_range(sample_brief):
    result = calculate_reuse_score(sample_brief)

    assert 0 <= result["reuse_score"] <= 100
    assert 0 <= result["new_generation_required"] <= 100
    assert result["reuse_score"] + result["new_generation_required"] == 100


def test_reuse_score_has_breakdown_for_all_components(sample_brief):
    result = calculate_reuse_score(sample_brief)

    assert "avatar" in result["breakdown"]
    assert "voice" in result["breakdown"]
    assert "background" in result["breakdown"]


def test_get_asset_label_voice_uses_tone_and_accent():
    voice_asset = {"tone": "reassuring", "accent": "British RP"}
    label = get_asset_label("voice", voice_asset)

    assert "reassuring" in label
    assert "British RP" in label


def test_get_asset_label_returns_none_for_missing_asset():
    label = get_asset_label("avatar", None)
    assert label is None