import random
import uuid

from app.providers.base import VideoProvider
from app.models.assets import VideoBrief

class MockHeyGenProvider(VideoProvider):
    def list_avatars(self) -> list[dict]:
        return [
            {"id": "hg_avatar_001", "name": "Sarah Mitchell"},
            {"id": "hg_avatar_027", "name": "Fatima Al-Rashid"},
        ]

    def estimate_cost(self, brief: VideoBrief) -> float:
        rate_per_second = 0.07
        return round(brief.duration_seconds * rate_per_second, 2)

    def create_video(self, brief: VideoBrief) -> dict:
        job_id = str(uuid.uuid4())
        return {
            "job_id": job_id,
            "provider": "heygen",
            "status": "queued",
            "estimated_completion_seconds": random.randint(30, 90),
        }

    def check_status(self, job_id: str) -> str:
        return "completed"