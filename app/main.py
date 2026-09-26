from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.models.assets import VideoBrief
from app.models.api import VideoCreationResponse
from app.graph.run import run_video_creation
from app.db.session import get_db
from app.db.crud import save_video_request, create_video_with_version, get_all_videos, get_video_by_id

app = FastAPI(
    title="N2X AI Video Creation Platform",
    description="Orchestration and reuse engine for AI video generation",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "N2X AI Video Platform"}


@app.post("/create-video", response_model=VideoCreationResponse)
def create_video(brief: VideoBrief, db: Session = Depends(get_db)):
    try:
        result = run_video_creation(brief)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video creation pipeline failed: {str(e)}",
        )

    request_record = save_video_request(db, brief, result)
    video = create_video_with_version(db, brief, result, request_record.id)

    return VideoCreationResponse(
        video_id=video.id,
        video_plan=result["video_plan"],
        reuse_result=result["reuse_result"],
        provider_decision=result["provider_decision"],
        cost_estimate=result["cost_estimate"],
    )


@app.get("/videos")
def list_videos(db: Session = Depends(get_db)):
    videos = get_all_videos(db)
    return [
        {
            "id": v.id,
            "title": v.title,
            "sector": v.sector,
            "provider": v.provider,
            "status": v.status,
            "duration_seconds": v.duration_seconds,
            "created_at": v.created_at,
        }
        for v in videos
    ]


@app.get("/videos/{video_id}")
def get_video(video_id: str, db: Session = Depends(get_db)):
    video = get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return {
        "id": video.id,
        "title": video.title,
        "sector": video.sector,
        "country": video.country,
        "avatar_name": video.avatar_name,
        "provider": video.provider,
        "status": video.status,
        "duration_seconds": video.duration_seconds,
        "created_at": video.created_at,
    }