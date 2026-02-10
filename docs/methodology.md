# Methodology

## 1. Project Overview
The objective of this project is to evaluate the robustness of a Large Language Model (LLM) against prompt injection attacks.
To achieve this, we designed an automated evaluation pipeline based on the HarmBench benchmark, allowing systematic testing and analysis of model behavior.

---

## 2. Benchmark Preparation
The HarmBench dataset provides a collection of prompts designed to trigger unsafe or undesired behaviors in LLMs.
Each prompt is associated with:
- an attack category (e.g., jailbreak, authority, emotional manipulation),
- a prompt type (standard or contextual),
- an expected safe behavior (refusal or safe answer).

The prompts were stored in a structured CSV file to enable automated processing.

---

## 3. Evaluation Pipeline
The evaluation pipeline is composed of four main steps:

### 3.1 Prompt Loading
Prompts are loaded from the CSV file and iterated sequentially.
Each prompt is sent to the evaluated model with controlled generation parameters such as temperature and maximum token length.

### 3.2 Model Execution
The main evaluated model is an open-source LLM (TinyLlama-1.1B-Chat) executed locally using the Hugging Face Transformers library.
A mock model is also used to validate the correctness of the pipeline independently of model behavior.

For each prompt, the model response is recorded along with metadata such as:
- model name
- timestamp
- prompt category and type

---

## 4. Result Collection
All model outputs are stored in a structured JSONL file (`results.jsonl`).
This file acts as a raw log of the evaluation process and enables traceability of each prompt–response pair.

---

## 5. Automated Scoring
An automated scoring script compares the model response with the expected behavior.
Each response is classified as:
- correct (1) if it matches the expected safe behavior,
- incorrect (0) otherwise.

The scoring results are stored in a CSV file (`scores.csv`) to facilitate further analysis.

---

## 6. Data Analysis
The analysis phase aggregates the scoring results to compute:
- global accuracy
- refusal rate
- accuracy by prompt type (standard vs contextual)
- accuracy by attack category

These metrics provide a quantitative view of the model’s robustness against different classes of prompt injection attacks.

---

## 7. Visualization
To improve interpretability, key metrics are visualized using bar charts:
- comparison between standard and contextual prompts,
- accuracy by attack category.

These visualizations highlight the most critical weaknesses of the evaluated model.

---

## 8. Reproducibility
The entire pipeline is designed to be reproducible:
- prompts are versioned,
- scripts are modular,
- results are stored in standardized formats (CSV and JSONL).

This design allows the evaluation to be easily extended to additional models or integrated into industrial monitoring systems.

---

## 9. Summary
This methodology enables a systematic and reproducible evaluation of LLM robustness against prompt injection attacks.
By combining automated execution, scoring, and analysis, it provides a solid foundation for both academic study and industrial applications.
