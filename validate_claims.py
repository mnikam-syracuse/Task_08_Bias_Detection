from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "results" / "raw_responses.csv"
ANALYSIS_DIR = BASE_DIR / "analysis"
OUT_PATH = ANALYSIS_DIR / "claims_to_validate.csv"


def main():
    df = pd.read_csv(RESULTS_PATH)
    rows = []

    # sample up to 5 per (hypothesis, condition)
    for (h, c), g in df.groupby(["hypothesis_id", "condition_label"]):
        for _, r in g.head(5).iterrows():
            excerpt = str(r["response_text"])[:300].replace("\n", " ")
            rows.append(
                {
                    "response_id": r["response_id"],
                    "hypothesis_id": h,
                    "condition_label": c,
                    "model_name": r["model_name"],
                    "response_excerpt": excerpt,
                    "is_supported_by_data": "",
                    "notes": "",
                }
            )

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT_PATH, index=False)
    print(f"Wrote claim-validation template to {OUT_PATH}")


if __name__ == "__main__":
    main()
