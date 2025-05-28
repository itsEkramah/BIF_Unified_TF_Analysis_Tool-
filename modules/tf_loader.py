# modules/tf_loader.py

import os
import pandas as pd

TF_DATA_FILE = os.path.join("data", "tf_detailed_info.tsv")

def load_tf_data():
    """
    Load the main TF dataset from TSV into a pandas DataFrame.
    """
    if not os.path.exists(TF_DATA_FILE):
        print(f"[TF Loader] File not found: {TF_DATA_FILE}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(TF_DATA_FILE, sep="\t")
        if 'TF' not in df.columns:
            print("[TF Loader] Column 'TF' not found in dataset.")
            return pd.DataFrame()
        df["TF"] = df["TF"].astype(str).str.strip().str.upper()
        return df
    except Exception as e:
        print(f"[TF Loader] Error reading file: {e}")
        return pd.DataFrame()


def get_tf_row(tf_name, df=None):
    """
    Retrieve a single TF row by name from the full dataset.
    """
    if df is None:
        df = load_tf_data()

    tf_name = tf_name.strip().upper()
    if 'TF' not in df.columns:
        print("[TF Loader] No 'TF' column to filter by.")
        return None

    matches = df[df["TF"] == tf_name]
    if not matches.empty:
        return matches.iloc[0]
    
    print(f"[TF Loader] No match found for TF: {tf_name}")
    return None
