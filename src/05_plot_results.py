import os
import pandas as pd
import matplotlib.pyplot as plt


SCORES_PATH = os.path.join("data", "scores.csv")
OUT_DIR = os.path.join("data", "plots")


def save_bar(df, x, y, title, out_name):
    plt.figure()
    plt.bar(df[x].astype(str), df[y])
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, out_name)
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[OK] saved {out_path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(SCORES_PATH):
        raise FileNotFoundError(f"Missing {SCORES_PATH}. Run: python src/03_score_results.py")

    df = pd.read_csv(SCORES_PATH)

    needed = {"model", "type", "category", "is_correct"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"scores.csv missing columns: {missing}\nFound columns: {list(df.columns)}")

    # 1) Accuracy by model
    acc_model = df.groupby("model")["is_correct"].mean().reset_index().sort_values("is_correct", ascending=False)
    save_bar(acc_model, "model", "is_correct", "Accuracy by model", "accuracy_by_model.png")

    # 2) Accuracy by category
    acc_cat = df.groupby("category")["is_correct"].mean().reset_index().sort_values("is_correct", ascending=False)
    save_bar(acc_cat, "category", "is_correct", "Accuracy by category", "accuracy_by_category.png")

    # 3) Accuracy by type
    acc_type = df.groupby("type")["is_correct"].mean().reset_index().sort_values("is_correct", ascending=False)
    save_bar(acc_type, "type", "is_correct", "Accuracy by type", "accuracy_by_type.png")

    # 4) Count by category
    cnt_cat = df.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
    save_bar(cnt_cat, "category", "count", "Samples count by category", "count_by_category.png")

    print("[DONE] Plots generated in data/plots/")


if __name__ == "__main__":
    main()