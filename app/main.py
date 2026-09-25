from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.models.assets import VideoBrief
from app.models.api import VideoCreationResponse
from app.graph.run import run_video_creation
from app.db.session import get_db
from app.db.crud import save_video_request

app = FastAPI(
    title="N2X AI Video Creation Platform",
    description="Orchestration and reuse engine for AI video generation"
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

    save_video_request(db, brief, result)

    return VideoCreationResponse(
        video_plan=result["video_plan"],
        reuse_result=result["reuse_result"],
        provider_decision=result["provider_decision"],
        cost_estimate=result["cost_estimate"],
    )