from app.providers import PROVIDERS
from app.services.provider_selector import select_provider_with_fallback
from app.models.assets import VideoBrief, Sector


if __name__ == "__main__":
    test_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional",
        video_type="Training",
        duration_seconds=60,
        description="test fallback scenario",
    )

    print("=== TEST 1: Normal (all providers available) ===")
    result = select_provider_with_fallback(test_brief)
    print(f"Recommended: {result['recommended']}")
    for log in result["fallback_log"]:
        print(f"  {log}")

    print("\n=== TEST 2: Synthesia marked unavailable ===")
    PROVIDERS["synthesia"].is_available = False

    result = select_provider_with_fallback(test_brief)
    print(f"Recommended: {result['recommended']}")
    for log in result["fallback_log"]:
        print(f"  {log}")

    PROVIDERS["synthesia"].is_available = True

    print("\n=== TEST 3: Synthesia AND HeyGen both unavailable ===")
    PROVIDERS["synthesia"].is_available = False
    PROVIDERS["heygen"].is_available = False

    result = select_provider_with_fallback(test_brief)
    print(f"Recommended: {result['recommended']}")
    for log in result["fallback_log"]:
        print(f"  {log}")

    PROVIDERS["synthesia"].is_available = True
    PROVIDERS["heygen"].is_available = True