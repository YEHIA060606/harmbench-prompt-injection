import csv
import json
import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from transformers import pipeline


# Paths

PROMPTS_PATH = os.path.join("data", "prompts_from_hf.csv")
RESULTS_PATH = os.path.join("data", "results.jsonl")

# Models
HF_MODELS = [
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "distilgpt2",
    "google/flan-t5-base",
]


# Params + Env overrides
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "200"))

# Run only first N prompts if set (FAST)
FAST_N = int(os.getenv("FAST_N", "0"))

# If you want to skip HF calls (only mock) -> set SKIP_HF=1
SKIP_HF = os.getenv("SKIP_HF", "0").strip() in ("1", "true", "True", "yes", "YES")

SLEEP_BETWEEN_CALLS = float(os.getenv("SLEEP", "0.05"))

# Cache pipelines so we don't reload model every prompt
_PIPE_CACHE: Dict[str, Any] = {}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_prompts(path: str) -> List[Dict[str, str]]:
    """
    Loads prompts from CSV with flexible columns.

    Expected columns (preferred):
      - id OR prompt_id
      - type
      - category
      - expected_behavior
      - prompt OR prompt_text
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Prompts file not found: {path}\n"
            f"Make sure you generated/downloaded it into data/ (ex: prompts_from_hf.csv)"
        )

    prompts: List[Dict[str, str]] = []

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header row: {path}")

        for row in reader:
            prompt_id = (
                row.get("id")
                or row.get("prompt_id")
                or row.get("promptId")
                or row.get("promptID")
            )
            prompt_text = (
                row.get("prompt")
                or row.get("prompt_text")
                or row.get("text")
                or row.get("question")
            )

            if not prompt_id or not prompt_text:
                continue

            prompts.append(
                {
                    "id": str(prompt_id),
                    "type": (row.get("type") or "standard").strip(),
                    "category": (row.get("category") or "unknown").strip(),
                    "expected_behavior": (row.get("expected_behavior") or row.get("expected") or "refuse").strip(),
                    "prompt": str(prompt_text),
                }
            )

    if not prompts:
        raise ValueError(f"No valid prompts loaded from: {path}")

    return prompts


def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# =========================
# Mock model
# =========================
def mock_call_model(prompt: str) -> str:
    # Simple "safe-ish" behavior for demo
    if "ignore" in prompt.lower() or "system:" in prompt.lower():
        return "I'm sorry, I can't comply with that request."
    return "This is a safe, general answer (MOCK)."


# =========================
# Hugging Face models
# =========================
def _get_hf_pipeline(model_id: str):
    """
    Create or return cached pipeline for the model.
    Uses:
      - text2text-generation for T5/FLAN
      - text-generation for GPT-like
    """
    if model_id in _PIPE_CACHE:
        return _PIPE_CACHE[model_id]

    # Heuristic: FLAN/T5 are encoder-decoder
    if "t5" in model_id.lower() or "flan" in model_id.lower():
        task = "text2text-generation"
    else:
        task = "text-generation"

    pipe = pipeline(task, model=model_id)
    _PIPE_CACHE[model_id] = (task, pipe)
    return _PIPE_CACHE[model_id]


def call_hf(model_id: str, prompt: str) -> str:
    task, hf_pipe = _get_hf_pipeline(model_id)

    # Make an instruction-like wrapper for chat models (works ok for TinyLlama too)
    chat_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"

    if task == "text2text-generation":
        out = hf_pipe(
            prompt,
            max_new_tokens=MAX_TOKENS,
        )
        # output format: [{"generated_text": "..."}]
        return out[0].get("generated_text", "") if out else ""

    # text-generation
    out = hf_pipe(
        chat_prompt,
        max_new_tokens=MAX_TOKENS,
        do_sample=True,
        temperature=TEMPERATURE,
        return_full_text=False,
    )
    text = out[0].get("generated_text", "") if out else ""

    # fallback if empty
    if not text.strip():
        out2 = hf_pipe(
            prompt,
            max_new_tokens=MAX_TOKENS,
            do_sample=True,
            temperature=TEMPERATURE,
            return_full_text=False,
        )
        text = out2[0].get("generated_text", "") if out2 else ""

    return text


def call_model(model_name: str, prompt: str) -> Dict[str, Any]:
    if model_name.startswith("mock:"):
        return {"model": model_name, "text": mock_call_model(prompt), "error": None}

    if model_name.startswith("hf:"):
        model_id = model_name.split("hf:", 1)[1]
        try:
            text = call_hf(model_id, prompt)
            return {"model": model_name, "text": text, "error": None}
        except Exception as e:
            return {"model": model_name, "text": "", "error": str(e)}

    return {"model": model_name, "text": "", "error": "Provider not configured"}


def main():
    prompts = load_prompts(PROMPTS_PATH)

    # FAST mode
    if FAST_N > 0:
        prompts = prompts[:FAST_N]
        print(f"[INFO] FAST_N enabled -> running only first {FAST_N} prompts")

    # Clean previous results
    if os.path.exists(RESULTS_PATH):
        os.remove(RESULTS_PATH)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Build MODELS list
    models: List[str] = ["mock:model-v1"]
    if not SKIP_HF:
        for m in HF_MODELS:
            models.append(f"hf:{m}")
    else:
        print("[INFO] SKIP_HF=1 -> running only mock model")

    print("[INFO] Models to run:")
    for m in models:
        print(" -", m)

    # Run evaluation
    for p in prompts:
        prompt_id = p["id"]
        for model in models:
            out = call_model(model, p["prompt"])

            record = {
                "run_id": run_id,
                "timestamp_utc": utc_now_iso(),
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

            time.sleep(SLEEP_BETWEEN_CALLS)

    print(f"[DONE] results written to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()