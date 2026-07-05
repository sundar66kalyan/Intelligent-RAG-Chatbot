import uuid
import os


def generate_document_id(filename):
    """
    Generate a unique document ID.
    """

    name = os.path.splitext(filename)[0]

    unique = uuid.uuid4().hex[:8]

    return f"{name}_{unique}"