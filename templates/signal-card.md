# Signal card: <agent name> (<loop>)

Pick the signal your agent improves from, and the other two slots. Read this after the learning check: its "no"s tell you which slot is missing.

| agent | its job, in one sentence | platform (see where-to-look) | repo / export @ commit | would it run as stored? | did you run it? |
|---|---|---|---|---|---|
| | | | | yes / no (reasons below) | yes / no |

_Notes (reasons it wouldn't run, assumptions you made):_


**My agent gets better when ________________ goes up.**

_Example (a support bot): "…when the share of conversations routed to the right team on the first try goes up." Signal: the routing label (score). Search: an instruction optimizer, scored on validation groups. Artifact: the router's instructions._

## Candidate signals
| candidate | type | where it comes from (`path:line [node-id]`, or see where-to-look) | how often (per run / per day) | cost ($ or person-minutes per item) | outside the model? |
|---|---|---|---|---|---|
| | | | | | |

**Types:**
- **score:** a number per output. Example: test pass rate.
- **preference:** a choice. Example: A vs B, approve / reject, thumbs up / down without a comment.
- **feedback:** free text. Example: a reviewer's comment, or a thumbs-down with a reason. It becomes a metric through a rubric.
- **confidence:** the model's own estimate. It is not an outside signal; don't pick it alone.

**How to choose:** the most frequent, cheapest signal that comes from outside the model. If two are close, keep both, and say which one the search optimizes.

**The signal doesn't exist yet?** That's common. Write where it would attach (e.g. "a 'reviewed rating' column next to the output") and mark the row "proposed". Leave how often / cost as estimates.

## Slots
| slot | options | pick for now |
|---|---|---|
| Signal | from the table above | |
| Search | DSPy `BootstrapFewShot` · `MIPROv2` · `GEPA`; Ax `AxBootstrapFewShot` · `AxGEPA` (check your version) · hill-climbing over a config field (e.g. a LangGraph runtime system prompt) · **for no-code and hosted agents:** export the prompt, score variants offline on your validation groups, paste the winner back · a person reviewing proposals | |
| Artifact | prompt / instructions · demos · skill file · memory · code · a node's prompt field in an export | |

_A person choosing the winner counts as learning only if they choose on a held-out score. Without one, the learning check scores it "not learning (you're the loop)"._

## Metric
`metric:` <existing: `path:line`> or a sketch: `metric(example, prediction) -> float` (0 to 1)
- If the only signal is a person: the rate of agreement with their recorded decisions. No decisions recorded yet? The first step is to start recording them; until then, write the metric as a rubric a person could score.
- If the output has several fields: score each field and say how they combine.
- If there are several objectives: name the weights, and keep each part as its own number.

---
Agent version: `signal-card` in brunnr (optional; see the README section "Agent versions").
