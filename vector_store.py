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
# Get Vector Store (Cached)
# ----------------------------------------

@st.cache_resource
def get_vector_store():
    """
    Get the Chroma vector database instance.
    Streamlit caches it across reruns to avoid reloading.
    """
    return Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )


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

    return get_vector_store()


# ----------------------------------------
# Create Database
# ----------------------------------------

def create_vector_store():
    """
    Create ChromaDB from metadata.
    If the database already exists, load it instead of rebuilding.
    """

    # ✅ Step 4: Don't rebuild Chroma if it already exists
    if os.path.exists(config.VECTOR_DB_DIR):
        print("📂 Vector database already exists. Loading existing database...")
        return get_vector_store()

    db = get_vector_store()

    documents = list_documents()

    if len(documents) == 0:
        print("⚠️ No documents found in metadata.")
        return db

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

        # ✅ Step 6: Check documents before splitting
        if len(docs) == 0:
            print(f"⚠️ No pages extracted from: {pdf_path}")
            continue

        chunks = split_single_document(docs)

        # ✅ Step 7: Check chunks before embedding
        if len(chunks) == 0:
            print(f"⚠️ No chunks created from: {pdf_path}")
            continue

        print(f"📊 Processing: {doc['file_name']} - {len(chunks)} chunks")

        for chunk in chunks:
            chunk.metadata["document_id"] = doc["document_id"]
            chunk.metadata["file_name"] = doc["file_name"]

        # ✅ Step 5: Never insert empty documents
        if len(chunks) == 0:
            print(f"⚠️ Skipping empty chunks for: {pdf_path}")
            continue

        db.add_documents(chunks)
        total_chunks += len(chunks)

    print(f"✅ Indexed {total_chunks} chunks")

    return db


# ----------------------------------------
# Add New PDFs
# ----------------------------------------

def update_vector_store():

    docs = load_documents()

    # ✅ Step 6: Check documents before splitting
    if len(docs) == 0:
        print("⚠️ No documents found to update.")
        return None

    chunks = split_documents(docs)

    # ✅ Step 7: Check chunks before embedding
    if len(chunks) == 0:
        print("⚠️ No chunks created from documents.")
        return None

    vector_db = get_vector_store()

    # ✅ Step 5: Never insert empty documents
    if len(chunks) == 0:
        print("⚠️ Skipping empty chunks.")
        return vector_db

    vector_db.add_documents(chunks)
    print(f"✅ Added {len(chunks)} chunks to vector store")

    return vector_db


# ----------------------------------------
# Add PDF to Vector DB (with document_id)
# ----------------------------------------

def add_pdf_to_vector_db(pdf_path, document_id):
    """
    Add a single PDF to ChromaDB with document_id in metadata.
    """

    docs = load_single_pdf(pdf_path)

    # ✅ Step 6: Check documents before splitting
    if len(docs) == 0:
        raise ValueError(
            "PDF contains no readable pages."
        )

    chunks = split_single_document(docs)

    # ✅ Step 7: Check chunks before embedding
    if len(chunks) == 0:
        raise ValueError(
            "Uploaded PDF contains no readable text."
        )

    # Add document_id to each chunk's metadata
    for chunk in chunks:
        chunk.metadata["document_id"] = document_id

    db = get_vector_store()

    # ✅ Step 5: Never insert empty documents
    if len(chunks) == 0:
        raise ValueError("No chunks to add to vector store.")

    db.add_documents(chunks)
    print(f"✅ Added {len(chunks)} chunks for document: {document_id}")

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
    """
    Rebuild the entire vector database from scratch.
    """

    print("🔄 Rebuilding Knowledge Base...")

    if os.path.exists(config.VECTOR_DB_DIR):
        shutil.rmtree(config.VECTOR_DB_DIR)
        print("🗑️ Removed old vector database.")

    os.makedirs(config.VECTOR_DB_DIR, exist_ok=True)
    print("📁 Created new vector database directory.")

    create_vector_store()

    # ✅ Clear the cached vector store so it reloads with new data
    st.cache_resource.clear()
    print("🧹 Cleared Streamlit cache.")

    print("✅ Knowledge Base Rebuilt Successfully")


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