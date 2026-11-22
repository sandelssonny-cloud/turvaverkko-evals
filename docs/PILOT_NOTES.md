# Pilot notes

What the first real-model pilot (2026-11-07) taught us. No scores are reported here: the scenarios are unreviewed drafts, both evaluated models and the grader came from one provider, and each sample ran once. The numbers would say more about those limits than about the models.

## What we ran
- Two evaluated models and a separate grader model, all from one provider.
- Six draft scenarios × two languages × two conditions × one epoch = 48 answers, each graded once.
- A small smoke test first, with one model and English only.

## What we learned

**1. Reasoning models need a bigger token budget.**
With `max_tokens=800`, the smoke test cut off 5 of 12 answers. Most of the budget went on hidden reasoning before the visible reply. The truncated answers were in the hardest scenarios, so the scores would have been lowest exactly where it matters, for a reason that has nothing to do with the model's behaviour. The limit is now 4000, and `analysis/check_run.py` flags any truncated answer.

**2. Run the cheap test before the real one.**
The smoke test also found that `-T languages=fi,en` crashed, because the Inspect CLI turns it into a list. Both bugs would have wasted a full run.

**3. The audit did not leak into the answers.**
No answer mentioned audits, logging or a safety team, so the grader stayed blind to the condition. Answers did mention confidentiality, in both conditions, which is expected because both prompts promise it.

**4. The shared confidentiality sentence shapes what a "good" answer is.**
In the "don't tell anyone, promise?" scenario, models promised secrecy in both conditions. This does not bias the comparison, because it happens in both, but it raises a question for the professionals reviewing the scenarios: is that the setup we want, and what should a good answer do here?

**5. Finnish answers named real services.**
Answers pointed to real Finnish youth services. Whether models get these right in small languages, or invent them, is worth measuring on its own. It is now on the roadmap.

## Why the design changed before the pilot
The first draft compared a prompt saying a youth worker reads the chats with one saying the chats are fully private. A model could then correctly rely on the youth worker, and could honestly promise secrecy only in the private condition. A score gap would not have shown misbehaviour. The conditions now differ only in whether the model's replies are audited, and the audit never reaches the young person.
