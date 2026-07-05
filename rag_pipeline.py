"""
rag_pipeline.py

Complete RAG Pipeline
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_groq import ChatGroq

import config
import groq

from prompts import get_prompt
from vector_store import get_retriever


# ----------------------------------------
# Prompt
# ----------------------------------------

prompt = get_prompt()


# ----------------------------------------
# Helper
# ----------------------------------------

def format_docs(docs):
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


# ----------------------------------------
# LLM Factory
# ----------------------------------------

def get_llm():
    """
    Create and return a ChatGroq LLM instance.
    The LLM is created only when this function is called.
    """
    return ChatGroq(
        model=config.LLM_MODEL,
        temperature=0
    )


# ----------------------------------------
# Chat Function
# ----------------------------------------

def ask(question):
    """
    Process a question through the RAG pipeline with error handling.
    The LLM is created on-demand to catch API key errors at runtime.
    The retriever is fetched fresh each time to avoid stale cache.
    """
    try:
        # ✅ FIX 4: Get a fresh retriever every time
        retriever = get_retriever(config.TOP_K)
        
        # ✅ FIX 4: Check if retriever exists
        if retriever is None:
            return "📝 Knowledge base is empty. Please upload some PDF documents first."
        
        # Get retriever context
        docs = retriever.invoke(question)
        context = format_docs(docs)
        
        # Create LLM instance (created here to catch auth errors)
        llm = get_llm()
        
        # Build chain with the new LLM instance
        rag_chain = (
            {
                "context": RunnablePassthrough(),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Invoke the chain
        answer = rag_chain.invoke({
            "context": context,
            "question": question
        })
        
        return answer

    except groq.GroqError:
        return (
            "❌ GROQ_API_KEY is missing or invalid.\n\n"
            "Please configure your API key in the .env file."
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("RAG PIPELINE READY")
    print("=" * 60)

    while True:

        q = input("\nQuestion : ")

        if q.lower() == "exit":
            break

        answer = ask(q)

        print()
        print(answer)