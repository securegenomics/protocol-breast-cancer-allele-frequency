"""FHE Decryption and Result Interpretation for SecureGenomics Protocol."""

import pickle
import base64
from typing import Dict, Any

def decrypt_results(encrypted_results: bytes, private_context: str) -> Dict[str, Any]:
    """Decrypt FHE computation results using private key."""
    # Decode private context
    context_data = pickle.loads(base64.b64decode(private_context))
    
    # Deserialize encrypted results
    result_data = pickle.loads(encrypted_results)
    
    # Mock decryption - replace with actual FHE library
    decrypted_data = {
        'computation_type': result_data.get('computation_type'),
        'participant_count': result_data.get('participant_count'),
        'variant_frequencies': [0.25, 0.15]  # Mock frequencies for BRCA1, BRCA2
    }
    
    return decrypted_data

def interpret_results(decrypted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Interpret and format decrypted results for user presentation."""
    from encode import TARGET_VARIANTS
    
    frequencies = decrypted_data.get('variant_frequencies', [])
    participant_count = decrypted_data.get('participant_count', 0)
    
    results = {
        'analysis_type': 'Breast Cancer Allele Frequency',
        'participant_count': participant_count,
        'variants': []
    }
    
    for i, variant in enumerate(TARGET_VARIANTS):
        if i < len(frequencies):
            results['variants'].append({
                'gene': variant['gene'],
                'variant_id': variant['variant_id'],
                'position': f"{variant['chr']}:{variant['pos']}",
                'allele_frequency': frequencies[i],
                'allele_count': int(frequencies[i] * participant_count * 2)  # diploid
            })
    
    return results 