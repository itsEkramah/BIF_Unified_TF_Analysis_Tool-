# utils/visualization.py

import os
import matplotlib.pyplot as plt
import logomaker
import pandas as pd
import networkx as nx


def plot_pwm_logo(pwm_df, out_path="pwm_logo.png"):
    """
    Generates a PWM logo using logomaker and saves it to disk.
    """
    try:
        if pwm_df.empty:
            raise ValueError("PWM matrix is empty.")

        pwm_norm = pwm_df.div(pwm_df.sum(axis=1), axis=0).fillna(0)
        plt.figure(figsize=(6, 2))
        logomaker.Logo(pwm_norm)
        plt.title("PWM Motif Logo")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        print(f"[PWM] Logo saved: {out_path}")
    except Exception as e:
        print(f"[PWM] Logo error: {e}")


def plot_tf_network(edges_df, out_path="tf_network.png"):
    """
    Plots a TF-target interaction graph using NetworkX and saves it as an image.
    Expects a DataFrame with columns: 'TF', 'Target'.
    """
    try:
        if edges_df.empty:
            raise ValueError("No edges to plot.")

        if not {'TF', 'Target'}.issubset(edges_df.columns):
            raise ValueError("Required columns 'TF' and 'Target' not found in dataframe.")

        G = nx.DiGraph()
        for _, row in edges_df.iterrows():
            G.add_edge(row["TF"], row["Target"])

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(7, 5))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
                node_size=1800, font_size=10, font_weight='bold', arrowsize=20)
        plt.title("TF-Target Network")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        print(f"[Network] Diagram saved: {out_path}")
    except Exception as e:
        print(f"[Network] Diagram error: {e}")


def build_tf_target_network(df):
    """
    Constructs a NetworkX graph from a DataFrame containing:
    source_gene, target_gene, effect, pubmed_id
    """
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(
            row["source_gene"],
            row["target_gene"],
            effect=row.get("effect", ""),
            pubmed_id=row.get("pubmed_id", "")
        )
    return G


def get_network_statistics(G):
    """
    Returns key statistics for a given NetworkX graph.
    """
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G)
    }
