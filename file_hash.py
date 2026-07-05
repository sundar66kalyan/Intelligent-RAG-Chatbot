"""
file_hash.py
"""

import hashlib


def calculate_sha256(file_path):
    """
    Calculate SHA-256 hash of a file.
    """

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()