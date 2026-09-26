import uuid
from datetime import datetime

from sqlalchemy import String, Float, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class VideoRequestRecord(Base):
    __tablename__ = "video_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    sector: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[int] = mapped_column(Integer)

    video_plan_title: Mapped[str] = mapped_column(String)

    provider: Mapped[str] = mapped_column(String)
    reuse_score: Mapped[int] = mapped_column(Integer)
    new_generation_required: Mapped[int] = mapped_column(Integer)
    provider_generation_cost: Mapped[float] = mapped_column(Float)
    internal_processing_cost: Mapped[float] = mapped_column(Float)
    estimated_total: Mapped[float] = mapped_column(Float)
    estimated_cost_without_reuse: Mapped[float] = mapped_column(Float)
    rag_saving_amount: Mapped[float] = mapped_column(Float)
    rag_saving_percentage: Mapped[int] = mapped_column(Integer)

    reuse_breakdown: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    title: Mapped[str] = mapped_column(String)
    sector: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    avatar_name: Mapped[str] = mapped_column(String, nullable=True)
    provider: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String, default="Draft")

    thumbnail_url: Mapped[str] = mapped_column(String, nullable=True)
    video_url: Mapped[str] = mapped_column(String, nullable=True)

    request_id: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class VideoVersion(Base):
    __tablename__ = "video_versions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    video_id: Mapped[str] = mapped_column(String)

    version_number: Mapped[int] = mapped_column(Integer)
    
    change_description: Mapped[str] = mapped_column(String)
    previous_value: Mapped[str] = mapped_column(String, nullable=True)
    new_value: Mapped[str] = mapped_column(String, nullable=True)
    additional_cost: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)