import csv
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = BASE_DIR / "prompts" / "prompts_generated.csv"
RESULTS_PATH = BASE_DIR / "results" / "raw_responses.csv"


def call_llm(prompt: str, model_name: str) -> str:
    """Simulated LLM response.

    This stub generates a deterministic-looking placeholder so that downstream
    analysis has realistic-looking text, but no real API calls are made.
    """
    snippet = prompt[:180].replace("\n", " ")
    return (
        f"[SIMULATED RESPONSE from {model_name}] "
        f"This narrative discusses the given statistics and may exhibit framing effects. Prompt snippet: '{snippet}'..."
    )


def load_prompts(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(samples_per_prompt: int = 3):
    prompts = load_prompts(PROMPTS_PATH)
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "response_id",
        "prompt_id",
        "hypothesis_id",
        "condition_label",
        "model_name",
        "sample_index",
        "prompt_text",
        "response_text",
        "timestamp",
    ]

    with RESULTS_PATH.open("w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        rid = 1
        for row in prompts:
            for s in range(samples_per_prompt):
                response_text = call_llm(row["prompt_text"], row["model_name"])
                writer.writerow(
                    {
                        "response_id": f"R{rid}",
                        "prompt_id": row["prompt_id"],
                        "hypothesis_id": row["hypothesis_id"],
                        "condition_label": row["condition_label"],
                        "model_name": row["model_name"],
                        "sample_index": s,
                        "prompt_text": row["prompt_text"],
                        "response_text": response_text,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                rid += 1
                time.sleep(0.01)

    print(f"Wrote {rid - 1} simulated responses to {RESULTS_PATH}")


if __name__ == "__main__":
    # Simple CLI-style entry; you can adapt to argparse if desired
    main(samples_per_prompt=3)
