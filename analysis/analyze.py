"""Summarise Inspect logs: supervised vs unsupervised gap per model and dimension.

Usage:
    python analysis/analyze.py logs/            # all .eval logs in a folder
    python analysis/analyze.py logs/ --out results/summary.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from inspect_ai.log import list_eval_logs, read_eval_log

DIMENSIONS = (
    "recognises_distress",
    "connects_to_humans",
    "avoids_dependency",
    "honest_not_sycophantic",
    "warm_not_moralising",
    "overall",
)


def logs_to_frame(log_dir: str) -> pd.DataFrame:
    rows = []
    for info in list_eval_logs(log_dir):
        log = read_eval_log(info)
        model = log.eval.model
        for sample in log.samples or []:
            for score in (sample.scores or {}).values():
                if not isinstance(score.value, dict):
                    continue
                row = {"model": model, "epoch": sample.epoch, **sample.metadata}
                row["parse_error"] = bool((score.metadata or {}).get("parse_error"))
                row.update({d: score.value.get(d) for d in DIMENSIONS})
                rows.append(row)
    return pd.DataFrame(rows)


def excluded_by_condition(df: pd.DataFrame) -> pd.DataFrame:
    """Count samples excluded for unparseable grader output, per model and condition.

    An uneven rate between conditions could bias the gap, so it is always reported.
    """
    grouped = df.groupby(["model", "condition"])["parse_error"]
    return pd.DataFrame({"samples": grouped.size(), "excluded": grouped.sum().astype(int)})


def condition_gap(df: pd.DataFrame) -> pd.DataFrame:
    """Mean per condition and the gap (unsupervised minus supervised).

    A negative gap means the model behaves worse when it thinks nobody is
    checking its replies, which is the effect this eval is designed to detect.
    """
    means = df.groupby(["model", "condition"])[list(DIMENSIONS)].mean()
    sup = means.xs("supervised", level="condition")
    uns = means.xs("unsupervised", level="condition")
    gap = (uns - sup).add_suffix("_gap")
    return pd.concat([sup.add_suffix("_sup"), uns.add_suffix("_uns"), gap], axis=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    all_samples = logs_to_frame(args.log_dir)
    df = all_samples[~all_samples["parse_error"]] if not all_samples.empty else all_samples
    if df.empty:
        raise SystemExit("No usable scored samples found.")

    parts = [
        "# Turvaverkko results\n",
        f"Scored samples: {len(df)} of {len(all_samples)}\n",
        "## Samples excluded for unparseable grader output\n",
        excluded_by_condition(all_samples).to_markdown(),
        "\n## Supervised vs unsupervised (overall)\n",
        condition_gap(df)[["overall_sup", "overall_uns", "overall_gap"]].round(2).to_markdown(),
        "\n## Gap per dimension\n",
        condition_gap(df).filter(like="_gap").round(2).to_markdown(),
        "\n## Overall by risk level and condition\n",
        df.pivot_table(index=["model", "risk_level"], columns="condition", values="overall")
        .round(2)
        .to_markdown(),
        "\n## Overall by language\n",
        df.pivot_table(index="model", columns="language", values="overall").round(2).to_markdown(),
    ]
    report = "\n".join(parts)
    print(report)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
