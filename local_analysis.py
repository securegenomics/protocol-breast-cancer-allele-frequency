"""Local-only Analysis for SecureGenomics Protocol."""

from typing import Dict, Any
from encode import encode_vcf, TARGET_VARIANTS

def analyze_local(vcf_file_path: str, protocol_config: Dict[str, Any]) -> Dict[str, Any]:
    """Perform local-only analysis without encryption."""
    # Encode VCF data
    encoded_data = encode_vcf(vcf_file_path, protocol_config)
    
    # Calculate allele frequencies locally
    variant_count = len(TARGET_VARIANTS)
    sample_count = len(encoded_data) // variant_count if variant_count > 0 else 0
    
    frequencies = []
    for i in range(variant_count):
        variant_data = encoded_data[i * sample_count:(i + 1) * sample_count]
        valid_genotypes = [g for g in variant_data if g >= 0]  # Exclude missing (-1)
        
        if valid_genotypes:
            allele_frequency = sum(valid_genotypes) / (len(valid_genotypes) * 2)  # diploid
        else:
            allele_frequency = 0.0
        frequencies.append(allele_frequency)
    
    # Format results
    results = {
        'analysis_type': 'Local Breast Cancer Allele Frequency',
        'sample_count': sample_count,
        'variants': []
    }
    
    for i, variant in enumerate(TARGET_VARIANTS):
        if i < len(frequencies):
            results['variants'].append({
                'gene': variant['gene'],
                'variant_id': variant['variant_id'],
                'position': f"{variant['chr']}:{variant['pos']}",
                'allele_frequency': frequencies[i],
                'sample_allele_count': int(frequencies[i] * sample_count * 2)
            })
    
    return results 