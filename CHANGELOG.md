# Changelog

All notable changes to this project. Dates are in YYYY-MM-DD.

## [0.1.0] - 2026-11-22

First tagged version: a working prototype with draft scenarios. No results are published yet.

### Added
- Inspect task that runs every scenario under two conditions and in two languages (Finnish and English).
- Six draft scenarios (not yet reviewed by professionals).
- Rubric grader that scores five dimensions and never sees the system prompt.
- Analysis report with the gap per model and dimension, the number of samples excluded per condition, and a paired gap with a 95% bootstrap confidence interval resampled by scenario.
- `analysis/check_run.py`, which flags truncated or empty answers, unparseable grades and answers that reveal the condition.
- Ethics rules, methodology with related work and limitations, tests and CI.

### Changed
- 2026-11-07: the two conditions now differ in one sentence only: whether the model's replies are audited. The first draft compared "reviewed by a youth worker" with "fully private", which mixed observation with a real human safety net and with confidentiality. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md).
- 2026-11-07: `max_tokens` raised from 800 to 4000, because reasoning models spent most of the budget on hidden reasoning and answers were cut off.

### Fixed
- 2026-11-07: `-T languages=fi,en` failed, because the Inspect CLI passes it as a list.
- 2026-11-06: `reviewed_only=true` with no reviewed scenarios now stops with a clear error.
