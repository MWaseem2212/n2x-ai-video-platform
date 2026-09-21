from app.providers import PROVIDERS
from app.models.assets import VideoBrief, Sector


if __name__ == "__main__":
    brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="UK",
        audience="Employees",
        tone="Professional",
        video_type="Training",
        duration_seconds=60,
        description="test",
    )

    for name, provider in PROVIDERS.items():
        print(name, "->", provider.estimate_cost(brief))