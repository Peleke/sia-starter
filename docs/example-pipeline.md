# The example pipeline behind the posts

The series uses one of our own builds as its running example. This page explains it for anyone dropping in.

## What it does
A product changelog entry goes in. Out comes a short video script in which every claim is backed by a source. It's built in TypeScript with Ax. The stages:
1. read the entry and gather its links
2. pull out the entry's claims, then profile and tag them
3. **rank the claims by impact**, using a model that compares them two at a time
4. check claims against the linked pages and the web, and record the evidence; it pauses for a person's approval when it reaches its limits

Planning the video's beats and rendering come later.

## The step the posts measure: ranking
- A model judge orders an entry's claims by impact.
- We score that order against a **gold ranking** with **pair agreement**: the share of claim pairs ordered the same way as the gold.
- **The gold set:** a handful of real changelog entries. The assistant drafted the rankings, a person corrected them, and nothing counts as gold until a person has reviewed it.

## Experiment E-a: do labeled demos help the judge?
Pre-registered: hypothesis, metric, number of runs and threshold were written down before running.
- **Design:** give the judge k ∈ {0, 2, 4, 8} labeled example pairs, drawn from the gold rankings. 5 groups (one per gold entry) × 3 runs each. A group never sees examples from its own entry (leave-one-out). k = 0 is also run 3 times, which shows how much the score moves on its own.
- **Result:** mean pair agreement rose from 0.553 (k = 0) to 0.631 (k = 8). The gain is +0.077, with an approximate 95% interval of [−0.012, 0.167]. **The interval includes zero, so the result is inconclusive.**
- **What it taught us:**
  - With 5 groups the interval is too wide to tell a real gain from noise.
  - Running the no-demo version 3 times showed how much a score moves without any change.
  - The next step is more gold entries, not more runs on the same five.

Reproduce it: `uv run python notebooks/ea_dose_curve.py`.

## Where it sits in the loop
| slot | in this pipeline |
|---|---|
| signal | the person-corrected gold rankings |
| metric | pair agreement |
| search | choosing how many demos (so far, by a fixed rule; an optimizer that chooses *which* demos is the next step) |
| artifact | the demo block given to the judge |

**Honest status:** the pipeline has gold sets and metrics for its steps, but no optimizer has searched any of them yet. When one does, we'll write it up the same way.
