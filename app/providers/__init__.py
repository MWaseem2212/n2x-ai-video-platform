from app.providers.base import VideoProvider
from app.providers.mock_heygen import MockHeyGenProvider
from app.providers.mock_synthesia import MockSynthesiaProvider
from app.providers.mock_creatify import MockCreatifyProvider

PROVIDERS: dict[str, VideoProvider] = {
    "heygen": MockHeyGenProvider(),
    "synthesia": MockSynthesiaProvider(),
    "creatify": MockCreatifyProvider(),
}