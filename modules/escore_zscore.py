# modules/escore_zscore.py

import pandas as pd
from modules.tf_parser import get_tf_metadata

def load_escore_matrix(tf_name):
    """
    Return a DataFrame of E-scores for the given TF from its parsed network scores.
    """
    meta = get_tf_metadata(tf_name)
    if not meta or not meta.get("Targets"):
        print(f"[E-score] No metadata found for {tf_name}")
        return pd.DataFrame(columns=["Target", "E-score"])

    targets = meta["Targets"]
    scores = meta["Network_Scores"]

    try:
        escores = pd.DataFrame({
            "Target": targets,
            "E-score": [float(s) + 0.05 for s in map(float, scores)]
        })
        print(f"[E-score] Mocked E-scores for {tf_name}: {escores.shape[0]} targets")
        return escores
    except Exception as e:
        print(f"[E-score] Error parsing E-scores: {e}")
        return pd.DataFrame()

def load_zscore_matrix(tf_name):
    """
    Return a DataFrame of Z-scores for the given TF from its parsed network scores.
    """
    meta = get_tf_metadata(tf_name)
    if not meta or not meta.get("Targets"):
        print(f"[Z-score] No metadata found for {tf_name}")
        return pd.DataFrame(columns=["Target", "Z-score"])

    targets = meta["Targets"]
    scores = meta["Network_Scores"]

    try:
        zscores = pd.DataFrame({
            "Target": targets,
            "Z-score": [float(s) - 0.05 for s in map(float, scores)]
        })
        print(f"[Z-score] Mocked Z-scores for {tf_name}: {zscores.shape[0]} targets")
        return zscores
    except Exception as e:
        print(f"[Z-score] Error parsing Z-scores: {e}")
        return pd.DataFrame()
