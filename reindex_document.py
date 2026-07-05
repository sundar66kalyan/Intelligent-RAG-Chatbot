"""
reindex_document.py

Re-index one PDF document
"""

import os

import config

from delete_vectors import delete_document_vectors
from vector_store import add_pdf_to_vector_db
from metadata_manager import (
    update_chunks,
    list_documents
)


def reindex_document(document_id):
    """
    Re-index one document.
    Returns True if successful, False otherwise.
    """

    documents = list_documents()

    document = None

    for doc in documents:

        if doc["document_id"] == document_id:
            document = doc
            break

    if document is None:
        print(f"❌ Document not found: {document_id}")
        return False

    pdf_path = os.path.join(
        config.DOCUMENTS_DIR,
        document["file_name"]
    )

    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Original PDF not found: {pdf_path}")
        raise FileNotFoundError(
            f"Original PDF not found:\n{pdf_path}"
        )

    try:
        # Delete old vectors
        print(f"🔄 Deleting old vectors for: {document['file_name']}")
        delete_document_vectors(document_id)

        # Add new vectors
        print(f"🔄 Indexing new vectors for: {document['file_name']}")
        chunk_count = add_pdf_to_vector_db(
            pdf_path,
            document_id
        )

        # Update metadata
        print(f"🔄 Updating metadata for: {document['file_name']}")
        update_chunks(
            document_id,
            chunk_count
        )

        print(f"✅ Successfully re-indexed: {document['file_name']} ({chunk_count} chunks)")
        return True

    except Exception as e:
        print(f"❌ Error re-indexing document: {str(e)}")
        raise


def reindex_document_safe(document_id):
    """
    Safe version of reindex_document that catches all exceptions.
    Returns (success, error_message).
    """
    try:
        success = reindex_document(document_id)
        return success, None
    except FileNotFoundError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Re-index failed: {str(e)}"


if __name__ == "__main__":
    # Test the reindex function
    import sys
    
    if len(sys.argv) > 1:
        doc_id = sys.argv[1]
        print(f"Re-indexing document: {doc_id}")
        try:
            result = reindex_document(doc_id)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage: python reindex_document.py <document_id>")