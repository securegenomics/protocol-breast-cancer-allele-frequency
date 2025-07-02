# Breast Cancer Allele Frequency Protocol

Template protocol for secure multi-party computation of breast cancer susceptibility variant frequencies.

## Variants Analyzed
- **BRCA1**: rs80357382 (17:43044295 G>A)
- **BRCA2**: rs80359550 (13:32315086 T>C)

## Usage
- **Aggregated**: Secure computation across encrypted datasets
- **Local**: Direct analysis on local VCF files

## Files
- `protocol.yaml`: Configuration and parameters
- `crypto_context.py`: FHE key generation
- `encode.py`: VCF data encoding
- `encrypt.py`: Data encryption
- `circuit.py`: FHE computation circuit
- `decrypt.py`: Result decryption
- `local_analysis.py`: Local-only analysis 