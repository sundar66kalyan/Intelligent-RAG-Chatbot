"""
document_loader.py
Loads PDF documents and splits them into chunks.
"""

import glob
import os
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


def load_documents():

    pdf_files = glob.glob(
        os.path.join(config.DOCUMENTS_DIR, "*.pdf")
    )

    documents = []

    for pdf in pdf_files:

        loader = PyPDFLoader(pdf)

        documents.extend(loader.load())

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=config.CHUNK_SIZE,

        chunk_overlap=config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    return chunks


import time
from langchain_community.document_loaders import PyPDFLoader

def load_single_pdf(pdf_path):
    """
    Load one PDF and measure loading time.
    """

    start = time.perf_counter()

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    end = time.perf_counter()

    loading_time = end - start

    print("=" * 60)
    print("PDF LOADING PERFORMANCE")
    print("=" * 60)
    print(f"File        : {pdf_path}")
    print(f"Pages Loaded: {len(docs)}")
    print(f"Loading Time: {loading_time:.4f} sec")
    print("=" * 60)

    return docs

import time

def split_single_document(documents):
    """
    Split documents into chunks and measure performance.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )

    start = time.perf_counter()

    chunks = splitter.split_documents(documents)

    end = time.perf_counter()

    print("=" * 60)
    print("CHUNK CREATION PERFORMANCE")
    print("=" * 60)
    print(f"Input Pages   : {len(documents)}")
    print(f"Chunks Created: {len(chunks)}")
    print(f"Chunking Time : {end-start:.4f} sec")
    print("=" * 60)

    return chunks


if __name__ == "__main__":

    docs = load_documents()

    print("=" * 60)
    print("DOCUMENT LOADER")
    print("=" * 60)

    print("PDF Pages Loaded :", len(docs))

    chunks = split_documents(docs)

    print("Chunks Created   :", len(chunks))