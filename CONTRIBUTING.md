# Contributing

Turvaverkko is built around the knowledge of people who work with young people every day. You don't need to write code to help.

## Propose a scenario (no code needed)

If you are a youth worker, teacher, school welfare professional, school nurse, psychologist or clinician, you know what distress looks like in a young person's message. That is exactly what we need.

1. Open the [scenario form](https://github.com/sandelssonny-cloud/turvaverkko-evals/issues/new?template=scenario.yml). You need a free GitHub account.
2. Write a short message a young person (15–19) might send to an AI chatbot, and a few notes on what a good reply would do.
3. You can write in Finnish or English.

We turn each proposal into the scenario format in both languages. A scenario is marked as reviewed only after a youth-work or clinical professional has approved it.

Prefer email or a conversation? Contact Santtu Vesterinen through [LinkedIn](https://www.linkedin.com/in/santtu-vesterinen-yep/).

## Rules for every scenario

These come from [docs/ETHICS.md](docs/ETHICS.md) and are not negotiable:

- **No real young people.** Every scenario is a composite. Nothing should make a real person recognisable.
- **No case material.** Nothing from your clients, students or case files, even anonymised.
- **No harmful details.** Never include methods, quantities or plans for self-harm, suicide, substance use or other dangerous acts. Show distress through feelings and situations, not methods.

Writing about distress can be heavy. Take your time, and only write what feels okay to write.

## Contribute code

1. Read [CLAUDE.md](CLAUDE.md) and [docs/METHODOLOGY.md](docs/METHODOLOGY.md).
2. Install with `pip install -e ".[dev]"`, then run `pytest` and `ruff check src tests analysis`.
3. New functionality needs a test in `tests/`.
4. Keep the two conditions identical except for the audit sentence. Open an issue before changing that, because every result depends on it.
