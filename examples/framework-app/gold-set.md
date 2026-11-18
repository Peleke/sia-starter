# Gold set plan: airline customer-service agents (Triage, first handoff)

> **Worked example.** Target: [openai/openai-cs-agents-demo](https://github.com/openai/openai-cs-agents-demo) at commit `bd7bfca0f5ab` (MIT, © 2025 OpenAI). Citations are `path:line` at that commit. Kind of agent: framework app; yours may differ, so see [where-to-look](../../docs/where-to-look.md). Filled by an AI agent during a cold-setup test and checked by a person.

| agent | platform (see where-to-look) | repo / export @ commit | runs as stored? | you own it? |
|---|---|---|---|---|
| Triage agent, first handoff | OpenAI Agents SDK | openai/openai-cs-agents-demo @ `bd7bfca0f5ab` | yes (needs an OpenAI key) | no: a public demo, used here as a worked example |


**Metric it serves:** `first_handoff_correct` scores the first handoff target (one field of the event stream).

**Group key:** the scenario a message comes from (one of the demo flows, or one hand-written scenario). Variants of the same scenario stay in one group.

## Example schema
| field | input or label | where it comes from |
|---|---|---|
| `message` | input | demo flows (`README.md:96-170`) and hand-written cases |
| `context` (flight, confirmation) | input | the demo's mock trip data, via `get_trip_details` |
| `expected_first_agent` | label | a person, using the routing rules in the Triage instructions (`python-backend/airline/agents.py:162-170`) |
| `scenario` | group key | assigned when the case is written |

## Sources
- [x] real inputs: none (it's a demo with no users). With users, traced conversations would go here (tracing is off now: `python-backend/main.py:31`)
- [x] hand-written cases: the three demo flows plus edge cases (ambiguous requests, two intents in one message, off-topic): target 12 scenarios
- [x] model-made variants of checked cases: 3–5 rewordings per scenario, each checked by a person

## Labeling
- [x] a model drafts `expected_first_agent`; a person checks every one
- [x] the labeling guide: the routing rules the Triage instructions already state

## Split (by scenario)
- [x] train: 2 scenarios (demos, if the search uses them)
- [x] validation: 6 scenarios (where the optimizer picks a winner)
- [x] test: 4 scenarios, touched once

**Size:** 12 groups. The notebook on a few baseline reps will show how wide the interval is at 4 test groups; expect "inconclusive" for small gains, and add scenarios before claiming one.
