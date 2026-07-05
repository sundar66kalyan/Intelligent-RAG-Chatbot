"""
Intelligent RAG Chatbot
Created by: KALYANASUNDAR-AI_Engineer
Version: 3.0
"""

import time
import streamlit as st
import os

from rag_pipeline import ask
from vector_store import get_retriever, rebuild_vector_database
from pdf_uploader import process_uploaded_files
from metadata_manager import (
    list_documents,
    total_documents,
    total_pages,
    total_chunks,
    search_documents
)
from document_manager import remove_document
from reindex_document import reindex_document
from preview_document import preview_document
import config

# -------------------------------------------------
# Custom CSS for Premium Animated UI with Better Readability
# -------------------------------------------------

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #1a1a3e, #24243e, #302b63);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism effect */
    .css-1d391kg, .css-12oz5g7, .st-emotion-cache-1v0mbdj {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 12, 41, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Animated main title */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 40%, #c084fc 70%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s ease-in-out infinite;
        background-size: 300% 300%;
        text-align: center;
        padding: 10px 0;
        letter-spacing: -1px;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtitle with better contrast */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.2rem;
        font-weight: 300;
        animation: fadeInUp 1s ease-out;
        letter-spacing: 1px;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* What is this app section - improved readability */
    .app-description {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        margin: 20px 0;
        animation: fadeInUp 1.2s ease-out;
    }
    
    .app-description h2 {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 15px;
    }
    
    .app-description p {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .app-description strong {
        color: #c084fc;
        font-weight: 700;
    }
    
    /* Feature list - improved visibility */
    .feature-list {
        list-style: none;
        padding: 0;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    
    .feature-list li {
        color: rgba(255, 255, 255, 0.92);
        padding: 12px 18px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    .feature-list li:hover {
        background: rgba(129, 140, 248, 0.2);
        border-color: rgba(129, 140, 248, 0.4);
        transform: translateX(5px);
    }
    
    .feature-list li::before {
        content: "✦ ";
        color: #c084fc;
        font-weight: 700;
    }
    
    /* Feature cards with better contrast */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        padding: 15px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .feature-card:nth-child(2) { animation-delay: 0.5s; }
    .feature-card:nth-child(3) { animation-delay: 1s; }
    .feature-card:nth-child(4) { animation-delay: 1.5s; }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 60px rgba(129, 140, 248, 0.3);
        border-color: rgba(129, 140, 248, 0.4);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .feature-icon {
        font-size: 2.8rem;
        display: block;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.05rem;
        margin: 5px 0;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.75);
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* Section headers */
    .section-header {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 15px;
        padding: 10px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #818cf8 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(129, 140, 248, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(129, 140, 248, 0.5) !important;
    }
    
    /* Chat messages with better contrast */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        animation: slideIn 0.6s ease-out;
        padding: 12px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stChatMessage p {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(129, 140, 248, 0.3);
        transform: scale(1.02);
    }
    
    /* Creator credit */
    .creator-section {
        text-align: center;
        padding: 25px;
        margin-top: 30px;
        background: rgba(129, 140, 248, 0.1);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        animation: pulseGlow 3s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 20px rgba(129, 140, 248, 0.1); }
        50% { box-shadow: 0 0 40px rgba(129, 140, 248, 0.2); }
        100% { box-shadow: 0 0 20px rgba(129, 140, 248, 0.1); }
    }
    
    .creator-name {
        font-size: 1.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #818cf8, #7c3aed, #c084fc, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 300%;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .creator-title {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        letter-spacing: 3px;
        font-weight: 300;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    
    /* Upload area */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        transition: all 0.4s ease !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #818cf8 !important;
        background: rgba(129, 140, 248, 0.08) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #818cf8, #7c3aed); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #7c3aed, #c084fc); }
    
    /* Input fields with better contrast */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }
    
    /* Expanders with better contrast */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(129, 140, 248, 0.3) !important;
    }
    
    /* Warning, Success, Info messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* Metric labels */
    .stMetric label {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stMetric .stMetricValue {
        color: #ffffff !important;
    }
    
    /* Chat input */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
    }
    
    .stChatInputContainer input {
        color: #ffffff !important;
    }
    
    .stChatInputContainer input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Intelligent RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:
    # Brand header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="font-size: 4rem; animation: float 3s ease-in-out infinite;">🚀</div>
        <h2 style="color: #ffffff; font-weight: 800; margin: 5px 0; background: linear-gradient(135deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            RAG Chatbot
        </h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.7rem; letter-spacing: 3px; margin-top: 5px;">
            INTELLIGENT DOCUMENT Q&A
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # System status with better contrast
    st.markdown("""
    <div style="background: rgba(255,255,255,0.06); border-radius: 16px; padding: 20px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.7rem; letter-spacing: 2px; margin-bottom: 15px;">⚡ SYSTEM STATUS</p>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="color: rgba(255,255,255,0.8);">LLM</span>
            <span style="color: #34d399; font-size: 0.8rem;">● Llama 3.3</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <span style="color: rgba(255,255,255,0.8);">Embedding</span>
            <span style="color: #60a5fa; font-size: 0.8rem;">● MiniLM L6</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0;">
            <span style="color: rgba(255,255,255,0.8);">Vector DB</span>
            <span style="color: #a78bfa; font-size: 0.8rem;">● ChromaDB</span>
        </div>
        <div style="margin-top: 15px; padding: 8px; background: rgba(52, 211, 153, 0.12); border-radius: 8px; text-align: center;">
            <span style="color: #34d399; font-size: 0.75rem;">● System Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📚 Knowledge Base")

    search_text = st.text_input(
        "🔍 Search Documents",
        placeholder="Type document name..."
    )

    if search_text:
        documents = search_documents(search_text)
    else:
        documents = list_documents()

    if len(documents) == 0:
        st.warning("No matching documents found.")
    else:
        for doc in documents:
            with st.expander(f"📄 {doc['file_name']}"):
                st.write(f"**Pages:** {doc['pages']}")
                st.write(f"**Chunks:** {doc['chunks']}")
                st.write(f"**Status:** {doc['status']}")
                st.write(f"**Uploaded:** {doc['upload_date']}")
                
                st.code(doc["document_id"])
                st.caption(f"SHA256: {doc['file_hash'][:20]}...")
                
                if st.button("👁 Preview", key=f"preview_{doc['document_id']}"):
                    preview = preview_document(doc["file_name"])
                    if preview:
                        st.text_area("First Page Preview", preview[:1500], height=250)
                    else:
                        st.warning("Unable to preview this document.")
                
                pdf_path = os.path.join(config.DOCUMENTS_DIR, doc["file_name"])
                
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button("⬇ Download PDF", data=f, file_name=doc["file_name"], mime="application/pdf", key=f"download_{doc['document_id']}")
                else:
                    st.warning("PDF file not found on disk.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑 Delete", key=f"delete_{doc['document_id']}"):
                        try:
                            result = remove_document(doc["document_id"], doc["file_hash"], doc["file_name"])
                            if isinstance(result, dict):
                                if result.get("success", False):
                                    if result.get("file_deleted", False):
                                        st.success("Document deleted successfully!")
                                    else:
                                        st.warning("PDF file was already missing. Metadata cleaned successfully.")
                                else:
                                    st.warning("Document partially deleted. Check logs for details.")
                            else:
                                st.success("Document deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting document: {str(e)}")
                        st.cache_resource.clear()
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Re-index", key=f"reindex_{doc['document_id']}"):
                        with st.spinner("Re-indexing document..."):
                            try:
                                success = reindex_document(doc["document_id"])
                                if success:
                                    st.success("Document re-indexed successfully.")
                                    st.cache_resource.clear()
                                    st.rerun()
                                else:
                                    st.error("Re-index failed.")
                            except FileNotFoundError:
                                st.warning("⚠ Original PDF not found. Cannot re-index.")
                            except Exception as e:
                                st.error(f"Error during re-indexing: {str(e)}")

    st.markdown("---")

    if st.button("🔄 Rebuild Knowledge Base", use_container_width=True):
        rebuild_vector_database()
        st.success("Knowledge Base rebuilt successfully!")
        st.rerun()

    st.markdown("---")

    st.subheader("📊 Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📄 PDFs", total_documents())
        st.metric("📃 Pages", total_pages())

    with col2:
        st.metric("🧩 Chunks", total_chunks())
        st.metric("🧠 Model", "MiniLM")

    st.markdown("---")

    # Upload section
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h4 style="color: #ffffff; margin: 0;">📄 Upload Documents</h4>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.75rem;">PDF files only</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        with st.spinner("🚀 Building Knowledge Base..."):
            try:
                indexed, skipped = process_uploaded_files(uploaded_files)
            except ValueError as e:
                st.warning(str(e))
                st.stop()

        st.success("Knowledge Base Updated Successfully!")

        for item in indexed:
            st.success(f"✅ {item['file']} ({item['chunks']} chunks indexed)")

        if skipped:
            st.warning(f"{len(skipped)} duplicate PDF(s) skipped.")
            for file in skipped:
                st.write("⚠", file)

        st.cache_resource.clear()

    st.markdown("---")

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Creator section in sidebar
    st.markdown("""
    <div class="creator-section" style="margin-top: 30px;">
        <p style="color: rgba(255,255,255,0.4); font-size: 0.6rem; letter-spacing: 3px;">CREATED BY</p>
        <p class="creator-name" style="font-size: 1.1rem;">KALYANASUNDAR</p>
        <p style="color: rgba(255,255,255,0.4); font-size: 0.6rem; letter-spacing: 2px;">AI ENGINEER</p>
        <div style="margin-top: 10px; display: flex; justify-content: center; gap: 10px;">
            <span style="color: rgba(255,255,255,0.2); font-size: 0.5rem;">⚡</span>
            <span style="color: rgba(255,255,255,0.2); font-size: 0.5rem;">🔮</span>
            <span style="color: rgba(255,255,255,0.2); font-size: 0.5rem;">🚀</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Main Content
# -------------------------------------------------

# Animated header
st.markdown("""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 class="main-title">Intelligent RAG Chatbot</h1>
    <p class="subtitle">Ask questions from your PDF documents with AI-powered intelligence</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# What is this app? Section
# -------------------------------------------------

st.markdown("""
<div class="app-description">
    <h2>🚀 What is Intelligent RAG Chatbot?</h2>
    <p>
        <strong>Intelligent RAG Chatbot</strong> is a cutting-edge document Q&A system that leverages 
        <strong>Retrieval-Augmented Generation (RAG)</strong> to provide intelligent, context-aware answers 
        from your PDF documents. This advanced technology combines the power of <strong>Groq's Llama 3.3</strong> 
        language model with the retrieval capabilities of RAG, enabling it to deliver accurate, context-aware 
        responses with high precision.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Features Section
# -------------------------------------------------

with st.expander("✨ Key Features - Click to Expand", expanded=True):
    
    st.markdown("""
    <div style="padding: 10px 0;">
        <h3 style="color: #ffffff; font-weight: 700; margin-bottom: 15px;">📋 What This App Can Do For You:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature list as bullet points with better visibility
    st.markdown("""
    <ul class="feature-list">
        <li>📄 Upload multiple PDF documents with automatic text extraction</li>
        <li>🔍 Search through your documents using semantic similarity</li>
        <li>💬 Ask natural language questions and get AI-powered answers</li>
        <li>🧠 Retrieve relevant document chunks using RAG pipeline</li>
        <li>⚡ Powered by Groq's Llama 3.3 for fast, accurate responses</li>
        <li>🗄️ ChromaDB vector database for efficient document storage</li>
        <li>📊 View real-time statistics (PDFs, Pages, Chunks)</li>
        <li>👁️ Preview document content before asking questions</li>
        <li>⬇️ Download PDF files directly from the interface</li>
        <li>🗑️ Delete documents with automatic cleanup of vectors & metadata</li>
        <li>🔄 Re-index individual documents or rebuild entire knowledge base</li>
        <li>📝 View source documents and page references for each answer</li>
        <li>⏱️ Track response time for performance monitoring</li>
        <li>🚀 Smart deduplication prevents duplicate file uploads</li>
    </ul>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("""
    <div style="padding: 10px 0;">
        <h3 style="color: #ffffff; font-weight: 700; margin-bottom: 15px;">🎯 Core Capabilities:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📄</span>
            <div class="feature-title">Upload & Manage</div>
            <div class="feature-desc">Upload, preview, download, and delete PDF documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🧠</span>
            <div class="feature-title">RAG Pipeline</div>
            <div class="feature-desc">Retrieval-Augmented Generation for AI-powered answers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💬</span>
            <div class="feature-title">Interactive Chat</div>
            <div class="feature-desc">Ask questions and get AI-powered responses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <div class="feature-title">Smart Search</div>
            <div class="feature-desc">Search documents with context-aware responses</div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# Chat Interface
# -------------------------------------------------

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("💬 Ask a question about your documents...")

if question is not None:
    question = question.strip()

    if question == "":
        st.warning("⚠ Please enter a question.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching documents..."):
            start = time.time()
            answer = ask(question)
            end = time.time()

            st.markdown(answer)
            st.caption(f"⏱️ Response Time: {round(end-start, 2)} sec")

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Source documents
    retriever = get_retriever()

    if retriever is not None:
        docs = retriever.invoke(question)

        with st.expander("📚 Source Documents"):
            for i, doc in enumerate(docs, 1):
                st.markdown(f"### 📄 Document {i}")
                st.write(f"**Source:** {doc.metadata['source']}")
                st.write(f"**Page:** {doc.metadata['page']}")
                st.write("**Content Preview:**")
                st.write(doc.page_content[:400])
                st.markdown("---")
    else:
        with st.expander("📚 Source Documents"):
            st.info("📝 No documents have been indexed yet. Upload some PDFs to get started.")

# -------------------------------------------------
# Footer with Creator Credit
# -------------------------------------------------

st.markdown("""
<div style="text-align: center; padding: 30px 0 10px 0; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.06);">
    <p style="color: rgba(255,255,255,0.3); font-size: 0.7rem; letter-spacing: 2px;">
        BUILT WITH ❤️ BY 
        <span style="background: linear-gradient(135deg, #818cf8, #7c3aed, #c084fc, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1rem;">
            KALYANASUNDAR-AI ENGINEER
        </span>
    </p>
    <p style="color: rgba(255,255,255,0.15); font-size: 0.6rem; letter-spacing: 1px; margin-top: 5px;">
        © 2026 • INTELLIGENT RAG CHATBOT • POWERED BY STREAMLIT & GROQ
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px;">
        <span style="color: rgba(255,255,255,0.1); font-size: 0.5rem;">✦</span>
        <span style="color: rgba(255,255,255,0.1); font-size: 0.5rem;">✦</span>
        <span style="color: rgba(255,255,255,0.1); font-size: 0.5rem;">✦</span>
    </div>
</div>
""", unsafe_allow_html=True)