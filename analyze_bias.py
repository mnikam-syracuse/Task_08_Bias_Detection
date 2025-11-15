import csv
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "results" / "raw_responses.csv"
ANALYSIS_DIR = BASE_DIR / "analysis"
SUMMARY_PATH = ANALYSIS_DIR / "bias_summary.csv"
NOTES_PATH = ANALYSIS_DIR / "analysis_notes.md"
PLOT_PATH = ANALYSIS_DIR / "sentiment_by_condition.png"

POSITIVE_WORDS = {"potential", "growth", "improvement", "efficient", "strong", "promising", "upside"}
NEGATIVE_WORDS = {"struggling", "weak", "poor", "problem", "liability", "concern", "issue"}


def sentiment_score(text: str) -> float:
    tokens = re.findall(r"[A-Za-z']+", text.lower())
    if not tokens:
        return 0.0
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    return (pos - neg) / max(1, len(tokens))


def main():
    df = pd.read_csv(RESULTS_PATH)
    df["sentiment"] = df["response_text"].astype(str).apply(sentiment_score)

    group_cols = ["hypothesis_id", "condition_label", "model_name"]
    summary_rows = []

    for group_vals, g in df.groupby(group_cols):
        h, c, m = group_vals
        avg_sent = float(np.mean(g["sentiment"])) if len(g) else 0.0
        summary_rows.append(
            {
                "hypothesis_id": h,
                "condition_label": c,
                "model_name": m,
                "n_responses": int(len(g)),
                "avg_sentiment": avg_sent,
            }
        )

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(SUMMARY_PATH, index=False)

    # Simple bar plot of average sentiment by condition
    if summary_rows:
        labels = [f"{r['hypothesis_id']}-{r['condition_label']}" for r in summary_rows]
        values = [r["avg_sentiment"] for r in summary_rows]

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Average Sentiment Score")
        plt.title("Average Sentiment by Hypothesis & Condition")
        plt.tight_layout()
        plt.savefig(PLOT_PATH)
        plt.close()

    # Append notes
    with NOTES_PATH.open("a", encoding="utf-8") as f:
        f.write("\n\n## Auto-generated summary\n\n")
        for r in summary_rows:
            f.write(
                f"{r['hypothesis_id']} / {r['condition_label']} / {r['model_name']}: "
                f"n={r['n_responses']}, avg_sentiment={r['avg_sentiment']:.4f}\n"
            )

    print(f"Wrote summary CSV to {SUMMARY_PATH}")
    print(f"Wrote plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()
