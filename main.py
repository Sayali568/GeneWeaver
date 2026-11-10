import numpy as np

# Optional GPU support
try:
    import cupy as cp
    GPU_AVAILABLE = cp.cuda.is_available()
except Exception:
    cp = None
    GPU_AVAILABLE = False


def validate_dna(sequence):
    sequence = sequence.upper().replace("U", "T")

    if not sequence or any(base not in "ATCG" for base in sequence):
        raise ValueError("DNA sequence must contain only A, T, C, G.")

    return sequence
