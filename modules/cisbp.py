import os
import pandas as pd

def load_cisbp_data():
    path = os.path.join("data", "TF_Information_all_motifs.txt")
    print(f"[CIS-BP] Loading: {path}")
    try:
        df = pd.read_csv(path, sep="\t", header=0)
        return df
    except Exception as e:
        print("[CIS-BP] Error:", e)
        return pd.DataFrame()

def get_tf_motifs(tf_name, df):
    tf_matches = df[df["TF_Name"].str.upper() == tf_name.upper()]
    tf_matches = tf_matches[tf_matches["Motif_ID"].notna() & (df["Motif_ID"] != ".")]
    return tf_matches
