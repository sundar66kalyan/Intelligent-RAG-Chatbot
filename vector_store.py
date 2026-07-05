"""
vector_store.py

Create and load Chroma Vector Database
"""

import shutil
import os
import streamlit as st
from langchain_chroma import Chroma

from embeddings import get_embedding_model
from document_loader import load_documents, split_documents
import config

from document_loader import (
    load_single_pdf,
    split_single_document
)

from metadata_manager import list_documents


# ----------------------------------------
# Load Existing Database (Cached)
# ----------------------------------------

@st.cache_resource
def load_vector_store():
    """
    Load the Chroma vector database if it exists.
    Returns None if the database directory doesn't exist.
    Streamlit caches it across reruns.
    """

    if not os.path.exists(config.VECTOR_DB_DIR):
        return None

    return Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )


# ----------------------------------------
# Create Database
# ----------------------------------------

def create_vector_store():
    """
    Create ChromaDB from metadata.
    """

    db = Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )

    documents = list_documents()

    total_chunks = 0

    for doc in documents:

        pdf_path = os.path.join(
            config.DOCUMENTS_DIR,
            doc["file_name"]
        )

        if not os.path.exists(pdf_path):
            print(f"Missing PDF: {pdf_path}")
            continue

        docs = load_single_pdf(pdf_path)

        chunks = split_single_document(docs)

        if len(chunks) == 0:
            print(f"Warning: PDF contains no readable text: {pdf_path}")
            continue

        for chunk in chunks:

            chunk.metadata["document_id"] = doc["document_id"]
            chunk.metadata["file_name"] = doc["file_name"]

        db.add_documents(chunks)

        total_chunks += len(chunks)

    print(f"Indexed {total_chunks} chunks")

    return db


# ----------------------------------------
# Add New PDFs
# ----------------------------------------

def update_vector_store():

    docs = load_documents()

    chunks = split_documents(docs)

    vector_db = Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )

    vector_db.add_documents(chunks)

    return vector_db


# ----------------------------------------
# Add PDF to Vector DB (with document_id)
# ----------------------------------------

def add_pdf_to_vector_db(pdf_path, document_id):
    """
    Add a single PDF to ChromaDB with document_id in metadata.
    """

    docs = load_single_pdf(pdf_path)

    chunks = split_single_document(docs)

    # Add document_id to each chunk's metadata
    if len(chunks) == 0:
        raise ValueError(
            "Uploaded PDF contains no readable text."
        )

    for chunk in chunks:
        chunk.metadata["document_id"] = document_id

    db = Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )

    db.add_documents(chunks)

    return len(chunks)


# ----------------------------------------
# Retriever
# ----------------------------------------

def get_retriever(k=3):
    """
    Get a retriever from the vector database.
    Returns None if the database doesn't exist.
    """

    db = load_vector_store()

    if db is None:
        return None

    return db.as_retriever(
        search_kwargs={"k": k}
    )


# ----------------------------------------
# Rebuild Vector Database
# ----------------------------------------

def rebuild_vector_database():

    if os.path.exists(config.VECTOR_DB_DIR):
        shutil.rmtree(config.VECTOR_DB_DIR)

    os.makedirs(config.VECTOR_DB_DIR, exist_ok=True)

    create_vector_store()

    # Clear the cached vector store so it reloads with new data
    st.cache_resource.clear()

    print("Knowledge Base Rebuilt Successfully")


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    db = load_vector_store()

    if db is None:
        print("="*60)
        print("No vector database found. Please index some documents first.")
        print("="*60)
    else:
        print("="*60)
        print("Vector Database Loaded")
        print("="*60)
        print("Chunks :", db._collection.count())