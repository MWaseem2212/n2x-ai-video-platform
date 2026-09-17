import json
from pathlib import Path

from qdrant_client.models import PointStruct

from app.models.assets import Avatar, Voice, Background
from app.vector_store.qdrant_setup import client
from app.vector_store.embeddings import embed_text

SEED_DIR = Path("seed_data")

def build_avatar_text(avatar: Avatar) -> str:
    sectors = ", ".join(avatar.sector_suitability)
    return (
        f"Avatar {avatar.name}. {avatar.appearance}."
        f"Accent: {avatar.accent}. Country: {avatar.country}"
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
        f"Backgound category: {bg.category}. {bg.environment}. "
        f"Style: {bg.style}. Suitable for sectors: {sectors}."
    )

def ingest_avatars():
    data = json.loads((SEED_DIR / "avatars.json").read_text())
    points = []

    for i, raw in enumerate(data):
        avatar = Avatar(**raw)
        text = build_avatar_text(avatar)
        vector = embed_text(text)

        points.append(
            PointStruct(
                id = str(avatar.id),
                vector=vector,
                payload = avatar.model_dump(mode="json")
            )
        )
    client.upsert(collection_name="avatars", points=points)
    print(f"Ingested {len(points)} avatars")

def ingest_voices():
    data = json.loads((SEED_DIR / "voices.json").read_text())
    points = []

    for raw in data:
        voice = Voice(**raw)
        text = build_voice_text(voice)
        vector = embed_text(text)

        points.append(
            PointStruct(
                id=str(voice.id),
                vector=vector,
                payload=voice.model_dump(mode="json"),
            )
        )

    client.upsert(collection_name="voices", points=points)
    print(f"Ingested {len(points)} voices")


def ingest_backgrounds():
    data = json.loads((SEED_DIR / "backgrounds.json").read_text())
    points = []

    for raw in data:
        bg = Background(**raw)
        text = build_background_text(bg)
        vector = embed_text(text)

        points.append(
            PointStruct(
                id=str(bg.id),
                vector=vector,
                payload=bg.model_dump(mode="json"),
            )
        )

    client.upsert(collection_name="backgrounds", points=points)
    print(f"Ingested {len(points)} backgrounds")


if __name__ == "__main__":
    ingest_avatars()
    ingest_voices()
    ingest_backgrounds()