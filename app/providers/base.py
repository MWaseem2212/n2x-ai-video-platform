from abc import ABC, abstractmethod

from app.models.assets import VideoBrief

class VideoProvider(ABC):
    @abstractmethod
    def list_avatars(self) -> list[dict]:
        ...
    @abstractmethod
    def estimate_cost(self, brief: VideoBrief) -> float:
        ...

    @abstractmethod
    def create_video(self, brief: VideoBrief) -> dict:
        ...

    @abstractmethod
    def check_status(self, job_id: str) -> str:
        ...
        