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
   
for strand, sequence in strands:
        for i in range(len(sequence) - target_length - 2 + 1):
            target = sequence[i:i + target_length]
            pam = sequence[i + target_length:i + target_length + 3]

            if len(pam) == 3 and pam[1:] == "GG":
                results.append({
                    "position": i,
                    "strand": strand,
                    "target": target,
                    "pam": pam
                })
                return results
