from typing import TypedDict, Optional

from app.models.assets import VideoBrief, VideoPlan

class VideoCreationState(TypedDict):
    brief: VideoBrief
    video_plan: Optional[VideoPlan]
    reuse_result: Optional[dict]
    provider_decision: Optional[dict]
    cost_estimate: Optional[dict]