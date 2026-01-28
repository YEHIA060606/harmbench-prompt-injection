# HarmBench – Prompt Injection Audit on LLMs

## Objective
This project evaluates the robustness of a Large Language Model (LLM) against prompt injection attacks using the HarmBench benchmark.

## Evaluated Model
- TinyLlama-1.1B-Chat (open-source, local)
- Mock model used for validation

## Benchmark
HarmBench prompts grouped into:
- Jailbreak
- Authority
- Emotional manipulation
- Policy bypass
- Roleplay
- Misinformation
- Fake system prompts

## Project Structure
src/        : Python evaluation pipeline  
data/       : prompts and results  
docs/       : methodology and analysis  
report/     : final report  
slides/     : presentation  

## Execution
```bash
python src/02_run_models.py
python src/03_score_results.py
python src/04_analyze.py

Results : 

Global accuracy: 38.3%

Standard prompts: 50.0%

Contextual prompts: 24.1%

Major weaknesses observed in:

Jailbreak

Authority

Emotional manipulation

Perspective : 

This work can be extended toward industrial monitoring using ELK (Elasticsearch, Logstash, Kibana).

Team :

Yahya – Pipeline & execution

Hocine – State of the art

Ines – Docker & analysis

Malik – ELK & presentation