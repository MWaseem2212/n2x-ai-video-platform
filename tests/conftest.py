import pytest

from app.models.assets import VideoBrief, Sector


@pytest.fixture
def sample_brief() -> VideoBrief:
    return VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining safeguarding",
    )