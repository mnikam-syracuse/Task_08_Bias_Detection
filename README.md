# Task_08_Bias_Detection

This repository implements a full, reproducible pipeline for Syracuse University OPT **Research Task 08: Bias Detection in LLM Data Narratives**.


## Contents

- `experiment_design.py` – generates prompts for 3 hypotheses (H1, H2, H3)
- `run_experiment.py` – simulates LLM responses and logs them to CSV
- `analyze_bias.py` – computes simple sentiment and generates a plot + summary CSV
- `validate_claims.py` – creates a template CSV to manually mark which claims are supported by data
- `data/` – local-only anonymized dataset (not committed)
- `prompts/` – prompt templates and generated prompts
- `results/` – raw simulated responses
- `analysis/` – summaries, plot, and claim-validation sheet
- `REPORT.md` – final written report

## How to Run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python experiment_design.py
python run_experiment.py --samples_per_prompt 3
python analyze_bias.py
python validate_claims.py
```

Then open:

- `analysis/bias_summary.csv`
- `analysis/sentiment_by_condition.png`
- `analysis/claims_to_validate.csv`
- `REPORT.md`
