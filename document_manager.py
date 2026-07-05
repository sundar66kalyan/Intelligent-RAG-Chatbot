"""
document_manager.py

Manage indexed PDF documents.
"""

import os

import config

from metadata_manager import delete_document
from delete_vectors import delete_document_vectors


def remove_document(file_name, file_hash, document_id):
    """
    Remove a document from the system.
    Deletes vectors, metadata, and the physical PDF file.
    """

    # 1. Delete the physical PDF file (if it exists)
    pdf_path = os.path.join(
        config.DOCUMENTS_DIR,
        file_name
    )

    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"✅ Removed PDF file: {file_name}")
        else:
            print(f"ℹ️ PDF already deleted from disk: {file_name}")
    except Exception as e:
        print(f"⚠️ Error removing PDF file: {e}")

    # 2. Remove from metadata (always execute)
    try:
        delete_document(file_hash)
        print(f"✅ Removed metadata for: {file_name}")
    except Exception as e:
        print(f"⚠️ Error removing metadata: {e}")

    # 3. Delete vectors from ChromaDB (always execute)
    try:
        delete_document_vectors(document_id)
        print(f"✅ Removed vectors for: {file_name}")
    except Exception as e:
        print(f"⚠️ Error removing vectors: {e}")

    return True


def remove_document_safe(file_name, file_hash, document_id):
    """
    Safe version of remove_document that catches all exceptions.
    Returns a dict with success status for each step.
    """
    result = {
        "file_deleted": False,
        "metadata_deleted": False,
        "vectors_deleted": False,
        "success": False
    }

    # 1. Delete the physical PDF file
    pdf_path = os.path.join(
        config.DOCUMENTS_DIR,
        file_name
    )

    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            result["file_deleted"] = True
            print(f"✅ Removed PDF file: {file_name}")
        else:
            print(f"ℹ️ PDF already deleted from disk: {file_name}")
            result["file_deleted"] = True  # Already deleted counts as success
    except Exception as e:
        print(f"⚠️ Error removing PDF file: {e}")

    # 2. Remove from metadata
    try:
        delete_document(file_hash)
        result["metadata_deleted"] = True
        print(f"✅ Removed metadata for: {file_name}")
    except Exception as e:
        print(f"⚠️ Error removing metadata: {e}")

    # 3. Delete vectors from ChromaDB
    try:
        delete_document_vectors(document_id)
        result["vectors_deleted"] = True
        print(f"✅ Removed vectors for: {file_name}")
    except Exception as e:
        print(f"⚠️ Error removing vectors: {e}")

    # Overall success if all three steps succeeded
    result["success"] = all([
        result["file_deleted"],
        result["metadata_deleted"],
        result["vectors_deleted"]
    ])

    return result