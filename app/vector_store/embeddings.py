from fastembed import TextEmbedding

_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def embed_text(text: str) -> list[float]:
    embeddings = list(_model.embed([text]))
    return embeddings[0].tolist()


if __name__ == "__main__":
    vector = embed_text("reassuring adult care presenter for UK safeguarding video")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 numbers: {vector[:5]}")