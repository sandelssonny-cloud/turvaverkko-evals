"""Inspect task: does a model treat vulnerable young users differently when
it believes nobody is watching?

Run (see README):
    inspect eval src/turvaverkko/task.py \
        --model <provider>/<model> \
        --model-role grader=<provider>/<grader-model>
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import generate

from turvaverkko.dataset import build_dataset
from turvaverkko.scorer import rubric_scorer

DEFAULT_SCENARIOS = Path(__file__).resolve().parents[2] / "scenarios"


@task
def turvaverkko(
    scenarios: str = str(DEFAULT_SCENARIOS),
    languages: str = "fi,en",
    reviewed_only: bool = False,
    grader_model: str | None = None,
    epochs: int = 3,
) -> Task:
    """Main eval.

    Args:
        scenarios: YAML file or folder of scenarios.
        languages: comma-separated subset of fi,en.
        reviewed_only: only run scenarios a professional has signed off.
        grader_model: explicit grader; otherwise uses --model-role grader=...
        epochs: repeats per sample (responses vary; 3 gives a usable estimate).
    """
    return Task(
        dataset=build_dataset(
            scenarios,
            languages=[lang.strip() for lang in languages.split(",")],
            reviewed_only=reviewed_only,
        ),
        solver=[generate()],
        scorer=rubric_scorer(grader_model=grader_model),
        config=GenerateConfig(temperature=0.7, max_tokens=800),
        epochs=epochs,
    )
