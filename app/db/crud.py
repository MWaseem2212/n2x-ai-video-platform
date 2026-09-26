from sqlalchemy.orm import Session

from app.db.models import VideoRequestRecord
from app.models.assets import VideoBrief
from app.db.models import Video, VideoVersion

def save_video_request(db: Session, brief: VideoBrief, result: dict) -> VideoRequestRecord:
    record = VideoRequestRecord(
        sector=brief.sector.value,
        country=brief.country,
        description=brief.description,
        duration_seconds=brief.duration_seconds,
        video_plan_title=result["video_plan"].title,
        provider=result["provider_decision"]["recommended"],
        reuse_score=result["reuse_result"]["reuse_score"],
        new_generation_required=result["reuse_result"]["new_generation_required"],
        provider_generation_cost=result["cost_estimate"]["provider_generation_cost"],
        internal_processing_cost=result["cost_estimate"]["internal_processing_cost"],
        estimated_total=result["cost_estimate"]["estimated_total"],
        estimated_cost_without_reuse=result["cost_estimate"]["estimated_cost_without_reuse"],
        rag_saving_amount=result["cost_estimate"]["rag_saving_amount"],
        rag_saving_percentage=result["cost_estimate"]["rag_saving_percentage"],
        reuse_breakdown=result["reuse_result"]["breakdown"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record



def create_video_with_version(db: Session, brief: VideoBrief, result: dict, request_id: str) -> Video:
    avatar_info = result["reuse_result"]["breakdown"]["avatar"]

    video = Video(
        title=result["video_plan"].title,
        sector=brief.sector.value,
        country=brief.country,
        avatar_name=avatar_info["asset_name"],
        provider=result["provider_decision"]["recommended"],
        duration_seconds=brief.duration_seconds,
        status="Ready for Review",
        request_id=request_id,
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    version = VideoVersion(
        video_id=video.id,
        version_number=1,
        change_description="Original creation",
        previous_value=None,
        new_value=None,
        additional_cost=result["cost_estimate"]["estimated_total"],
    )
    db.add(version)
    db.commit()

    return video

def get_all_videos(db: Session):
    return db.query(Video).order_by(Video.created_at.desc()).all()


def get_video_by_id(db: Session, video_id: str):
    return db.query(Video).filter(Video.id == video_id).first()