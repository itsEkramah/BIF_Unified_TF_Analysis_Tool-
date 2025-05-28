import requests
import pandas as pd
from io import StringIO

def query_chip_atlas(tf_name):
    url = f"https://chip-atlas.org/target_genes?antigen={tf_name}&format=tsv"
    response = requests.get(url)
    if response.ok:
        df = pd.read_csv(StringIO(response.text), sep='\t')
        return df
    else:
        return pd.DataFrame()
