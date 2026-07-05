"""
vector_store.py

Create and load Chroma Vector Database
"""

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
        collection_name="rag_documents",
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )


# ----------------------------------------
# Reset Collection
# ----------------------------------------

def reset_collection():
    """
    Reset the Chroma collection by deleting and recreating it.
    """
    db = get_vector_store()

    try:
        db.delete_collection()
        print("🗑️ Deleted existing collection.")
    except Exception as e:
        print(f"ℹ️ No existing collection to delete: {e}")

    print("📁 Created new collection: rag_documents")
    return Chroma(
        collection_name="rag_documents",
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=get_embedding_model()
    )


# ----------------------------------------
# Load Existing Database
# ----------------------------------------

def load_vector_store():
    """
    Load the cached Chroma vector database.
    Returns None if the database directory doesn't exist.
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
    Indexes all documents from metadata into the vector store.
    """

    db = get_vector_store()

    documents = list_documents()

    if len(documents) == 0:
        print("⚠️ No metadata found. Vector store will be empty.")
        return db

    total_chunks = 0

    for doc in documents:

        pdf_path = os.path.join(
            config.DOCUMENTS_DIR,
            doc["file_name"]
        )

        if not os.path.exists(pdf_path):
            print(f"⚠️ Missing PDF: {pdf_path}")
            continue

        docs = load_single_pdf(pdf_path)

        # Check documents before splitting
        if len(docs) == 0:
            print(f"⚠️ No pages extracted from: {pdf_path}")
            continue

        chunks = split_single_document(docs)

        # Check chunks before embedding
        if len(chunks) == 0:
            print(f"⚠️ No chunks created from: {pdf_path}")
            continue

        print(f"📊 Processing: {doc['file_name']} - {len(chunks)} chunks")

        for chunk in chunks:
            chunk.metadata["document_id"] = doc["document_id"]
            chunk.metadata["file_name"] = doc["file_name"]

        # Never insert empty documents
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

    # Check documents before splitting
    if len(docs) == 0:
        print("⚠️ No documents found to update.")
        return None

    chunks = split_documents(docs)

    # Check chunks before embedding
    if len(chunks) == 0:
        print("⚠️ No chunks created from documents.")
        return None

    vector_db = get_vector_store()

    # Never insert empty documents
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

    # Check documents before splitting
    if len(docs) == 0:
        raise ValueError(
            "PDF contains no readable pages."
        )

    chunks = split_single_document(docs)

    # Check chunks before embedding
    if len(chunks) == 0:
        raise ValueError(
            "Uploaded PDF contains no readable text."
        )

    # Add document_id to each chunk's metadata
    for chunk in chunks:
        chunk.metadata["document_id"] = document_id

    db = get_vector_store()

    # Never insert empty documents
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
    Rebuild the entire vector database by resetting the collection
    and re-indexing all documents from metadata.
    """

    print("🔄 Rebuilding Knowledge Base...")

    # Clear cache before rebuild
    st.cache_resource.clear()
    print("🧹 Cleared Streamlit cache before rebuild.")

    # Reset the collection (delete and recreate)
    db = reset_collection()

    documents = list_documents()

    if len(documents) == 0:
        print("⚠️ No documents found in metadata.")
        st.cache_resource.clear()
        print("🧹 Cleared Streamlit cache after rebuild.")
        print("✅ Knowledge Base Rebuilt Successfully (empty)")
        return

    total_chunks = 0

    for doc in documents:

        pdf_path = os.path.join(
            config.DOCUMENTS_DIR,
            doc["file_name"]
        )

        if not os.path.exists(pdf_path):
            print(f"⚠️ Missing PDF: {pdf_path}")
            continue

        docs = load_single_pdf(pdf_path)

        if len(docs) == 0:
            print(f"⚠️ No pages extracted from: {pdf_path}")
            continue

        chunks = split_single_document(docs)

        if len(chunks) == 0:
            print(f"⚠️ No chunks created from: {pdf_path}")
            continue

        print(f"📊 Processing: {doc['file_name']} - {len(chunks)} chunks")

        for chunk in chunks:
            chunk.metadata["document_id"] = doc["document_id"]
            chunk.metadata["file_name"] = doc["file_name"]

        db.add_documents(chunks)
        total_chunks += len(chunks)

    # Clear cache again so a new Chroma object is created with new data
    st.cache_resource.clear()
    print("🧹 Cleared Streamlit cache after rebuild.")

    print(f"✅ Indexed {total_chunks} chunks")
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