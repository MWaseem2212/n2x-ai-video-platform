from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class Sector(str, Enum):
    ADULT_CARE = "adult_care"
    EARLY_YEARS = "early_years"
    FOSTERING = "fostering"
    CHILDERNS_HOMES = "childrens_homes"
    EDUCATION = "education"
    CHILDRENS_SOCIAL_WORK = "childrens_social_work"
    ADULT_SOCIAL_WORK = "adult_social_work"
    LEAVING_CARE = "leaving_care"
    OTHER = "other"

class AssetBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    provider: str 
    provider_asset_id: str
    sector_suitability: list[Sector] = []
    country: str | None = None
    culture: str | None = None
    previous_usage_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Avatar(AssetBase):
    name: str
    appearance: str | None = None
    gender_presentation: str | None = None
    approximate_age_style: str | None = None
    accent: str | None = None
    language: str = "en"
    clothing: str | None = None
    pose_style: str | None = None
    example_video_urls: list[str] = []

class Voice(AssetBase):
    language: str = "en"
    accent: str | None = None
    tone: str | None = None            
    gender_presentation: str | None = None
    speed: float = 1.0
    style: str | None = None

class Background(AssetBase):
    category: str                       
    environment: str | None = None
    style: str | None = None
    color_palette: str | None = None
    aspect_ratio: str = "16:9"
    media_url: str 

class Script(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    full_script: str
    scene_scripts: list[str] = []
    subject: str
    sector: Sector
    country: str | None = None
    tone: str | None = None
    audience: str | None = None
    keywords: list[str] = []
    version: int = 1
    previous_usage_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VideoBrief(BaseModel):
    sector: Sector
    country: str
    audience: str
    tone: str
    culture: str | None = None          
    video_format: str = "16:9"
    duration_seconds: int
    description: str  