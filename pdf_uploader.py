"""
pdf_uploader.py
"""

import os
import time
import config
from vector_store import add_pdf_to_vector_db
from file_hash import calculate_sha256
from metadata_manager import (
    file_exists,
    add_document,
    update_chunk_count
)
from document_loader import (
    load_single_pdf,
    split_single_document
)

def save_uploaded_files(uploaded_files):
    """
    Save uploaded PDF files.
    """

    saved_files = []

    os.makedirs(config.DOCUMENTS_DIR, exist_ok=True)

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            config.DOCUMENTS_DIR,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved_files.append(file_path)

    return saved_files

def process_uploaded_files(uploaded_files):
    """
    Process uploaded PDF files with deduplication.
    Returns: (indexed_files, skipped_files)
    """

    start_upload = time.perf_counter()

    indexed = []
    skipped = []

    os.makedirs(config.DOCUMENTS_DIR, exist_ok=True)

    for uploaded_file in uploaded_files:

        save_path = os.path.join(
            config.DOCUMENTS_DIR,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_hash = calculate_sha256(save_path)

        if file_exists(file_hash):
            skipped.append(uploaded_file.name)
            continue

        # -----------------------------
        # Validate PDF
        # -----------------------------

        try:
            docs = load_single_pdf(save_path)
        except Exception:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise ValueError(
                "Invalid or corrupted PDF file."
            )

        pages = len(docs)

        chunks = split_single_document(docs)

        if len(chunks) == 0:
            os.remove(save_path)
            raise ValueError(
                "Uploaded PDF contains no readable text."
            )

        # -----------------------------
        # Create Metadata
        # -----------------------------

        document_id = add_document(
            file_name=uploaded_file.name,
            file_hash=file_hash,
            pages=pages,
            chunks=0
        )

        # -----------------------------
        # Index into ChromaDB
        # -----------------------------

        try:
            start = time.time()
            
            chunk_count = add_pdf_to_vector_db(
                save_path,
                document_id
            )
            
            end = time.time()

            print("="*60)
            print("INDEXING REPORT")
            print("="*60)
            print("File    :", uploaded_file.name)
            print("Pages   :", pages)
            print("Chunks  :", chunk_count)
            print("Time    :", round(end-start, 2), "sec")
            print("="*60)

        except Exception as e:
            # Remove invalid PDF file
            if os.path.exists(save_path):
                os.remove(save_path)

            # Remove metadata entry that was just created
            from metadata_manager import delete_document
            delete_document(file_hash)

            raise ValueError(str(e))

        # -----------------------------
        # Update Metadata
        # -----------------------------

        update_chunk_count(
            document_id,
            chunk_count
        )

        indexed.append(
            {
                "file": uploaded_file.name,
                "chunks": chunk_count,
                "document_id": document_id
            }
        )

    upload_time = time.perf_counter() - start_upload

    print("="*60)
    print(f"PDF Upload Time : {upload_time:.3f} sec")
    print("="*60)

    return indexed, skipped