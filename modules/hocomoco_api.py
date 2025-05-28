# modules/hocomoco_api.py

import os
import pandas as pd

def read_pwm_matrix(motif_id, pwm_folder="pwms"):
    """
    Reads a PWM matrix from a text file and returns it as a pandas DataFrame.
    """
    if pd.isna(motif_id) or not isinstance(motif_id, str) or not motif_id.strip():
        print(f"[PWM] Invalid motif ID: {motif_id}")
        return None

    filename = f"{motif_id}.txt"
    filepath = os.path.join(pwm_folder, filename)

    if not os.path.exists(filepath):
        print(f"[PWM] File not found: {filepath}")
        return None

    try:
        pwm = pd.read_csv(filepath, sep="\t", comment="#", index_col=False)
        print(f"[PWM] Loaded {motif_id} from {filepath} with shape {pwm.shape}")
        return pwm
    except Exception as e:
        print(f"[PWM] Failed to load {motif_id}: {e}")
        return None
