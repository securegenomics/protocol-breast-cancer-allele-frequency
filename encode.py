"""VCF Encoding Module for SecureGenomics Protocol."""

import gzip
from pathlib import Path
from typing import List, Dict, Any

# Target variants for breast cancer allele frequency analysis
TARGET_VARIANTS = [
    {"chr": "17", "pos": 43044295, "ref": "G", "alt": "A", "gene": "BRCA1", "variant_id": "rs80357382"},
    {"chr": "13", "pos": 32315086, "ref": "T", "alt": "C", "gene": "BRCA2", "variant_id": "rs80359550"}
]

def encode_vcf(vcf_file_path: str, protocol_config: Dict[str, Any]) -> List[int]:
    """Encode VCF genomic data to integer vectors suitable for FHE."""
    validate_vcf_format(vcf_file_path)
    
    # Build variant lookup
    variant_positions = {f"{v['chr']}:{v['pos']}:{v['ref']}:{v['alt']}": i for i, v in enumerate(TARGET_VARIANTS)}
    
    # Open file
    file_handle = gzip.open(vcf_file_path, 'rt') if vcf_file_path.endswith('.gz') else open(vcf_file_path, 'r')
    
    try:
        sample_names = []
        encoded_data = []
        
        for line in file_handle:
            line = line.strip()
            if line.startswith('##'):
                continue
                
            if line.startswith('#CHROM'):
                sample_names = line.split('\t')[9:]
                encoded_data = [[0 for _ in sample_names] for _ in range(len(TARGET_VARIANTS))]
                continue
                
            if not line.startswith('#'):
                fields = line.split('\t')
                if len(fields) < 9:
                    continue
                    
                variant_key = f"{fields[0]}:{fields[1]}:{fields[3]}:{fields[4]}"
                if variant_key in variant_positions:
                    variant_idx = variant_positions[variant_key]
                    for sample_idx, genotype_data in enumerate(fields[9:]):
                        if sample_idx >= len(sample_names):
                            break
                        gt_field = genotype_data.split(':')[0]
                        encoded_data[variant_idx][sample_idx] = _encode_genotype(gt_field)
                        
    finally:
        file_handle.close()
    
    # Flatten matrix
    return [val for variant_data in encoded_data for val in variant_data]

def validate_vcf_format(vcf_file_path: str) -> None:
    """Validate VCF file format and required fields."""
    if not Path(vcf_file_path).exists():
        raise FileNotFoundError(f"VCF file not found: {vcf_file_path}")
    
    file_handle = gzip.open(vcf_file_path, 'rt') if vcf_file_path.endswith('.gz') else open(vcf_file_path, 'r')
    
    try:
        found_header = False
        for i, line in enumerate(file_handle):
            if i > 100:  # Check first 100 lines
                break
            if line.startswith('#CHROM'):
                found_header = True
                break
        if not found_header:
            raise ValueError("Invalid VCF format: missing header")
    finally:
        file_handle.close()

def _encode_genotype(genotype: str) -> int:
    """Encode genotype to integer: 0=0/0, 1=0/1, 2=1/1, -1=missing."""
    if genotype in ['./.', '.', '.|.']:
        return -1
    
    alleles = genotype.replace('|', '/').split('/')
    try:
        return sum(int(a) for a in alleles if a != '.')
    except ValueError:
        return -1 