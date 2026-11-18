# Gold set plan: <agent name> (<loop>)

The examples your metric runs on, planned before you score anything.

| agent | its job, in one sentence | platform (see where-to-look) | repo / export @ commit | would it run as stored? | did you run it? |
|---|---|---|---|---|---|
| | | | | yes / no (reasons below) | yes / no |

_Notes (reasons it wouldn't run, assumptions you made):_


**Metric it serves:** `<metric>` scores `<the output it judges: one field, or the whole response>`

**Group key** (what produces near-duplicates; one group = one independent unit): <source / scenario / author / …>

## Example schema
| field | input or label | where it comes from |
|---|---|---|
| | | |
| `label_as_of` (if the right answer can change: prices, rankings, live web data) | label | the date the label was checked |

_Example (a support bot): `message` (input, from past conversations) · `expected_team` (label, a person checks each) · `scenario` (group key)._

**Multi-turn agents** (a chat app that asks questions back): one example is a whole conversation. Script the user: a short brief per example saying how the user answers the agent's questions, so reruns are comparable.

## Sources (mix them; each covers gaps the others miss)
- [ ] real inputs from production (see where-to-look): <location>, target <n groups>
- [ ] hand-written cases (edge cases you know about): target <n>
- [ ] model-made variants of checked examples: target <n>
- [ ] for a step in the middle of a pipeline: cached outputs of the steps before it, used as its inputs

## Labeling
- [ ] the agent's own rules are settled first (if its prompt contradicts itself, decide which policy the labels follow)
- [ ] personal data (names, emails) is removed or masked
- [ ] labels already exist, written by people: <where>
- [ ] a model drafts labels; a person checks every one
- [ ] the labeling guide is written down (what "acceptable" means for each field)

## Split (before you score anything; split by group, so near-duplicates stay together)
- [ ] **train**: demos come from here (can be empty when the search is a person editing the prompt)
- [ ] **validation**: where the search picks a winner. With an optimizer, make this larger than train. With a person as the search, this is the set you judge proposed changes on.
- [ ] **test**: held back, touched once, at the end

Tick a box when it's part of the plan; note "done" when it's done.

**Scoring for the script:** if a group holds several items, the score for that group in one run is the mean of its item scores. One row per group × arm × run.

**Size:** count groups, not items. One test case is not a test set. Thirty items from five sources are five groups. To see how much your score moves on its own, run the baseline twice on each group and give the script those rows (arm 0, reps 1 and 2): it reports an A/A interval, the smallest gain you could tell apart from noise.

---
Agent version: `gold-set` in brunnr (optional; see the README section "Agent versions"). Not published yet.
