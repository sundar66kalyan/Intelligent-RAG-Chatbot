"""
prompts.py

Prompt templates for the RAG chatbot.
"""

from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_template(
"""
You are an intelligent AI assistant.

Use ONLY the information provided in the context below.

If the answer is not found in the context, reply exactly:

"I could not find the answer in the provided documents."

Do not use outside knowledge.
Do not guess.
Do not hallucinate.

=========================
Context:
{context}
=========================

Question:
{question}

Answer:
"""
)


def get_prompt():
    return RAG_PROMPT


if __name__ == "__main__":

    prompt = get_prompt()

    print("=" * 60)
    print("PROMPT TEMPLATE LOADED")
    print("=" * 60)

    print(prompt)