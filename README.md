
# 🧬 Unified TF Analysis Tool

A PyQt5-based desktop application that allows integrated, real-time analysis of human transcription factors (TFs) using data from multiple bioinformatics resources: TRRUST, CIS-BP, HOCOMOCO, AnimalTFDB, and ChIP-Atlas. It generates TF summaries, motif logos, target networks, and E-/Z-scores — all in a scrollable, visually intuitive GUI.

---

## 📌 Introduction

Understanding transcription factors is central to gene regulation research. This tool streamlines the querying, visualization, and interpretation of TF-related information from leading databases. It is designed for molecular biologists, bioinformaticians, and students who need fast and unified access to TF insights.

---

## 🎯 Objectives

* Provide an all-in-one TF query system.
* Automatically retrieve target data, binding motifs, and regulatory networks.
* Use ChatGPT and Wikipedia to generate functional TF summaries.
* Visualize position weight matrices (PWMs) and TF-target networks.
* Export integrated data for downstream analysis.


## ⚙️ How It Works

The application combines structured TSV data with live API lookups and AI-generated text. Here’s how each component functions:

| Module                                                       | Description                                                                                          |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `tf_parser.py`                                               | Core engine to parse all TF-related rows and extract structured info from `tf_detailed_info.tsv`.    |
| `tf_summary.py` + `chatgpt_summary.py`                       | Returns summary from local TSV or dynamically via ChatGPT or Wikipedia.                              |
| `hocomoco_api.py`                                            | Loads PWM motif matrix and plots logo using Logomaker.                                               |
| `escore_zscore.py`                                           | Parses mock E-scores and Z-scores from encoded network weights.                                      |
| `network_builder.py`                                         | Builds TF-target network graphs using NetworkX and matplotlib.                                       |
| `trrust.py`, `cisbp.py`, `animaltfdb.py`, `chipatlas_api.py` | Load TF-related metadata from TRRUST, CIS-BP, AnimalTFDB, and ChIP-Atlas respectively.               |
| `main_window.py`                                             | PyQt5 GUI where users input a TF name and receive all outputs in a clean 2-column scrollable format. |

---

## 🧪 Features

✅ Unified TF search across five databases
✅ ChatGPT and Wikipedia summaries
✅ PWM motif logo generation (Logomaker)
✅ TF-Target interaction networks (NetworkX)
✅ E-score and Z-score computation
✅ Scrollable, card-style PyQt5 GUI
✅ Data export functionality

---
## 🖼Graphic User Interface Example Screenshots

### TP53 Analysis

![TP53 Panel 1](https://raw.githubusercontent.com/itsEkramah/BIF_Unified_TF_Analysis_Tool-/main/INTERFACE%20EXAMPLE%20SCREENSHOTS/SCREENSHOT1%20TP53.png)  
*Figure 1* 

![TP53 Panel 2](https://raw.githubusercontent.com/itsEkramah/BIF_Unified_TF_Analysis_Tool-/main/INTERFACE%20EXAMPLE%20SCREENSHOTS/SCREENSHOT2%20TP53.png)  
*Figure 2*

---

### RELA Analysis

![RELA Panel 1](https://raw.githubusercontent.com/itsEkramah/BIF_Unified_TF_Analysis_Tool-/main/INTERFACE%20EXAMPLE%20SCREENSHOTS/Screenshot1%20RELA.png)  
*Figure 1*

![RELA Panel 2](https://raw.githubusercontent.com/itsEkramah/BIF_Unified_TF_Analysis_Tool-/main/INTERFACE%20EXAMPLE%20SCREENSHOTS/Screenshot2%20RELA.png)  
*Figure 2*

---
## 🖥️ How to Use

### 🔧 1. Prerequisites

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🗂 2. Download Required Data Files

Create a `data/` folder in your project and add:

```
tf_detailed_info.tsv
TF_Information_all_motifs.txt
Homo_sapiens_TF.txt
Homo_sapiens_TF_cofactors.txt
Homo_sapiens_TF_protein.fasta
Escores.txt
Zscores.txt
TRRUST_human.tsv
tf_motif_info.json
```

Also create a `pwms/` folder with PWM files:

```
pwms/
├── M01142_3.00.txt
├── M01143_3.00.txt
...
```
### 🔑 3. Add OpenAI API Key

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key_here
```

### 🚀 4. Run the Application

```bash
python main.py
```

Once launched, enter a transcription factor name (e.g. `TP53`) and click **Analyze**.

---

## 🖼️ GUI Overview

The app displays results in 8 scrollable panels:

| Section            | Content                                               |
| ------------------ | ----------------------------------------------------- |
| TRRUST Results     | TF → Target + Effect relationships                    |
| CIS-BP Results     | Motif ID and domain info                              |
| AnimalTFDB Results | Cancer associations and subcellular localization      |
| PWM Motif Logo     | Graphical logo from HOCOMOCO motif                    |
| TF Summary         | Generated by ChatGPT or fallback to Wikipedia         |
| TF Network Diagram | TF → Target network diagram                           |
| E-score Table      | Mock scores derived from network edges (+0.05 offset) |
| Z-score Table      | Mock scores derived from network edges (×2.7 scaling) |

---

## 📂 Directory Structure

```
project/
│
├── data/
│   ├── tf_detailed_info.tsv              # Main TSV with all TF-related parsed data
│   ├── TF_Information_all_motifs.txt     # CIS-BP motif and domain information
│   ├── Homo_sapiens_TF.txt               # AnimalTFDB main TF metadata
│   ├── Homo_sapiens_TF_cofactors.txt     # List of TF cofactors (not used directly yet)
│   ├── Homo_sapiens_TF_protein.fasta     # FASTA sequences for human TF proteins
│   ├── Escores.txt                       # E-score values (mock or derived)
│   ├── Zscores.txt                       # Z-score values (mock or derived)
│   ├── TRRUST_human.tsv                  # TRRUST TF → Target → Effect relationships
│   └── tf_motif_info.json                # Motif metadata, ID mapping (future enhancement)
│
├── pwms/                                 # Folder with PWM motif files (e.g. M01142_3.00.txt)
│   ├── M01142_3.00.txt
│   ├── M01143_3.00.txt
│   └── ...
│
├── gui/
│   └── main_window.py                    # Main PyQt5 GUI layout and logic
│
├── modules/                              # Functional modules
│   ├── tf_parser.py
│   ├── tf_summary.py
│   ├── chatgpt_summary.py
│   ├── tf_loader.py
│   ├── tf_parser_utils.py
│   ├── trrust.py
│   ├── cisbp.py
│   ├── animaltfdb.py
│   ├── chipatlas_api.py
│   ├── escore_zscore.py
│   ├── hocomoco_api.py
│   ├── network_builder.py
│   └── export.py
│
├── utils/
│   └── visualization.py                  # PWM and network plot logic
│
├── main.py                               # Application launcher
├── .env                                  # Contains your OpenAI API key
├── requirements.txt                      # List of required Python libraries
└── README.md                             # Project documentation

---

## 🧪 Example TFs for Testing

Try these transcription factors for instant demo:

* `TP53`
* `HIF1A`
* `STAT3`
* `FOXO3`
* `MYC`

---

## 📤 Exporting Results

Use `export.py` to save TRRUST, CIS-BP, and AnimalTFDB outputs:

```python
from modules.export import export_combined_data
export_combined_data(trrust_df, cisbp_df, animal_df, out_file="TF_combined_results.xlsx")
```

---

## 🤖 AI Summary Generation

Uses OpenAI’s GPT-3.5 to summarize TF biology. If ChatGPT fails, it gracefully falls back to Wikipedia summaries.

---

## 💡 Future Enhancements

* Real-time ChIP-Atlas API integration
* Support for species-specific TF analysis
* Upload your own TF dataset
* Batch processing of TFs

---

## 👩‍🔬 License & Citation

For academic use only. If used in publications, please cite the GitHub project and underlying data sources like TRRUST, HOCOMOCO, CIS-BP, AnimalTFDB.

---



