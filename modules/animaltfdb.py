import os
import pandas as pd

def load_animaltfdb():
    path = os.path.join("data", "Homo_sapiens_TF.txt")
    print(f"[AnimalTFDB] Loading: {path}")
    try:
        df = pd.read_csv(path, sep="\t", header=0)
        df.columns = ["Species", "Symbol", "Ensembl", "Family", "Protein", "Entrez_ID"]
        return df
    except Exception as e:
        print("[AnimalTFDB] Error:", e)
        return pd.DataFrame()