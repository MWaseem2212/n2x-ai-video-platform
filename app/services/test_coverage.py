from app.models.assets import VideoBrief, Sector
from app.services.reuse_scorer import calculate_reuse_score

TEST_BRIEFS = [
    VideoBrief(sector=Sector.ADULT_CARE, country="UK", audience="Employees", tone="Professional", video_type="Training", duration_seconds=60, description="adult care safeguarding"),
    VideoBrief(sector=Sector.EARLY_YEARS, country="UK", audience="Parents", tone="Friendly", video_type="Advice", duration_seconds=45, description="early years development tips"),
    VideoBrief(sector=Sector.FOSTERING, country="UK", audience="Foster Carers", tone="Supportive", video_type="Training", duration_seconds=60, description="fostering support guidance"),
    VideoBrief(sector=Sector.CHILDRENS_HOMES, country="UK", audience="Staff", tone="Professional", video_type="Training", duration_seconds=60, description="residential care standards"),
    VideoBrief(sector=Sector.EDUCATION, country="UK", audience="Teachers", tone="Educational", video_type="Training", duration_seconds=60, description="classroom safeguarding"),
    VideoBrief(sector=Sector.CHILDRENS_SOCIAL_WORK, country="UK", audience="Professionals", tone="Professional", video_type="Advice", duration_seconds=60, description="child protection casework"),
    VideoBrief(sector=Sector.ADULT_SOCIAL_WORK, country="UK", audience="Professionals", tone="Professional", video_type="Training", duration_seconds=60, description="adult social work practice"),
    VideoBrief(sector=Sector.LEAVING_CARE, country="UK", audience="Young People", tone="Supportive", video_type="Advice", duration_seconds=45, description="independent living advice"),
    VideoBrief(sector=Sector.OTHER, country="UK", audience="General public", tone="Professional", video_type="Explainer", duration_seconds=45, description="general awareness video"),
]


if __name__ == "__main__":
    print(f"{'Sector':<25} {'Reuse %':<10} {'New %':<10} {'Avatar':<20} {'Voice Found':<12} {'Background'}")
    print("-" * 100)

    for brief in TEST_BRIEFS:
        result = calculate_reuse_score(brief)
        avatar_name = result["breakdown"]["avatar"]["asset_name"] or "None"
        voice_found = result["breakdown"]["voice"]["status"]
        bg_name = result["breakdown"]["background"]["asset_name"] or "None"

        print(f"{brief.sector.value:<25} {result['reuse_score']:<10} {result['new_generation_required']:<10} {avatar_name:<20} {voice_found:<12} {bg_name}")