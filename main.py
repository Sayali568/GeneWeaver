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

def reverse_complement(sequence):
    table = str.maketrans("ATCG", "TAGC")
    return sequence.translate(table)[::-1]


def find_targets(reference, guide):
    """
    Find 20-base target sequences followed by
    an NGG PAM on both DNA strands.
    """
    target_length = len(guide)
    results = []

    strands = [
        ("+", reference),
        ("-", reverse_complement(reference))
    ]

