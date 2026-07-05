"""
PT008 - End-to-End Pipeline Performance Test
"""

import time

from rag_pipeline import ask

print("=" * 60)
print("END-TO-END PIPELINE PERFORMANCE TEST")
print("=" * 60)

question = "What is the leave policy?"

print(f"Question : {question}")

start = time.perf_counter()

answer = ask(question)

end = time.perf_counter()

pipeline_time = end - start

print("\nGenerated Answer\n")
print(answer)

print("\n" + "=" * 60)
print(f"Complete Pipeline Time : {pipeline_time:.4f} sec")
print("=" * 60)