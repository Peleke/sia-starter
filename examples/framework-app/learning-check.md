# Learning check: airline customer-service agents (Agents SDK + ChatKit)

> **Worked example.** Target: [openai/openai-cs-agents-demo](https://github.com/openai/openai-cs-agents-demo) at commit `bd7bfca0f5ab` (MIT, © 2025 OpenAI). Citations are `path:line` at that commit. Kind of agent: framework app; yours may differ, so see [where-to-look](../../docs/where-to-look.md). Filled by an AI agent during a cold-setup test and checked by a person.

| agent | platform (see where-to-look) | repo / export @ commit | runs as stored? | you own it? |
|---|---|---|---|---|
| Triage agent, first handoff | OpenAI Agents SDK | openai/openai-cs-agents-demo @ `bd7bfca0f5ab` | yes (needs an OpenAI key) | no: a public demo, used here as a worked example |


One agent = the **Triage agent's first handoff**: the decision every conversation depends on (`python-backend/airline/agents.py:158-174`). The app has six specialist agents and two guardrails; the triage decision is the unit we'd score.

## Loop: (none found)

| question | yes / partial / no | evidence |
|---|---|---|
| **Q1** When it gets something wrong, what tells it? | no | Feedback in the chat UI is turned off (`ui/components/chatkit-panel.tsx:65`, `feedback: false`). The action handler does nothing (`python-backend/server.py:470-479`). Tracing is disabled (`python-backend/main.py:31`). Looked in: UI config, server handlers, guardrails, README. |
| **Q2** When that happens, what changes, and how much? | no | Prompts and routing are constants in code (`python-backend/airline/agents.py:158-174`). Conversation state is in process memory only (`python-backend/memory_store.py:18-23`). |
| **Q3** Is it measurably better over time? | no | No tests, evals or stored results in the repo. Looked in: repo root, `python-backend/`, `ui/`. |

**Outcome for this loop:** not learning.

**Headline:** not learning. The only thing that changes the prompts is a developer editing them.

## First fix
Turn Q3 into a number before changing anything: score first-handoff correctness on ~30 hand-written cases built from the three demo flows (`README.md:96-170`). The server already emits a structured handoff event to score against (`python-backend/server.py:247-257`).
