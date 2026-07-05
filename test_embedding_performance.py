import os
import time

import config

from document_loader import (
    load_single_pdf,
    split_single_document
)

from embeddings import get_embedding_model

print("=" * 60)
print("EMBEDDING PERFORMANCE TEST")
print("=" * 60)

pdf_path = os.path.join(
    config.DOCUMENTS_DIR,
    "Visualisation Assignment.docx.pdf"
)

# Load PDF
docs = load_single_pdf(pdf_path)

# Split into chunks
chunks = split_single_document(docs)

# Load embedding model
embedding_model = get_embedding_model()

texts = [chunk.page_content for chunk in chunks]

start = time.perf_counter()

vectors = embedding_model.embed_documents(texts)

end = time.perf_counter()

print(f"Chunks            : {len(chunks)}")
print(f"Embedding Vectors : {len(vectors)}")
print(f"Embedding Time    : {end-start:.4f} sec")

if vectors:
    print(f"Vector Dimension  : {len(vectors[0])}")

print("=" * 60)