# modules/trrust.py

import pandas as pd
from modules.tf_parser import get_tf_metadata

def load_trrust_data():
    """
    Load mock TRRUST-like TF-target interaction data from tf_detailed_info.tsv.
    Returns the full DataFrame containing columns: TF, Target, Effect, PubMed_ID
    """
    records = []
    try:
        df = pd.read_csv("data/tf_detailed_info.tsv", sep="\t")
        for _, row in df.iterrows():
            tf = row['TF'].strip()
            targets = [t.strip() for t in row['Target'].split(',')]
            effects = [e.strip() for e in row['Effect'].split(',')]
            for t, eff in zip(targets, effects):
                records.append({
                    "TF": tf,
                    "Target": t,
                    "Effect": eff,
                    "PubMed_ID": "N/A"  # Mock placeholder
                })
        df_final = pd.DataFrame(records)
        print(f"[TRRUST] Generated mock TF-target records: {df_final.shape[0]}")
        return df_final
    except Exception as e:
        print(f"[TRRUST] Error loading TF-target mock data: {e}")
        return pd.DataFrame(columns=["TF", "Target", "Effect", "PubMed_ID"])
