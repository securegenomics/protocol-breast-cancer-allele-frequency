"""VCF Encoding Module for SecureGenomics Protocol."""

from typing import List, Dict, Any, TextIO
import pysam

# Target variants for breast cancer allele frequency analysis
TARGET_VARIANTS = [
    "rs1801282",
    ("10", 12345678, "A"),
    ("16", 764568, "T"),
    ("5", 1502341, "A"),
    ("8", 128413212, "G"),
    ("2", 217487839, "A"),
    ("3", 8761234, "G"),
    ("11", 6894561, "T"),
]

def make_record_map(vcf_path):
    record_map = {}
    vcf_reader = pysam.VariantFile(vcf_path)
    for record in vcf_reader.fetch():
        # Get genotype value (0=ref/ref, 1=ref/alt, 2=alt/alt)
        alt_count = sum(record.samples[0]['GT'])
        record_map[record.id] = alt_count
        record_map[(record.chrom, record.pos, record.alts[0])] = alt_count
    return record_map

# 2. Filter by variant list (by ID or (CHROM, POS))
def encode_on_variant_list(record_map: dict, filter_list: list):
    for pos_or_id in filter_list:
        if isinstance(pos_or_id, tuple):
            key = (pos_or_id[0], pos_or_id[1], pos_or_id[2])
        elif isinstance(pos_or_id, str):
            key = pos_or_id
        else:
            raise ValueError(f"Invalid input: {pos_or_id}")
        yield record_map[key] if key in record_map else 0


def encode_vcf(vcf_path: str) -> List[int]:
    """Encode VCF genomic data to integer vectors suitable for FHE."""
    record_map = make_record_map(vcf_path)
    encoded_data = list(encode_on_variant_list(record_map, TARGET_VARIANTS))
    return encoded_data
