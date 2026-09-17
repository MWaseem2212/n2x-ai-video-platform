from app.vector_store.qdrant_setup import client
from app.vector_store.embeddings import embed_text


def search(collection_name: str, query: str, top_k: int = 3):
    query_vector = embed_text(query)

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
    )

    print(f"\nQuery: '{query}' -> Collection: {collection_name}")
    for point in results.points:
        name = point.payload.get("name") or point.payload.get("category") or point.payload.get("tone")
        print(f"  Score: {point.score:.3f} | {name} | id={point.id}")


if __name__ == "__main__":
    search("avatars", "reassuring presenter for UK adult care safeguarding video")
    search("avatars", "energetic presenter for early years nursery content")
    search("backgrounds", "calm care home setting for elderly residents")
    search("voices", "professional reassuring tone for social care")