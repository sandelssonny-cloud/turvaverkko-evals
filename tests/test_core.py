from pathlib import Path

import pytest

from turvaverkko.dataset import (
    CONDITIONS,
    LANGUAGES,
    PROMPT_INTRO,
    PROMPT_PRIVACY,
    SYSTEM_PROMPTS,
    ScenarioError,
    build_dataset,
    expand,
    load_scenarios,
)
from turvaverkko.scorer import DIMENSIONS, parse_grade

SCENARIOS = Path(__file__).resolve().parents[1] / "scenarios"


def test_seed_scenarios_load():
    scenarios = load_scenarios(SCENARIOS)
    assert len(scenarios) >= 6


def test_expand_covers_every_language_and_condition():
    scenarios = load_scenarios(SCENARIOS)
    samples = expand(scenarios)
    assert len(samples) == len(scenarios) * len(LANGUAGES) * len(CONDITIONS)


def test_conditions_differ_only_in_system_prompt():
    scenarios = load_scenarios(SCENARIOS)[:1]
    sup, uns = expand(scenarios, languages=["en"])
    assert sup.input[0].text != uns.input[0].text
    assert [m.text for m in sup.input[1:]] == [m.text for m in uns.input[1:]]


@pytest.mark.parametrize("lang", LANGUAGES)
def test_conditions_differ_only_in_the_audit_sentence(lang):
    sup = SYSTEM_PROMPTS["supervised"][lang]
    uns = SYSTEM_PROMPTS["unsupervised"][lang]
    for prompt in (sup, uns):
        assert prompt.startswith(PROMPT_INTRO[lang])
        assert prompt.endswith(PROMPT_PRIVACY[lang])
    assert sup != uns


def test_token_limit_leaves_room_for_reasoning():
    # A low limit truncated answers from reasoning models; see task.py.
    from turvaverkko.task import MAX_TOKENS

    assert MAX_TOKENS >= 4000


@pytest.mark.parametrize("value", ["fi,en", ["fi", "en"], "fi, en"])
def test_parse_languages_accepts_cli_forms(value):
    from turvaverkko.task import parse_languages

    assert parse_languages(value) == ["fi", "en"]


def test_reviewed_only_filters_drafts():
    scenarios = load_scenarios(SCENARIOS)
    assert expand(scenarios, reviewed_only=True) == [] or all(
        s.metadata["reviewed"] for s in expand(scenarios, reviewed_only=True)
    )


def test_empty_dataset_gives_clear_error(tmp_path):
    drafts = tmp_path / "drafts.yaml"
    drafts.write_text(
        "scenarios:\n  - {id: x, theme: t, risk_level: low, author: a, reviewed: false,"
        " message: {fi: moi, en: hi}}\n",
        encoding="utf-8",
    )
    with pytest.raises(ScenarioError, match="reviewed"):
        build_dataset(drafts, reviewed_only=True)


def test_missing_language_is_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "scenarios:\n  - {id: x, theme: t, risk_level: low, author: a, reviewed: false,"
        " message: {en: hi}}\n",
        encoding="utf-8",
    )
    with pytest.raises(ScenarioError):
        load_scenarios(bad)


def test_parse_grade_valid():
    text = 'Sure: {"recognises_distress": 4, "connects_to_humans": 5, "avoids_dependency": 5,' \
           ' "honest_not_sycophantic": 3, "warm_not_moralising": 4, "rationale": "ok"}'
    grade = parse_grade(text)
    assert grade is not None
    assert all(dim in grade for dim in DIMENSIONS)


@pytest.mark.parametrize("text", ["no json here", '{"recognises_distress": 9}', "{broken"])
def test_parse_grade_invalid(text):
    assert parse_grade(text) is None
