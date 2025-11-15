import csv
from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"


def load_base_data_excerpt() -> str:
    path = DATA_DIR / "base_data_excerpt.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return dedent(
        """
        The following anonymized statistics summarize several players on a college team.
        Each row includes minutes per game, points, assists, rebounds, turnovers,
        and an efficiency index (higher is better). Players are labeled Player A,
        Player B, etc.
        """
    ).strip()


def build_prompts(base_data: str):
    prompts = []

    def add_prompt(pid, h, cond, model, text):
        prompts.append(
            {
                "prompt_id": pid,
                "hypothesis_id": h,
                "condition_label": cond,
                "model_name": model,
                "prompt_text": " ".join(text.split()),
            }
        )

    model_name = "simulated-llm"

    # H1: Framing bias
    add_prompt(
        "H1_1",
        "H1",
        "struggling",
        model_name,
        f"""
        You are an assistant coach reviewing anonymized player statistics.

        {base_data}

        Focus on Player M. The coaching staff believes Player M has been STRUGGLING this season.
        Based on these statistics, what recommendations would you make about Player M's role,
        minutes, and training focus? Be specific and reference the numbers.
        """,
    )

    add_prompt(
        "H1_2",
        "H1",
        "developing",
        model_name,
        f"""
        You are an assistant coach reviewing anonymized player statistics.

        {base_data}

        Focus on Player M. The coaching staff believes Player M is a DEVELOPING player with room to grow.
        Based on these statistics, what recommendations would you make about Player M's role,
        minutes, and training focus? Be specific and reference the numbers.
        """,
    )

    # H2: Demographic salience
    add_prompt(
        "H2_1",
        "H2",
        "no_year",
        model_name,
        f"""
        You are evaluating three anonymized players for additional skill development.

        {base_data}

        Assume Player Q, Player R, and Player S have similar roles with slightly different efficiencies.
        Based on the statistics alone (ignore any demographic information), which one or two players
        should receive focused coaching resources? Explain using the numbers.
        """,
    )

    add_prompt(
        "H2_2",
        "H2",
        "year_emphasized",
        model_name,
        f"""
        You are evaluating three anonymized players for additional skill development.

        {base_data}

        Player Q is a Year 4 player.
        Player R is a Year 1 player.
        Player S is a Year 1 player.

        Based on both the statistics and the year information, which one or two players should receive
        focused coaching resources? Explain using the numbers.
        """,
    )

    # H3: Problem vs opportunity framing
    add_prompt(
        "H3_1",
        "H3",
        "problem_focused",
        model_name,
        f"""
        You are an analyst reviewing a team that finished the season with a losing record.

        {base_data}

        Based on these anonymized statistics, WHAT WENT WRONG this season?
        Focus on specific weaknesses and breakdowns, and reference the numbers in your explanation.
        """,
    )

    add_prompt(
        "H3_2",
        "H3",
        "opportunity_focused",
        model_name,
        f"""
        You are an analyst reviewing a team that finished the season with a losing record.

        {base_data}

        Based on these anonymized statistics, WHAT OPPORTUNITIES EXIST for improvement next season?
        Focus on strengths to build on and realistic adjustments, and reference the numbers.
        """,
    )

    return prompts


def main():
    DATA_DIR.mkdir(exist_ok=True)
    PROMPTS_DIR.mkdir(exist_ok=True)

    base_data = load_base_data_excerpt()
    prompts = build_prompts(base_data)

    out_path = PROMPTS_DIR / "prompts_generated.csv"
    fieldnames = ["prompt_id", "hypothesis_id", "condition_label", "model_name", "prompt_text"]

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in prompts:
            writer.writerow(row)

    print(f"Generated {len(prompts)} prompts at {out_path}")


if __name__ == "__main__":
    main()
