import pandas as pd

HF_URL = "https://huggingface.co/datasets/Yehiaa06/harmbench-evaluation/resolve/main/prompts.csv"

def main():
    # Tolerant CSV read: skip bad lines
    df = pd.read_csv(
        HF_URL,
        engine="python",
        on_bad_lines="skip",   # skips problematic rows
    )

    print("Columns found:", list(df.columns))
    print("Rows loaded:", len(df))
    print(df.head())

    out_path = "data/prompts_from_hf.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] Saved prompts from HF to: {out_path}")

if __name__ == "__main__":
    main()