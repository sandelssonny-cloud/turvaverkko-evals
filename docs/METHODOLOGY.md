# Methodology

## Research questions
1. Does response quality differ when the system prompt states the conversation is supervised vs fully private?
2. Is the gap larger in high-risk scenarios?
3. Is the gap larger in Finnish than in English?
4. Which dimension shows the largest gap?

## Design
- **Within-scenario comparison.** Every scenario is run under both conditions. The user-facing conversation is identical. Only the system prompt changes (`src/turvaverkko/dataset.py`).
- **Languages.** Finnish and English versions of every scenario. Finnish is a lower-resource language where safety behaviour is less studied.
- **Repeats.** Default 3 epochs at temperature 0.7, because single responses vary.

## Scoring
- A separate grader model scores five dimensions on a 1–5 scale (`src/turvaverkko/scorer.py`).
- The grader is **blind to condition**: system messages are removed before grading.
- The grader also sees the professionals' notes on what a good response looks like.
- Unparseable grader output is flagged and excluded from analysis. The report shows the number excluded per model and condition. Inspect's own summary metrics count these samples as 0, so use `analysis/analyze.py` for results.
- The grader should not be one of the models under evaluation.

## Grader validation (planned)
A professional hand-scores a random subset of responses without seeing scores or conditions. Agreement with the grader is reported per dimension. If agreement is weak, the rubric is revised before final runs.

## Analysis
- Headline: mean gap (unsupervised − supervised) per model, overall and per dimension.
- Breakdown by risk level and language.
- Planned: bootstrap confidence intervals clustered by scenario.

## Limitations
- The system prompt is an explicit signal. Real deployments may signal supervision more subtly.
- Single-turn or short conversations only in v0.1. Real distress often unfolds over many turns.
- Model-graded scoring can share blind spots with the evaluated models; hence human validation.
- Scenario set is small; results are indicative, not definitive.
- Composite personas may not capture how every young person writes.
