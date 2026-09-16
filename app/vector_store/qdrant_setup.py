from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

COLLECTIONS = {
    "avatars": 384,     
    "voices": 384,
    "backgrounds": 384,
}


def create_collections():
    existing = [c.name for c in client.get_collections().collections]

    for name, vector_size in COLLECTIONS.items():
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Created collection: {name}")
        else:
            print(f"Collection already exists: {name}")


if __name__ == "__main__":
    create_collections()