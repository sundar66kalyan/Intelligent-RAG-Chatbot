"""
PT005 - ChromaDB Storage Performance Test
"""

import os
import time

import config

from document_loader import (
    load_single_pdf,
    split_single_document
)

from embeddings import get_embedding_model
from langchain_chroma import Chroma

print("=" * 60)
print("CHROMADB STORAGE PERFORMANCE TEST")
print("=" * 60)

# PDF Path
pdf_path = os.path.join(
    config.DOCUMENTS_DIR,
    "Visualisation Assignment.docx.pdf"
)

# Load PDF
docs = load_single_pdf(pdf_path)

# Split PDF
chunks = split_single_document(docs)

# Add test metadata
for chunk in chunks:
    chunk.metadata["document_id"] = "performance_test"

# Load embedding model
embedding_model = get_embedding_model()

# Open ChromaDB
db = Chroma(
    persist_directory=config.VECTOR_DB_DIR,
    embedding_function=embedding_model
)

print(f"Chunks to Store : {len(chunks)}")

start = time.perf_counter()

db.add_documents(chunks)

end = time.perf_counter()

storage_time = end - start

print(f"Storage Time    : {storage_time:.4f} sec")

print(f"Database Count  : {db._collection.count()}")

print("=" * 60)