"""
PT006 - Retriever Performance Test
"""

import time

from vector_store import get_retriever

print("=" * 60)
print("RETRIEVER PERFORMANCE TEST")
print("=" * 60)

question = "What is the leave policy?"

retriever = get_retriever(k=3)

start = time.perf_counter()

docs = retriever.invoke(question)

end = time.perf_counter()

retrieval_time = end - start

print(f"Question           : {question}")
print(f"Retrieved Chunks   : {len(docs)}")
print(f"Retrieval Time     : {retrieval_time:.4f} sec")

print("\nRetrieved Sources")

for i, doc in enumerate(docs, start=1):

    print("-" * 50)
    print(f"Chunk {i}")

    print(f"Source : {doc.metadata.get('source')}")

    print(f"Page   : {doc.metadata.get('page')}")

print("=" * 60)