import random
import uuid

from app.providers.base import VideoProvider
from app.models.assets import VideoBrief


class MockCreatifyProvider(VideoProvider):

    def list_avatars(self) -> list[dict]:
        return []

    def estimate_cost(self, brief: VideoBrief) -> float:
        rate_per_second = 0.05
        return round(brief.duration_seconds * rate_per_second, 2)

    def create_video(self, brief: VideoBrief) -> dict:
        job_id = str(uuid.uuid4())
        return {
            "job_id": job_id,
            "provider": "creatify",
            "status": "queued",
            "estimated_completion_seconds": random.randint(20, 60),
        }

    def check_status(self, job_id: str) -> str:
        return "completed"