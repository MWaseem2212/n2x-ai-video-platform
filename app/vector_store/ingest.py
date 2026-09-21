import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from app.models.assets import Avatar, Voice, Background
from app.vector_store.embeddings import embedding_model

SEED_DIR = Path("seed_data")
QDRANT_URL = "http://localhost:6333"


def build_avatar_text(avatar: Avatar) -> str:
    sectors = ", ".join(avatar.sector_suitability)
    return (
        f"Avatar {avatar.name}. {avatar.appearance}. "
        f"Accent: {avatar.accent}. Country: {avatar.country}. "
        f"Suitable for sectors: {sectors}. Style: {avatar.pose_style}."
    )


def build_voice_text(voice: Voice) -> str:
    sectors = ", ".join(voice.sector_suitability)
    return (
        f"Voice with {voice.accent} accent, tone: {voice.tone}, "
        f"style: {voice.style}. Suitable for sectors: {sectors}."
    )


def build_background_text(bg: Background) -> str:
    sectors = ", ".join(bg.sector_suitability)
    return (
        f"Background category: {bg.category}. {bg.environment}. "
        f"Style: {bg.style}. Suitable for sectors: {sectors}."
    )


def ingest_avatars():
    data = json.loads((SEED_DIR / "avatars.json").read_text())
    documents = [
        Document(page_content=build_avatar_text(Avatar(**raw)), metadata=Avatar(**raw).model_dump(mode="json"))
        for raw in data
    ]
    QdrantVectorStore.from_documents(
        documents, embedding_model, url=QDRANT_URL, collection_name="avatars"
    )
    print(f"Ingested {len(documents)} avatars")


def ingest_voices():
    data = json.loads((SEED_DIR / "voices.json").read_text())
    documents = [
        Document(page_content=build_voice_text(Voice(**raw)), metadata=Voice(**raw).model_dump(mode="json"))
        for raw in data
    ]
    QdrantVectorStore.from_documents(
        documents, embedding_model, url=QDRANT_URL, collection_name="voices"
    )
    print(f"Ingested {len(documents)} voices")


def ingest_backgrounds():
    data = json.loads((SEED_DIR / "backgrounds.json").read_text())
    documents = [
        Document(page_content=build_background_text(Background(**raw)), metadata=Background(**raw).model_dump(mode="json"))
        for raw in data
    ]
    QdrantVectorStore.from_documents(
        documents, embedding_model, url=QDRANT_URL, collection_name="backgrounds"
    )
    print(f"Ingested {len(documents)} backgrounds")


if __name__ == "__main__":
    ingest_avatars()
    ingest_voices()
    ingest_backgrounds()
