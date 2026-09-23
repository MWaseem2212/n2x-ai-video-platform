from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models.assets import VideoBrief
from app.models.api import VideoCreationResponse
from app.graph.run import run_video_creation

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
def create_video(brief: VideoBrief):
    """
    Section 46, 50 — Ye humara core endpoint hai. Client ek VideoBrief
    bhejta hai, hum poora LangGraph pipeline chalate hain, structured
    result wapas karte hain.
    """
    try:
        result = run_video_creation(brief)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video creation pipeline failed: {str(e)}",
        )

    return VideoCreationResponse(
        video_plan=result["video_plan"],
        reuse_result=result["reuse_result"],
        provider_decision=result["provider_decision"],
        cost_estimate=result["cost_estimate"],
    )