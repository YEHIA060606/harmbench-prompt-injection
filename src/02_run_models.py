import csv
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List

from transformers import pipeline


PROMPTS_PATH = os.path.join("data", "prompts.csv")
RESULTS_PATH = os.path.join("data", "results.jsonl")

# Local model (chat-like, lightweight)
HF_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Use text-generation pipeline (Transformers v5)
hf_pipe = pipeline("text-generation", model=HF_MODEL_ID)

MODELS = [
    "mock:model-v1",
    f"hf:{HF_MODEL_ID}",
]

TEMPERATURE = 0.2
MAX_TOKENS = 200


def load_prompts(path: str) -> List[Dict[str, str]]:
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append(row)
    return prompts


def mock_call_model(prompt: str) -> str:
    if "ignore" in prompt.lower() or "system:" in prompt.lower():
        return "I'm sorry, I can't comply with that request."
    return "This is a safe, general answer (MOCK)."


def call_hf(prompt: str) -> str:
    """
    TinyLlama is a chat/instruct-style model.
    We provide a simple instruction template + fallback to raw prompt.
    """
    chat_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"

    out = hf_pipe(
        chat_prompt,
        max_new_tokens=MAX_TOKENS,
        do_sample=True,
        temperature=TEMPERATURE,
        return_full_text=False,
    )
    text = out[0]["generated_text"] if out else ""

    # Fallback if empty
    if not text.strip():
        out2 = hf_pipe(
            prompt,
            max_new_tokens=MAX_TOKENS,
            do_sample=True,
            temperature=TEMPERATURE,
            return_full_text=False,
        )
        text = out2[0]["generated_text"] if out2 else ""

    return text


def call_model(model_name: str, prompt: str) -> Dict[str, Any]:
    if model_name.startswith("mock:"):
        return {"model": model_name, "text": mock_call_model(prompt)}

    if model_name.startswith("hf:"):
        try:
            text = call_hf(prompt)
            return {"model": model_name, "text": text}
        except Exception as e:
            return {"model": model_name, "text": "", "error": str(e)}

    return {"model": model_name, "text": "", "error": "Provider not configured"}


def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    prompts = load_prompts(PROMPTS_PATH)

    # Clean previous results
    if os.path.exists(RESULTS_PATH):
        os.remove(RESULTS_PATH)

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    for p in prompts:
        prompt_id = p["id"]
        for model in MODELS:
            out = call_model(model, p["prompt"])

            record = {
                "run_id": run_id,
                "timestamp_utc": datetime.utcnow().isoformat(),
                "prompt_id": prompt_id,
                "type": p["type"],
                "category": p["category"],
                "expected_behavior": p["expected_behavior"],
                "model": out.get("model"),
                "response_text": out.get("text"),
                "error": out.get("error"),
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
            }

            append_jsonl(RESULTS_PATH, record)
            status = "OK" if not record["error"] else "ERR"
            print(f"[{status}] prompt {prompt_id} -> {model}")

            time.sleep(0.05)


if __name__ == "__main__":
    main()
