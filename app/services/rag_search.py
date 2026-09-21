from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from langchain_qdrant import QdrantVectorStore

from app.vector_store.embeddings import embedding_model
from app.models.assets import VideoBrief

client = QdrantClient(host="localhost", port=6333)


def get_vectorstore(collection_name: str) -> QdrantVectorStore:
    return QdrantVectorStore(client=client, collection_name=collection_name, embedding=embedding_model)


def search_assets(brief: VideoBrief, collection_name: str, query_text: str, top_k: int = 3):
    vectorstore = get_vectorstore(collection_name)
    sector_filter = Filter(
        must=[FieldCondition(key="metadata.sector_suitability", match=MatchAny(any=[brief.sector.value]))]
    )

    return vectorstore.similarity_search_with_score(query_text, k=top_k, filter=sector_filter)


MATCH_THRESHOLD = 0.4

def find_best_avatar(brief: VideoBrief):
    query_text = f"{brief.tone} presenter for {brief.sector.value} sector, {brief.audience} audience"
    results = search_assets(brief, "avatars", query_text, top_k=1)
    if results and results[0][1] >= MATCH_THRESHOLD:
        doc, score = results[0]
        return {"found": True, "score": score, "asset": doc.metadata}
    return {"found": False, "score": results[0][1] if results else 0.0, "asset": None}


def find_best_voice(brief: VideoBrief):
    query_text = f"{brief.tone} tone voice for {brief.sector.value} sector"
    results = search_assets(brief, "voices", query_text, top_k=1)
    if results and results[0][1] >= MATCH_THRESHOLD:
        doc, score = results[0]
        return {"found": True, "score": score, "asset": doc.metadata}
    return {"found": False, "score": results[0][1] if results else 0.0, "asset": None}


def find_best_background(brief: VideoBrief):
    query_text = f"background setting for {brief.sector.value} sector video"
    results = search_assets(brief, "backgrounds", query_text, top_k=1)
    if results and results[0][1] >= MATCH_THRESHOLD:
        doc, score = results[0]
        return {"found": True, "score": score, "asset": doc.metadata}
    return {"found": False, "score": results[0][1] if results else 0.0, "asset": None}


if __name__ == "__main__":
    from app.models.assets import Sector

    test_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining safeguarding",
    )

    print("Avatar:", find_best_avatar(test_brief))
    print("Voice:", find_best_voice(test_brief))
    print("Background:", find_best_background(test_brief))
