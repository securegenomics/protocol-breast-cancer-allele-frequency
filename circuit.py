"""FHE Computation Circuit for SecureGenomics Protocol."""

from typing import Dict, Any, List
import tenseal as ts

def compute(encrypted_datasets: List[bytes]) -> bytes:
    # multiplication depth: 1
    vectors = []
    for data in encrypted_datasets:
        # Deserialize bytes directly into a vector
        vector = ts.bfv_vector_load(data)
        vectors.append(vector)
    
    if not vectors:
        raise ValueError("No encrypted datasets provided")
        
    num_alleles = len(vectors) * 2
    
    # sum vectors and divide by num_alleles
    encrypted_result = sum(vectors) / num_alleles
    
    return encrypted_result.serialize()
