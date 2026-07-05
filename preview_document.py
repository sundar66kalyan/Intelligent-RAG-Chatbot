"""
preview_document.py
"""

import os

import config

from document_loader import load_single_pdf


def preview_document(file_name):
    """
    Load the first page of a PDF.
    """

    pdf_path = os.path.join(
        config.DOCUMENTS_DIR,
        file_name
    )

    if not os.path.exists(pdf_path):
        return None

    docs = load_single_pdf(pdf_path)

    if len(docs) == 0:
        return None

    return docs[0].page_content