from pydantic import BaseModel
from app.models.assets import VideoPlan

class VideoCreationResponse(BaseModel):
    video_id: str
    video_plan: VideoPlan
    reuse_result: dict
    provider_decision: dict
    cost_estimate: dict