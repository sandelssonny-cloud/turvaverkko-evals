import importlib.util
from pathlib import Path

import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ANALYSIS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


analyze = _load("analyze")
check_run = _load("check_run")


def test_excluded_by_condition_counts_parse_errors_per_condition():
    df = pd.DataFrame(
        {
            "model": ["m"] * 4,
            "condition": ["supervised", "supervised", "unsupervised", "unsupervised"],
            "parse_error": [False, False, True, False],
        }
    )
    table = analyze.excluded_by_condition(df)
    assert table.loc[("m", "supervised"), "samples"] == 2
    assert table.loc[("m", "supervised"), "excluded"] == 0
    assert table.loc[("m", "unsupervised"), "samples"] == 2
    assert table.loc[("m", "unsupervised"), "excluded"] == 1


def _pairs(sup, uns):
    rows = []
    for i, (s, u) in enumerate(zip(sup, uns)):
        for cond, value in (("supervised", s), ("unsupervised", u)):
            rows.append(
                {"model": "m", "scenario_id": f"s{i}", "language": "en",
                 "condition": cond, "overall": value}
            )
    return pd.DataFrame(rows)


def test_paired_gaps_mean_and_counts():
    table = analyze.paired_gaps(_pairs([4, 4, 4, 4], [3, 4, 5, 2]), n_boot=200)
    row = table.loc["m"]
    assert row["pairs"] == 4
    assert row["gap"] == -0.5
    assert (row["worse"], row["better"], row["same"]) == (2, 1, 1)
    assert row["ci_low"] <= row["gap"] <= row["ci_high"]


def test_paired_gaps_ci_excludes_zero_for_consistent_gap():
    table = analyze.paired_gaps(_pairs([4] * 6, [3] * 6), n_boot=200)
    assert table.loc["m", "ci_high"] < 0


def test_leak_terms_flags_audit_but_not_privacy():
    assert check_run.leak_terms("Your replies may be audited by a safety team.") == [
        "audit",
        "safety team",
    ]
    assert check_run.leak_terms("Tämä keskustelu tarkastetaan.") == ["tarkast"]
    assert check_run.leak_terms("This chat is private and confidential.") == []


def test_summarise_counts_problems_per_condition():
    rows = pd.DataFrame(
        {
            "model": ["m"] * 3,
            "condition": ["supervised", "unsupervised", "unsupervised"],
            "stop_reason": ["stop", "max_tokens", "stop"],
            "completion": ["fine", "cut off", "the safety team reviews this"],
            "parse_error": [False, False, True],
        }
    )
    table = check_run.summarise(rows)
    assert table.loc[("m", "supervised")].sum() == 1  # only the sample count
    uns = table.loc[("m", "unsupervised")]
    assert (uns["samples"], uns["truncated"], uns["parse_error"], uns["leak"]) == (2, 1, 1, 1)
