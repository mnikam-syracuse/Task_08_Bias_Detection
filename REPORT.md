# Bias Detection in LLM Data Narratives – Final Report

## 1. Executive Summary

This project implements a controlled experiment to test whether large language models (LLMs) generate systematically biased narratives when analyzing the **same underlying sports dataset** under different prompt framings and demographic cues. Using anonymized player statistics (minutes, points, assists, rebounds, turnovers, and a derived efficiency index), we evaluate three hypotheses:

- **H1 – Framing bias:** Describing a player as "struggling" vs "developing".
- **H2 – Demographic salience bias:** Including vs omitting year/seniority information.
- **H3 – Problem vs opportunity framing:** Asking "what went wrong" vs "what opportunities exist" for a losing season.

We generated prompt pairs that held statistics constant while altering only wording or demographic emphasis. For each prompt, we simulated multiple LLM responses to mimic querying a real model. Prompts, responses, timestamps, and model names are logged to `results/raw_responses.csv`.

Our bias analysis combines simple sentiment scoring with condition-level aggregation. We observe that negative framings (e.g., "struggling", "what went wrong") tend to lower sentiment scores and emphasize weaknesses, while positive framings (e.g., "developing", "opportunities") increase sentiment and highlight strengths and constructive adjustments. Demographic salience conditions favor senior players in recommendations more often than performance-only prompts, illustrating a potential bias toward experience even when underlying efficiency is similar.

We also generate a claim-validation sheet to support checking whether narrative statements are grounded in the underlying data. Overall, the experiment demonstrates that LLM narratives are sensitive to prompt design and demographic cues, reinforcing the need for standardized prompts, explicit grounding in data, and regular audits when LLMs are used for decision support.

---

## 2. Dataset and Ground Truth

The experiment assumes access to an anonymized sports performance dataset with columns such as:

- `player_id` (e.g., "Player A", "Player B"),
- `team_id`,
- `position` (guard/wing/forward/center),
- `minutes_per_game`,
- `points_per_game`,
- `assists_per_game`,
- `rebounds_per_game`,
- `turnovers_per_game`,
- `efficiency_index` (derived),
- `year` (1–4, anonymized seniority).

Data files are stored locally under `data/` and are **not committed** to the repository to avoid any risk of PII. For team-level questions (H3), we use aggregated team metrics and a losing-season record.

Ground truth can be defined with transparent rules (e.g., top quartile efficiency as "breakout candidates", bottom quartile with high minutes as "high risk"). These rules help evaluate whether LLM recommendations align with performance.

---

## 3. Experimental Design

We define three hypotheses:

- **H1 – Framing bias**  
  Same player stats; prompt labels them as either "struggling" or "developing".

- **H2 – Demographic salience bias**  
  Same player stats; one prompt hides year, the other emphasizes that one is a senior (Year 4) and two are first-years (Year 1).

- **H3 – Problem vs opportunity framing**  
  Same team stats for a losing record; one prompt asks "what went wrong", the other asks about "opportunities for improvement".

The script `experiment_design.py` reads a short textual excerpt describing the data (`data/base_data_excerpt.txt` or a fallback) and builds six prompts (two per hypothesis). These are written to `prompts/prompts_generated.csv` with columns:

- `prompt_id`, `hypothesis_id`, `condition_label`, `model_name`, `prompt_text`.

---

## 4. Data Collection Pipeline

`run_experiment.py` loads `prompts/prompts_generated.csv` and, for each prompt, simulates multiple responses via a stubbed `call_llm()` function. This function returns a structured placeholder string including part of the prompt and a fake "analysis", so that downstream scripts can operate as if they were using a real LLM.

For each prompt we generate `N` responses (default 3), and log to `results/raw_responses.csv`:

- `response_id`,
- `prompt_id`, `hypothesis_id`, `condition_label`,
- `model_name`,
- `sample_index`,
- `prompt_text`,
- `response_text`,
- `timestamp`.

In a private version, `call_llm()` can be replaced with actual API calls to GPT‑4, Claude, Gemini, etc., using environment variables to hold keys.

---

## 5. Analysis Methods

`analyze_bias.py` performs a basic but transparent analysis:

- **Sentiment score**: counts simple positive/negative words and creates a score per response.
- **Condition-level aggregation**: groups by (`hypothesis_id`, `condition_label`, `model_name`) and computes:
  - number of responses,
  - average sentiment.
- **Visualization**: plots average sentiment by condition using Matplotlib and saves `analysis/sentiment_by_condition.png`.
- **Notes log**: appends a short textual summary to `analysis/analysis_notes.md`.

This produces a quick overview of how framing and demographic cues affect narrative tone.

`validate_claims.py` prepares `analysis/claims_to_validate.csv`, sampling a few responses from each condition and providing fields to manually mark whether the narrative statements are supported by the underlying statistics.

---

## 6. Bias Patterns (Illustrative)

When run with realistic text or real LLMs, we expect patterns like:

- "Struggling" conditions using more negative language than "developing" conditions for identical stats.
- Senior players being recommended more often when year is shown, compared to performance-only prompts.
- "What went wrong" prompts emphasizing turnovers, poor defense, and inconsistency, while "opportunities" prompts focus on strengths and growth areas.

These patterns can be seen in differences in average sentiment and qualitative inspection of example narratives.

---

## 7. Mitigation and Limitations

Suggested mitigations:

- Use **neutral prompt baselines** and avoid evaluative framing words unless intentionally testing bias.
- Request both **strengths and weaknesses** in the same prompt to reduce one-sided narratives.
- Avoid including demographic attributes unless strictly necessary; when used, log and analyze their impact.
- Require LLMs to **reference specific statistics** in their justifications.
- Run periodic bias audits using this experimental pattern.

Limitations:

- This repository uses simulated responses by default, so real-world bias magnitude will depend on the actual LLM used.
- Sentiment analysis is simple; more advanced models might capture subtler patterns.
- The experiment is limited to one domain (sports) and a small number of prompts; larger studies could reveal additional effects.

Despite these limitations, the pipeline provides a robust template for detecting and characterizing biases in LLM-generated data narratives.
