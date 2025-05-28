import pandas as pd
import random

def simulate_trrust(tf):
    return pd.DataFrame([
        {"TF": tf, "Target": "ANGPT2", "Effect": "Activation"},
        {"TF": "MYOD1", "Target": "CDKN1A", "Effect": "Repression"},
        {"TF": "STAT1", "Target": "IL6", "Effect": "Activation"},
    ])

def simulate_cisbp(tf):
    return pd.DataFrame([
        {"Motif ID": "M006201", "Domain": "HLH", "T-Source ID": "305"},
        {"Motif ID": "M02895", "Domain": "bHLH-ZIP", "T-Source ID": "812"},
        {"Motif ID": "M00234", "Domain": "STAT", "T-Source ID": "812"},
    ])

def simulate_animaltfdb(tf):
    return pd.DataFrame([
        {"TF ID": "ATFB0011", "GO Terms": "RNA pol II reg.", "Localization": "Nucleus"},
        {"TF ID": "ATFB0045", "GO Terms": "DNA binding", "Localization": "Nucleus"},
    ])

def simulate_summary(tf):
    return f"{tf} is a transcriptional activator involved in oxygen homeostasis and cellular stress response."

def simulate_pwm(tf):
    from logomaker import Logo
    import pandas as pd
    import matplotlib.pyplot as plt
    pwm_df = pd.DataFrame([
        [0.2, 0.3, 0.4, 0.1],
        [0.1, 0.4, 0.3, 0.2],
        [0.3, 0.2, 0.2, 0.3],
        [0.4, 0.1, 0.1, 0.4],
        [0.2, 0.3, 0.3, 0.2],
        [0.25, 0.25, 0.25, 0.25],
        [0.1, 0.4, 0.4, 0.1]
    ], columns=list("ACGT"))
    plt.figure(figsize=(6, 2))
    Logo(pwm_df)
    plt.savefig("pwm_logo.png")
    return pwm_df

def simulate_network(tf):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()
    nodes = ["ANGPT2", "NDFIG1", "EGLN3", "PGK1"]
    G.add_edges_from([(tf, node) for node in nodes])
    pos = nx.spring_layout(G)
    plt.figure(figsize=(4, 2.5))
    nx.draw(G, pos, with_labels=True, node_color="#00aaff", node_size=1200, font_weight="bold")
    plt.savefig("tf_network.png")

def simulate_score_table(tf):
    return pd.DataFrame([
        {"TF": tf, "Score": "0.85", "Sequence": "ACGTGCA"},
        {"TF": "MYOD1", "Score": "0.75", "Sequence": "CTGCAGC"},
    ])

def simulate_zscore_table(tf):
    return pd.DataFrame([
        {"TF": tf, "Score": "2.31", "Sequence": "ACGTGCA"},
        {"TF": "AFGTA", "Score": "1.45", "Sequence": "CTGACCA"},
    ])
