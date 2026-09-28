import pytest
from pydantic import ValidationError

from app.models.assets import Avatar, VideoBrief, Sector


def test_video_brief_valid_data(sample_brief):
    assert sample_brief.sector == Sector.ADULT_CARE
    assert sample_brief.duration_seconds == 60


def test_video_brief_rejects_invalid_sector():
    with pytest.raises(ValidationError):
        VideoBrief(
            sector="not_a_real_sector", 
            country="UK",
            audience="Employees",
            tone="Professional",
            video_type="Training",
            duration_seconds=60,
            description="test",
        )


def test_avatar_requires_name():
    with pytest.raises(ValidationError):
        Avatar(provider="heygen", provider_asset_id="hg_001")


def test_avatar_default_previous_usage_is_zero():
    avatar = Avatar(provider="heygen", provider_asset_id="hg_001", name="Test Avatar")
    assert avatar.previous_usage_count == 0