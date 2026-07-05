"""
metadata_manager.py

Manage metadata for indexed PDFs.
"""

import json
import os
from datetime import datetime

from document_id import generate_document_id

METADATA_DIR = "metadata"
METADATA_FILE = os.path.join(
    METADATA_DIR,
    "indexed_files.json"
)


def initialize_metadata():

    os.makedirs(METADATA_DIR, exist_ok=True)

    if not os.path.exists(METADATA_FILE):

        with open(METADATA_FILE, "w") as f:

            json.dump([], f, indent=4)


def load_metadata():

    initialize_metadata()

    with open(METADATA_FILE, "r") as f:

        return json.load(f)


def save_metadata(data):

    with open(METADATA_FILE, "w") as f:

        json.dump(data, f, indent=4)


def file_exists(file_hash):

    data = load_metadata()

    for item in data:

        if item["file_hash"] == file_hash:

            return True

    return False


def add_document(
    file_name,
    file_hash,
    pages,
    chunks
):

    data = load_metadata()

    document_id = generate_document_id(file_name)

    record = {

        "document_id": document_id,

        "file_name": file_name,

        "file_hash": file_hash,

        "pages": pages,

        "chunks": chunks,

        "upload_date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "status": "Indexed"

    }

    data.append(record)

    save_metadata(data)

    return document_id


def update_chunk_count(document_id, chunk_count):
    """
    Update the chunk count for a document by its document_id.
    """

    data = load_metadata()

    for item in data:

        if item["document_id"] == document_id:

            item["chunks"] = chunk_count

            break

    save_metadata(data)


def update_chunks(document_id, chunks):
    """
    Update the chunks for a document by its document_id.
    """

    documents = list_documents()

    for doc in documents:

        if doc["document_id"] == document_id:

            doc["chunks"] = chunks

            break

    save_metadata(documents)


def list_documents():

    return load_metadata()


def total_documents():

    return len(load_metadata())


def total_chunks():

    data = load_metadata()

    return sum(
        item["chunks"] for item in data
    )


def total_pages():

    data = load_metadata()

    return sum(
        item["pages"] for item in data
    )


def search_documents(keyword):
    """
    Search indexed documents by filename.
    """

    keyword = keyword.lower()

    data = load_metadata()

    results = []

    for item in data:

        if keyword in item["file_name"].lower():

            results.append(item)

    return results


def delete_document(file_hash):
    """
    Remove a document from metadata using its hash.
    """

    data = load_metadata()

    data = [
        item
        for item in data
        if item["file_hash"] != file_hash
    ]

    save_metadata(data)


def remove_document_by_hash(file_hash):
    """
    Alias for delete_document - removes a document by file_hash.
    """
    return delete_document(file_hash)


def remove_document_by_id(document_id):
    """
    Remove a document from metadata using its document_id.
    """

    data = load_metadata()

    data = [
        item
        for item in data
        if item["document_id"] != document_id
    ]

    save_metadata(data)


if __name__ == "__main__":

    initialize_metadata()

    print("="*60)
    print("Metadata Manager Ready")
    print("="*60)

    print(load_metadata())