"""
delete_vectors.py
"""

from langchain_chroma import Chroma

import config
from embeddings import get_embedding_model


def get_db():

    return Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )


def delete_document_vectors(document_id):

    db = get_db()

    try:

        db._collection.delete(
            where={
                "document_id": document_id
            }
        )

        print(f"Deleted vectors for {document_id}")

        return True

    except Exception as e:

        print(e)

        return False


if __name__ == "__main__":

    db = get_db()

    docs = db.get()

    print("Total Chunks:", len(docs["ids"]))