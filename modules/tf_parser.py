import os
import pandas as pd
from modules.tf_parser_utils import pwm_string_to_df, parse_tf_targets

# Path to the detailed TF information TSV
TSV_FILE = os.path.join("data", "tf_detailed_info.tsv")


def get_tf_results(tf_name: str) -> dict:
    """
    Fetch and structure all TF-related data into pandas DataFrames.
    """
    tf = tf_name.strip().upper()

    # Verify TSV exists
    if not os.path.exists(TSV_FILE):
        raise FileNotFoundError(f"[Parser] TSV data not found at: {TSV_FILE}")

    # Load and normalize
    df = pd.read_csv(TSV_FILE, sep="\t")
    df["TF"] = df["TF"].str.strip().str.upper()

    # Locate the requested TF
    row_df = df[df["TF"] == tf]
    if row_df.empty:
        print(f"[Parser] TF '{tf}' not found in TSV.")
        return {}
    row = row_df.iloc[0]

    result: dict = {}

    # --- TRRUST
    trrust_rows = []
    targets = [t.strip() for t in row["Target"].split(",") if t.strip()]
    effects = [e.strip() for e in row["Effect"].split(",") if e.strip()]
    for tgt, eff in zip(targets, effects):
        trrust_rows.append({"TF": tf, "Target": tgt, "Effect": eff})
    result["trrust_df"] = pd.DataFrame(trrust_rows)

    # --- CIS-BP (ensure equal-length lists)
    motif_ids = [m.strip() for m in row["CIS_BP_Motif_ID"].split(",") if m.strip()]
    domains = [d.strip() for d in row["Domain"].split(",") if d.strip()]
    if len(motif_ids) != len(domains):
        min_len = min(len(motif_ids), len(domains))
        print(f"[Warning] CIS-BP motif/domains length mismatch ({len(motif_ids)} vs {len(domains)}). Truncating to {min_len}.")
        motif_ids = motif_ids[:min_len]
        domains = domains[:min_len]
    result["cisbp_df"] = pd.DataFrame({
        "Motif ID": motif_ids,
        "Domain": domains,
        "T-Source ID": [812] * len(motif_ids)  # placeholder source ID
    })

    # --- AnimalTFDB
    result["animaltfdb_df"] = pd.DataFrame({
        "TF ID": [tf],
        "GO Terms": [row.get("Associated_Cancers", "")],
        "Localization": [row.get("Additional_Notes", "")]
    })

    # --- PWM Matrix
    pwm_seq = row.get("PWM_Sequence", "").strip()
    result["pwm_df"] = pwm_string_to_df(pwm_seq) if pwm_seq else pd.DataFrame()

    # --- Network Edges
    targets_network = [t.strip() for t in row.get("Network_TFs", "").split(",") if t.strip()]
    scores_raw = [s.strip() for s in row.get("Network_Scores", "").split(",") if s.strip()]
    # Convert scores to float
    scores_network = []
    for s in scores_raw:
        try:
            scores_network.append(float(s))
        except ValueError:
            print(f"[Warning] Invalid network score '{s}' for TF '{tf}', defaulting to 0.")
            scores_network.append(0.0)
    result["network_edges"] = parse_tf_targets(tf, list(zip(targets_network, scores_network)))

    # --- Summary
    result["summary"] = row.get("TF_Summary", "No summary available.")

    # --- E-score DataFrame
    escore_rows = []
    for score in scores_network:
        escore_rows.append({"TF": tf, "Score": score, "Sequence": pwm_seq})
    result["escore_df"] = pd.DataFrame(escore_rows)

    # --- Z-score DataFrame (scaled for differentiation)
    zscore_rows = []
    for score in scores_network:
        zscore_rows.append({"TF": tf, "Score": score * 2.7, "Sequence": pwm_seq})
    result["zscore_df"] = pd.DataFrame(zscore_rows)

    return result
