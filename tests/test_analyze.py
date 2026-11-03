import importlib.util
from pathlib import Path

import pandas as pd

ANALYZE = Path(__file__).resolve().parents[1] / "analysis" / "analyze.py"
spec = importlib.util.spec_from_file_location("analyze", ANALYZE)
analyze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze)


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
