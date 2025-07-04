"""
FHE Encryption Module for SecureGenomics Protocol.

This module handles the encryption of encoded genomic data using
the FHE public context for secure computation.
"""

import tenseal as ts
from typing import List

def encrypt_data(encoded_data: List[int], public_crypto_context: ts.Context) -> bytes:
    """
    Encrypt encoded genomic data using FHE public context.
    """
    return ts.bfv_vector(public_crypto_context, list(encoded_data)).serialize()
