"""
embeddings.py
Loads the embedding model for the RAG pipeline.
"""

import time
from langchain_huggingface import HuggingFaceEmbeddings
import config


def get_embedding_model():
    """
    Load and return the embedding model.
    """

    print("=" * 60)
    print("LOADING EMBEDDING MODEL")
    print("=" * 60)

    start = time.perf_counter()

    embedding_model = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    end = time.perf_counter()

    print(f"Model Loading Time : {end-start:.4f} sec")
    print("=" * 60)

    return embedding_model


if __name__ == "__main__":

    embedding_model = get_embedding_model()

    print("\nModel Loaded Successfully")

    sample_text = "Artificial Intelligence is transforming industries."

    vector = embedding_model.embed_query(sample_text)

    print(f"\nEmbedding Dimension : {len(vector)}")

    print("\nFirst 10 Values:")
    print(vector[:10])