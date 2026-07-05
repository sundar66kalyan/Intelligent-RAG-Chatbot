"""
config.py
Configuration settings for the RAG Chatbot application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------------------------------------
# API Configuration
# -------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not found in environment variables.")
    print("Please create a .env file with your Groq API key.")

# -------------------------------------------------
# Model Configuration
# -------------------------------------------------

LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -------------------------------------------------
# RAG Configuration
# -------------------------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3

# -------------------------------------------------
# Path Configuration
# -------------------------------------------------

# Base directory - where this config file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Use relative paths for portability (Step 8)
DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")  # ✅ Writable relative path
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
METADATA_DIR = os.path.join(BASE_DIR, "metadata")

# -------------------------------------------------
# Create Directories if they don't exist
# -------------------------------------------------

def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        DOCUMENTS_DIR,
        VECTOR_DB_DIR,
        PROMPT_DIR,
        METADATA_DIR
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")

# Create directories on import
ensure_directories()

# -------------------------------------------------
# Print Configuration (for debugging)
# -------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("📋 RAG Chatbot Configuration")
    print("=" * 60)
    print(f"GROQ_API_KEY      : {'✅ Set' if GROQ_API_KEY else '❌ Missing'}")
    print(f"LLM_MODEL         : {LLM_MODEL}")
    print(f"EMBEDDING_MODEL   : {EMBEDDING_MODEL}")
    print(f"CHUNK_SIZE        : {CHUNK_SIZE}")
    print(f"CHUNK_OVERLAP     : {CHUNK_OVERLAP}")
    print(f"TOP_K             : {TOP_K}")
    print(f"BASE_DIR          : {BASE_DIR}")
    print(f"DOCUMENTS_DIR     : {DOCUMENTS_DIR}")
    print(f"VECTOR_DB_DIR     : {VECTOR_DB_DIR}")
    print(f"PROMPT_DIR        : {PROMPT_DIR}")
    print(f"METADATA_DIR      : {METADATA_DIR}")
    print("=" * 60)