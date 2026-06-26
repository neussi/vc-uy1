# Handover & Experimental Phase Guide: VC-UY1 Predictive Models

This document serves as a complete handover and technical guide for the incoming AI agent to take over the experimental phase of the **VC-UY1** availability prediction system at the University of Yaoundé I.

---

## 1. Project Context & Objectives

The goal is to deploy a two-stage hybrid availability predictor on volunteer computing nodes:
1.  **RLS-ARX (Linear Baseline):** Runs minute-by-minute recursively on the node. Ultra-frugal ($< 1$ KB RAM), reacts immediately to electrical outages (battery, sector plug status).
2.  **GRU-EWC (Deep Model):** Runs periodically (e.g. every 24h). Learns user habits. Quantized to **INT8** ($< 2$ MB RAM) to fit within a strict **10 MB TinyML memory budget**. Fine-tuned locally using **Elastic Weight Consolidation (EWC)** to prevent forgetting global patterns learned during pre-training.

---

## 2. Codebase Structure & File Locations

All paths are relative to the workspace root: `/home/npe-tech/Documents/M2 Recherche/vc-uy1`.

### 🐍 Virtual Environment
*   **Path:** [venv-server](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/venv-server/)
*   **Usage:** You MUST use the Python executable inside this environment: `./venv-server/bin/python`. Do NOT use the default system `python3` (it lacks required packages like `numpy`).

### 📊 Datasets (Pre-processed and Ready)
*   **Global BOINC FTA Sample:** [boinc_fta_traces.json](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/data_boinc/boinc_fta_traces.json) (38 MB, 143,990 observations)
*   **Local UY1 Traces:** [local_uy1_traces.json](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/data_local/local_uy1_traces.json) (18.5 MB, 71,995 observations)

### ⚙️ Training & Evaluation Scripts
*   **Linear ARX-Ridge Model:** [train_linear_ridge.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/linear_model/train_linear_ridge.py)
*   **GRU-EWC Transfer Learning:** [train_transfer_gru.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/gru_model/train_transfer_gru.py)
*   **Wayback Downloader:** [download_real_seti.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/download_real_seti.py) (For reference, download of full 2.2 GB raw archive).

### 📝 Academic Beamer Presentations (16:9 Aspect Ratio)
*   **Architecture & Workflow:** [presentation_architecture_workflow.tex](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/presentation_architecture_workflow.tex) (Detailed GRU layers, TikZ diagrams, math).
*   **RLS-ARX Model Proof:** [presentation_modele_lineaire.tex](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/presentation_modele_lineaire.tex) (72h memory proof, RLS covariance, OLS comparison).
*   **SETI@home Context:** [presentation_seti09.tex](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/presentation_seti09.tex) (Global telemetry statistics).

---

## 3. What Has Been Completed & Verified

1.  **Mathematical Proof of RLS Equivalence:** Proven that a forgetting factor $\lambda = 0.99977$ at a 1-minute sampling interval is mathematically equivalent to a physical 72-hour sliding window ($N = 4320$), saving $99.9\%$ of RAM by eliminating historical point storage.
2.  **Linear Model Training:** Verified that `train_linear_ridge.py` runs successfully, outputting weights to `arx_weights.json` with **97.93% accuracy on BOINC** and **99.54% accuracy on UY1**.
3.  **GRU-EWC Continual Learning:** Verified that `train_transfer_gru.py` simulates pre-training and fine-tuning. Results in `transfer_learning_results.json` show that standard fine-tuning causes a drop to **60.29% accuracy** on BOINC (catastrophic forgetting), whereas EWC keeps it stable at **85.96%**.
4.  **Academic Slides:** Fully customized and polished LaTeX Beamer files ready to be compiled on Overleaf. TikZ packages are loaded, and native diagrams are drawn directly in LaTeX.

---

## 4. Crucial Pitfalls & Lessons Learned (Avoid These!)

> [!WARNING]
> **Dead Academic Links:** The official Western Sydney University server (`http://fta.scem.uws.edu.au`) is permanently down. Do NOT attempt to download datasets from it.

> [!IMPORTANT]
> **Wayback Machine File Size:** The raw tgz archives (`seti09_tab.tgz`) are 2.2 GB. Do NOT try to download them on slow local connections because the requests will time out. The 38 MB `boinc_fta_traces.json` and 18.5 MB `local_uy1_traces.json` files are already present and sufficient for all experimental runs.

> [!CAUTION]
> **LaTeX Overflows:** When updating Beamer slides, avoid inserting long mathematical derivations or source code snippets in text blocks. Keep lists short and use `\small` or `\footnotesize` inside blocks to prevent text superposition.

---

## 5. Next Steps / Remaining Tasks for the Incoming Agent

The incoming agent should prioritize the following tasks:

### 1. Actual INT8 Quantization Implementation
Currently, the quantization in `train_transfer_gru.py` is simulated. You need to write a script to perform actual **Post-Training Quantization (PTQ)** or **Quantization-Aware Training (QAT)** using PyTorch or TensorFlow Lite:
*   Convert the Float32 PyTorch weights of the trained GRU cell to INT8.
*   Export the network to a `.tflite` or `.onnx` binary file.
*   Verify that the size of the final binary is **$< 2$ MB** and RAM usage during execution is **$< 10$ MB**.

### 2. Kolmogorov-Smirnov Statistical Test
Write a script to compute the **Kolmogorov-Smirnov (KS) statistic** between the BOINC trace distributions and the local Yaoundé trace distributions. This will mathematically prove the "distribution shift" (environmental drift) and justify the necessity of transfer learning.

### 3. Agent Integration
Integrate the prediction inference loop into the active volunteer computing scheduler in [agent/main.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/main.py) and [predictor.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/predictor.py):
*   Load the quantized GRU model and the RLS-ARX weights.
*   Query the predictor before submitting computing tasks.
*   Execute backup checkpoints and trigger migrations if predicted availability drops below $0.80$.
