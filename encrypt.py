"""
FHE Encryption Module for SecureGenomics Protocol.

This module handles the encryption of encoded genomic data using
the FHE public context for secure computation.
"""

import pickle
import base64
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def encrypt_data(encoded_data: List[int], public_context: str) -> bytes:
    """
    Encrypt encoded genomic data using FHE public context.
    
    Args:
        encoded_data: Integer vectors from encode_vcf()
        public_context: Public crypto context (base64 encoded)
        
    Returns:
        bytes: Encrypted data ready for server upload
    """
    try:
        # Decode the public context
        context_data = pickle.loads(base64.b64decode(public_context))
        
        logger.info(f"Encrypting {len(encoded_data)} data points")
        logger.info(f"Using {context_data['scheme']} encryption scheme")
        
        # Validate context
        if not _validate_public_context(context_data):
            raise ValueError("Invalid public context")
            
        # Mock encryption - replace with actual FHE library
        encrypted_result = {
            'scheme': context_data['scheme'],
            'encrypted_data': f"mock_encrypted_{len(encoded_data)}_values",
            'metadata': {
                'data_count': len(encoded_data),
                'context_id': 'mock_context',
                'poly_modulus_degree': context_data.get('poly_modulus_degree', 8192)
            }
        }
        
        # Serialize the encrypted result
        serialized_data = pickle.dumps(encrypted_result)
        
        logger.info(f"Successfully encrypted data, size: {len(serialized_data)} bytes")
        return serialized_data
        
    except Exception as e:
        logger.error(f"Data encryption failed: {e}")
        raise Exception(f"Failed to encrypt data: {e}")


def validate_encrypted_data(encrypted_data: bytes, expected_size: int = None) -> bool:
    """
    Validate that encrypted data is properly formed.
    
    Args:
        encrypted_data: Encrypted data bytes
        expected_size: Expected number of data points (optional)
        
    Returns:
        bool: True if data appears valid, False otherwise
    """
    try:
        # Deserialize and check structure
        data = pickle.loads(encrypted_data)
        
        required_fields = ['scheme', 'encrypted_data', 'metadata']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field in encrypted data: {field}")
                return False
                
        metadata = data['metadata']
        required_metadata = ['data_count', 'context_id']
        for field in required_metadata:
            if field not in metadata:
                logger.error(f"Missing required metadata field: {field}")
                return False
                
        # Check expected size if provided
        if expected_size is not None:
            actual_size = metadata['data_count']
            if actual_size != expected_size:
                logger.error(f"Data count mismatch: expected {expected_size}, got {actual_size}")
                return False
                
        return True
        
    except Exception as e:
        logger.error(f"Encrypted data validation failed: {e}")
        return False


def get_encryption_metadata(encrypted_data: bytes) -> Dict[str, Any]:
    """
    Extract metadata from encrypted data.
    
    Args:
        encrypted_data: Encrypted data bytes
        
    Returns:
        dict: Metadata about the encrypted data
    """
    try:
        data = pickle.loads(encrypted_data)
        return {
            'scheme': data.get('scheme'),
            'data_count': data.get('metadata', {}).get('data_count'),
            'context_id': data.get('metadata', {}).get('context_id'),
            'poly_modulus_degree': data.get('metadata', {}).get('poly_modulus_degree'),
            'encryption_timestamp': data.get('metadata', {}).get('encryption_timestamp'),
            'data_size_bytes': len(encrypted_data)
        }
    except Exception as e:
        logger.error(f"Failed to extract metadata: {e}")
        return {}


def batch_encrypt_data(encoded_data_list: List[List[int]], public_context: str) -> List[bytes]:
    """
    Encrypt multiple datasets in batch for efficiency.
    
    Args:
        encoded_data_list: List of encoded data arrays
        public_context: Public crypto context
        
    Returns:
        list: List of encrypted data bytes
    """
    try:
        encrypted_results = []
        
        for i, encoded_data in enumerate(encoded_data_list):
            logger.info(f"Encrypting dataset {i+1}/{len(encoded_data_list)}")
            encrypted_data = encrypt_data(encoded_data, public_context)
            encrypted_results.append(encrypted_data)
            
        logger.info(f"Successfully encrypted {len(encoded_data_list)} datasets")
        return encrypted_results
        
    except Exception as e:
        logger.error(f"Batch encryption failed: {e}")
        raise Exception(f"Failed to batch encrypt data: {e}")


def _validate_public_context(context_data: Dict[str, Any]) -> bool:
    """
    Validate the structure of a public context.
    
    Args:
        context_data: Deserialized public context data
        
    Returns:
        bool: True if context is valid, False otherwise
    """
    required_fields = ['scheme', 'poly_modulus_degree', 'public_key']
    
    for field in required_fields:
        if field not in context_data:
            logger.error(f"Missing required field in public context: {field}")
            return False
            
    # Validate scheme
    supported_schemes = ['BFV', 'CKKS']
    if context_data['scheme'] not in supported_schemes:
        logger.error(f"Unsupported encryption scheme: {context_data['scheme']}")
        return False
        
    # Validate polynomial modulus degree (must be power of 2)
    degree = context_data['poly_modulus_degree']
    if not (degree > 0 and (degree & (degree - 1)) == 0):
        logger.error(f"Invalid polynomial modulus degree: {degree}")
        return False
        
    return True


def estimate_encrypted_size(data_count: int, poly_modulus_degree: int = 8192) -> int:
    """
    Estimate the size of encrypted data in bytes.
    
    Args:
        data_count: Number of data points to encrypt
        poly_modulus_degree: Polynomial modulus degree
        
    Returns:
        int: Estimated size in bytes
    """
    # Rough estimation based on FHE ciphertext sizes
    # Actual size depends on scheme and parameters
    
    # Number of ciphertexts needed
    batch_size = poly_modulus_degree // 2  # Typical batch size for BFV
    num_ciphertexts = (data_count + batch_size - 1) // batch_size
    
    # Approximate ciphertext size (depends on coeff_modulus)
    approx_ciphertext_size = poly_modulus_degree * 8 * 4  # Rough estimate
    
    # Add metadata overhead
    metadata_overhead = 1024  # Approximate
    
    total_size = num_ciphertexts * approx_ciphertext_size + metadata_overhead
    
    return total_size 