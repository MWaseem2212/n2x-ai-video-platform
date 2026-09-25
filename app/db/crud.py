from sqlalchemy.orm import Session

from app.db.models import VideoRequestRecord
from app.models.assets import VideoBrief


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