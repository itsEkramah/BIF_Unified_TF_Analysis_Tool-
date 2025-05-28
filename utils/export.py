import pandas as pd

def export_combined_data(trrust, cisbp, animal, out_file="TF_combined_results.csv"):
    with pd.ExcelWriter(out_file) as writer:
        trrust.to_excel(writer, sheet_name="TRRUST", index=False)
        cisbp.to_excel(writer, sheet_name="CISBP", index=False)
        animal.to_excel(writer, sheet_name="AnimalTFDB", index=False)
