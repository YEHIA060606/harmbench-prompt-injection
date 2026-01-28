import csv
import os
from collections import defaultdict

SCORES_PATH = os.path.join("data", "scores.csv")

def load_scores(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # normalize types
            r["is_correct"] = int(r["is_correct"]) if r.get("is_correct") else 0
            rows.append(r)
    return rows

def safe_div(num: int, den: int) -> float:
    return (num / den) if den else 0.0

def pct(x: float) -> str:
    return f"{x*100:.1f}%"

def main():
    if not os.path.exists(SCORES_PATH):
        print(f"Missing {SCORES_PATH}. Run 03_score_results.py first.")
        return

    rows = load_scores(SCORES_PATH)
    total = len(rows)

    # 1) Global accuracy
    correct = sum(r["is_correct"] for r in rows)
    global_acc = safe_div(correct, total)

    # 2) Accuracy by type (standard vs contextual)
    by_type = defaultdict(lambda: {"n": 0, "correct": 0})
    for r in rows:
        t = r.get("type", "unknown")
        by_type[t]["n"] += 1
        by_type[t]["correct"] += r["is_correct"]

    # 3) Accuracy by category
    by_cat = defaultdict(lambda: {"n": 0, "correct": 0})
    for r in rows:
        c = r.get("category", "unknown")
        by_cat[c]["n"] += 1
        by_cat[c]["correct"] += r["is_correct"]

    # 4) Refusal rate (predicted_behavior == refuse)
    refused = sum(1 for r in rows if (r.get("predicted_behavior") == "refuse"))
    refusal_rate = safe_div(refused, total)

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total samples: {total}")
    print(f"Global accuracy: {pct(global_acc)} ({correct}/{total})")
    print(f"Refusal rate (predicted): {pct(refusal_rate)} ({refused}/{total})")

    print("\n=== ACCURACY BY TYPE ===")
    for t, stats in sorted(by_type.items()):
        acc = safe_div(stats["correct"], stats["n"])
        print(f"- {t}: {pct(acc)} ({stats['correct']}/{stats['n']})")

    print("\n=== ACCURACY BY CATEGORY ===")
    # sort categories by lowest accuracy first (more vulnerable)
    cat_items = []
    for c, stats in by_cat.items():
        acc = safe_div(stats["correct"], stats["n"])
        cat_items.append((acc, c, stats["correct"], stats["n"]))
    for acc, c, cor, n in sorted(cat_items, key=lambda x: x[0]):
        print(f"- {c}: {pct(acc)} ({cor}/{n})")

    # Save a small report file for your docs/rapport
    out_path = os.path.join("data", "analysis_summary.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("SUMMARY\n")
        f.write(f"Total samples: {total}\n")
        f.write(f"Global accuracy: {pct(global_acc)} ({correct}/{total})\n")
        f.write(f"Refusal rate (predicted): {pct(refusal_rate)} ({refused}/{total})\n\n")

        f.write("ACCURACY BY TYPE\n")
        for t, stats in sorted(by_type.items()):
            acc = safe_div(stats["correct"], stats["n"])
            f.write(f"{t}: {pct(acc)} ({stats['correct']}/{stats['n']})\n")

        f.write("\nACCURACY BY CATEGORY\n")
        for acc, c, cor, n in sorted(cat_items, key=lambda x: x[0]):
            f.write(f"{c}: {pct(acc)} ({cor}/{n})\n")

    print(f"\n[OK] Wrote analysis summary to {out_path}")

if __name__ == "__main__":
    main()
