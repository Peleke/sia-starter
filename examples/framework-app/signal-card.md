# Signal card: airline customer-service agents (Triage, first handoff)

> **Worked example.** Target: [openai/openai-cs-agents-demo](https://github.com/openai/openai-cs-agents-demo) at commit `bd7bfca0f5ab` (MIT, © 2025 OpenAI). Citations are `path:line` at that commit. Kind of agent: framework app; yours may differ, so see [where-to-look](../../docs/where-to-look.md). Filled by an AI agent during a cold-setup test and checked by a person.

| agent | platform (see where-to-look) | repo / export @ commit | runs as stored? | you own it? |
|---|---|---|---|---|
| Triage agent, first handoff | OpenAI Agents SDK | openai/openai-cs-agents-demo @ `bd7bfca0f5ab` | yes (needs an OpenAI key) | no: a public demo, used here as a worked example |


**My agent gets better when the share of requests routed to the right specialist on the first handoff goes up.**

## Candidate signals
| candidate | type | where it comes from | how often | cost | outside the model? |
|---|---|---|---|---|---|
| First handoff matches the labeled specialist | score | handoff events, `python-backend/server.py:247-257`, vs a label | per conversation | ~1 person-minute per label | yes (labels) |
| The right tool called with the right arguments | score | tool-call events, `python-backend/server.py:289-300`, vs the expected call in the demo flows (`README.md:148-170`) | per conversation | a few person-minutes per flow | yes |
| User thumbs up / down | preference | ChatKit feedback, currently off (`ui/components/chatkit-panel.tsx:65`); needs a handler (`python-backend/server.py:470-479`) and storage | a minority of conversations | free to collect, noisy | yes |
| On-topic messages wrongly refused by a guardrail | score | guardrail results, `python-backend/server.py:397-400`, vs labeled on-topic messages | per message | ~1 person-minute per label | yes |

**Pick:** first-handoff correctness. It's the most frequent, cheapest outside signal, and it needs no LLM judge.

## Slots
| slot | pick for now |
|---|---|
| Signal | first-handoff correctness on a labeled set |
| Search | an instruction optimizer (e.g. GEPA) run offline over the Triage instructions, scored on the validation groups; a person reviews the winner before it ships |
| Artifact | the Triage agent's instructions (`python-backend/airline/agents.py:162-170`) |

## Metric
```python
def first_handoff_correct(example, prediction) -> float:
    # prediction: the AgentEvent list the server builds (python-backend/server.py:247-257 for handoffs)
    handoffs = [e for e in prediction if e["type"] == "handoff"]
    if not handoffs:
        return float(example["expected_first_agent"] == "Triage Agent")
    return float(handoffs[0]["metadata"]["target_agent"] == example["expected_first_agent"])
```
