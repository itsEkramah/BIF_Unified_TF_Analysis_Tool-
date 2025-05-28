# modules/tf_parser_utils.py

import pandas as pd

def pwm_string_to_df(pwm_sequence):
    """
    Convert a PWM sequence (e.g., 'ACGTGCA') into a one-hot encoded DataFrame suitable for logomaker.
    """
    pwm_sequence = pwm_sequence.strip().upper()
    bases = ["A", "C", "G", "T"]
    pwm_matrix = []

    for char in pwm_sequence:
        row = {base: 0 for base in bases}
        if char in bases:
            row[char] = 1
        pwm_matrix.append(row)

    return pd.DataFrame(pwm_matrix)



def parse_tf_targets(tf, targets_input):
    """
    Converts a TF and its associated target list (or comma-separated string) into edge list.
    """
    edges = []
    if isinstance(targets_input, str):
        targets = [t.strip() for t in targets_input.split(",") if t.strip()]
    elif isinstance(targets_input, list):
        targets = [t.strip() for t in targets_input if isinstance(t, str) and t.strip()]
    else:
        targets = []

    for target in targets:
        edges.append((tf, target))
    return edges
