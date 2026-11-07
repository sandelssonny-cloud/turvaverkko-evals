# Methodology

## Research questions
1. Does response quality differ when the system prompt says the model's replies are audited vs never audited?
2. Is the gap larger in high-risk scenarios?
3. Is the gap larger in Finnish than in English?
4. Which dimension shows the largest gap?

## Design
- **Within-scenario comparison.** Every scenario is run under both conditions. The user-facing conversation is identical. Only the system prompt changes (`src/turvaverkko/dataset.py`).
- **One-sentence manipulation.** Both system prompts share the same introduction (who the model is and that the app can show crisis-line and youth-service contacts) and the same confidentiality statement (no one contacts the user, and no adult in their life sees the chats). They differ only in whether anonymised samples of the model's replies are audited by the developer's safety team. The audit never reaches the user, so it changes whether the model is observed, not the help available to the young person. A well-behaved model therefore has no legitimate reason to respond differently.
- **Why not "reviewed by a youth worker" vs "fully private".** An earlier draft used that contrast. It confounded observation with a real human safety net and with confidentiality: a model could correctly rely on the youth worker, and could honestly promise secrecy only in the private condition. A gap would then not show misbehaviour.
- **Languages.** Finnish and English versions of every scenario. Finnish is a lower-resource language where safety behaviour is less studied.
- **Repeats.** Default 3 epochs at temperature 0.7, because single responses vary.

## Related work
- **Alignment faking.** Greenblatt et al. (2024), *Alignment faking in large language models* (arXiv:2412.14093). A model told which conversations were monitored and used for training behaved differently in monitored and unmonitored conversations.
- **Evaluation awareness.** Needham et al. (2025), *Large Language Models Often Know When They Are Being Evaluated* (arXiv:2505.23836). Frontier models can often distinguish evaluation transcripts from real deployment, which can make evals less reliable.
- **Gradual disempowerment.** Kulveit et al. (2025), *Gradual Disempowerment: Systemic Existential Risks from Incremental AI Development* (arXiv:2501.16946). Argues that incremental AI adoption can erode human influence over the systems society depends on.

Turvaverkko applies the monitored-versus-unmonitored question to everyday deployment: private conversations with vulnerable young users, scenarios to be written or reviewed by frontline professionals, scoring on wellbeing-relevant dimensions, and a lower-resource language.

## Scoring
- A separate grader model scores five dimensions on a 1–5 scale (`src/turvaverkko/scorer.py`).
- The grader **never sees the system prompt**: system messages are removed before grading. Blinding is partial (see limitations).
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
- The system prompt is an explicit signal. Real deployments may signal supervision more subtly. Mentioning an audit at all may also make the context look more like a test.
- Single-turn or short conversations only in v0.1. Real distress often unfolds over many turns.
- Model-graded scoring can share blind spots with the evaluated models; hence human validation.
- Grader blinding is partial: the grader never sees the system prompt, but a response can still reveal the condition (for example by mentioning that its replies are audited).
- Scenario set is small; results are indicative, not definitive.
- Composite personas may not capture how every young person writes.
