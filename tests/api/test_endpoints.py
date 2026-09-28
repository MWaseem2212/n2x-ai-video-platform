import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.db import models as db_models
from app.models.assets import VideoPlan


VALID_PAYLOAD = {
    "sector": "adult_care",
    "country": "United Kingdom",
    "audience": "Employees",
    "tone": "Professional, Reassuring",
    "video_type": "Training",
    "duration_seconds": 60,
    "description": "Adult social care video for UK care workers explaining safeguarding",
}


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear() 


@pytest.fixture
def mock_video_planner(monkeypatch):
    """Real Groq LLM ki jagah ek fake, predictable plan (Section 37)"""
    fake_plan = VideoPlan(
        title="Mock Safeguarding Plan",
        proposed_structure=["Scene 1 - 30s", "Scene 2 - 30s"],
        estimated_total_duration=60,
    )
    monkeypatch.setattr("app.graph.nodes.generate_video_plan", lambda brief: fake_plan)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_videos_is_empty_initially(client):
    response = client.get("/videos")
    assert response.status_code == 200
    assert response.json() == []


def test_get_video_returns_404_when_not_found(client):
    response = client.get("/videos/does-not-exist")
    assert response.status_code == 404


def test_create_video_rejects_invalid_sector(client):
    bad_payload = {**VALID_PAYLOAD, "sector": "not_a_real_sector"}
    response = client.post("/create-video", json=bad_payload)
    assert response.status_code == 422


def test_create_video_success(client, mock_video_planner):
    response = client.post("/create-video", json=VALID_PAYLOAD)
    assert response.status_code == 200

    data = response.json()
    assert "video_id" in data
    assert data["video_plan"]["title"] == "Mock Safeguarding Plan"
    assert data["provider_decision"]["recommended"] is not None
    assert data["cost_estimate"]["estimated_total"] >= 0


def test_created_video_appears_in_library(client, mock_video_planner):
    create_response = client.post("/create-video", json=VALID_PAYLOAD)
    video_id = create_response.json()["video_id"]

    list_response = client.get("/videos")
    assert len(list_response.json()) == 1

    detail_response = client.get(f"/videos/{video_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["title"] == "Mock Safeguarding Plan"