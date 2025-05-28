# modules/tf_summary.py

import os
import pandas as pd

TF_DATA_FILE = os.path.join("data", "tf_detailed_info.tsv")

def get_tf_summary(tf_name):
    tf = tf_name.strip().upper()
    print(f"[Summary] Looking up TF: {tf}")

    try:
        df = pd.read_csv(TF_DATA_FILE, sep="\t")
        df["TF"] = df["TF"].str.strip().str.upper()
        row = df[df["TF"] == tf].iloc[0]

        if row is not None and not pd.isna(row["TF_Summary"]):
            return row["TF_Summary"]
        else:
            return "No summary available in file."
    except Exception as e:
        print(f"[Summary] Error: {e}")
        return "Summary loading error."
