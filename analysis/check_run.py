"""Sanity checks for an eval run, before trusting its scores.

Flags three problems seen in the first pilot:
  * truncated answers (stop_reason "max_tokens"), which score badly for the wrong reason
  * empty answers or unparseable grader output
  * answers that mention the audit, which would reveal the condition to the grader

Usage:
    python analysis/check_run.py logs/pilot
"""

from __future__ import annotations

import argparse
import re

import pandas as pd
from inspect_ai.log import list_eval_logs, read_eval_log

# Words that would reveal the supervised/unsupervised condition. Privacy words are
# left out on purpose: both conditions promise the same confidentiality.
LEAK_PATTERN = re.compile(
    r"\baudit|safety team|\blogged\b|\bmonitor|"
    r"tarkast|turvallisuustiim|tallenne",
    re.IGNORECASE,
)


def leak_terms(text: str) -> list[str]:
    """Condition-revealing terms found in an answer, lower-cased and deduplicated."""
    return sorted({m.group(0).lower() for m in LEAK_PATTERN.finditer(text or "")})


def summarise(rows: pd.DataFrame) -> pd.DataFrame:
    """Count problems per model and condition from rows of sample results."""
    rows = rows.assign(
        truncated=rows["stop_reason"].eq("max_tokens"),
        empty=rows["completion"].fillna("").str.strip().eq(""),
        leak=rows["completion"].fillna("").map(lambda t: bool(leak_terms(t))),
    )
    grouped = rows.groupby(["model", "condition"])
    return pd.DataFrame(
        {
            "samples": grouped.size(),
            "truncated": grouped["truncated"].sum(),
            "empty": grouped["empty"].sum(),
            "parse_error": grouped["parse_error"].sum(),
            "leak": grouped["leak"].sum(),
        }
    ).astype(int)


def logs_to_rows(log_dir: str) -> pd.DataFrame:
    rows = []
    for info in list_eval_logs(log_dir):
        log = read_eval_log(info)
        for sample in log.samples or []:
            out = sample.output
            choice = out.choices[0] if out and out.choices else None
            score = next(iter((sample.scores or {}).values()), None)
            rows.append(
                {
                    "model": log.eval.model,
                    "id": sample.id,
                    "condition": sample.metadata.get("condition"),
                    "stop_reason": choice.stop_reason if choice else None,
                    "completion": out.completion if out else "",
                    "parse_error": bool(score and (score.metadata or {}).get("parse_error")),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir")
    args = parser.parse_args()

    rows = logs_to_rows(args.log_dir)
    if rows.empty:
        raise SystemExit("No samples found.")
    table = summarise(rows)
    print(table.to_markdown())

    problems = rows[
        rows["stop_reason"].eq("max_tokens")
        | rows["completion"].fillna("").map(lambda t: bool(leak_terms(t)))
    ]
    for _, row in problems.iterrows():
        print(f"- {row['model']} {row['id']}: stop={row['stop_reason']} "
              f"leak={leak_terms(row['completion'])}")
    if table[["truncated", "empty", "parse_error", "leak"]].to_numpy().sum():
        raise SystemExit("Problems found: fix or explain them before using the scores.")
    print("No problems found.")


if __name__ == "__main__":
    main()
