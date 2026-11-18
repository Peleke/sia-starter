# Where to look, by platform

The templates ask for evidence. This page says where each platform keeps it, **for an agent you own**: you can open its settings, logs and history. Each row says what it's based on. Your setup may differ.

**Your platform isn't listed?** Use the closest row, mark your answers "best-effort", and expect gaps. If you want a proper read on an agent like yours, get in touch (peleke.me · LinkedIn).

## Rules for every platform
1. **Export vs. instance.** Exports and repos hold the agent's design: prompts, nodes, code. Feedback, logs and run history usually live in the running platform. Check both. If you can only see the design, say so in your answers.
2. **State outside the repo.** Write `mechanism: yes (path:line); runtime evidence: <where you looked>`. "Is it measurably better" needs a number you have actually seen.
3. **It can't run as stored** (missing wiring, placeholder nodes, missing keys). Say so, and assess the design.
4. **Evidence format, one rule everywhere:** `path:line [node-id]`.
   - Drop the `[node-id]` for code and text files.
   - For JSON or YAML exports, add the node's id, because titles repeat and decoding moves lines.
   - Use `screen › setting` for anything you see only in a UI.
   - Define a short alias for a long path once.
   - Cite, don't quote.
5. **Export vs. what's live.** Hosted platforms keep versions; the export you have may not be the one running (n8n reports whether the active version matches the draft). Say which one you assessed.

## Coding harnesses
| platform | one agent = | signal shows up in | what changes | history | grep hints |
|---|---|---|---|---|---|
| **Claude Code.** *Based on: a public Claude Code harness; this kit's authors' own setup* | one skill or command, or one loop if several skills share a preamble | PR review outcomes, CI and test runs, tool errors, hooks that record verdicts, you approving or rejecting | `CLAUDE.md`, `.claude/skills/*/SKILL.md`, hooks in `settings.json`, memory or learnings files | session transcripts under `~/.claude/projects/`; state some setups keep under `~/.<tool>/` | `learn\|memory\|feedback\|eval\|preference\|hook` |
| **Codex CLI.** *Based on: codex-cli 0.167 help text* | as above | as above | `AGENTS.md`, skills | sessions persist under `CODEX_HOME` unless run with `--ephemeral` | as above |

## Personal gateway agents
| platform | one agent = | signal shows up in | what changes | history | grep hints |
|---|---|---|---|---|---|
| **OpenClaw.** *Based on: OpenClaw workspace templates* | the workspace, or each role in a team | your corrections in chat, reactions, approvals | `AGENTS.md`, `USER.md`, `MEMORY.md`, `SOUL.md`, daily notes | daily notes; automation state in the gateway's database; channel logs | `memory\|lesson\|mistake\|prefer\|USER.md\|MEMORY.md` |

## Framework apps
| platform | one agent = | signal shows up in | what changes | history | grep hints |
|---|---|---|---|---|---|
| **OpenAI Agents SDK.** *Based on: the Agents SDK customer-service demo* | one agent, or the one decision you'd score (e.g. the first handoff) | feedback widgets, action handlers, guardrail results, escalations | agent instructions and handoffs in code | traces (check whether tracing is disabled in code or env); the app's own store | `tracing\|feedback\|action\|guardrail\|Store\|handoff` |
| **LangGraph.** *Based on: a LangGraph research agent; LangGraph docs (persistence, observability)* | one graph, or the node you'd score | LangSmith traces and feedback; scheduled CI tests (often one or two questions: a signal for a developer, not a held-out set) | prompts (often a config field or `prompts.py`), graph wiring | **LangSmith** when `LANGSMITH_TRACING=true`; a **checkpointer** keeps state within a thread; a **Store** keeps data across threads. No Store usually means no memory across runs. A deployment server may add a checkpointer the code doesn't show; that's still per-thread, not learning | `LANGSMITH\|checkpointer\|Store\|reflect\|prompts\|@unit` |

## Prompt programs
| platform | one agent = | signal shows up in | what changes | history | grep hints |
|---|---|---|---|---|---|
| **DSPy.** *Based on: a DSPy research pipeline* | one module; in a pipeline, the module you'd score | the metric function, evaluation scripts | instructions, demos, saved program state | saved programs; eval outputs (sometimes on another branch) | `teleprompt\|compile\|Evaluate\|metric\|\.save\(\|\.load\(\|Example` |
| **Ax.** *Based on: Ax optimizer examples* | one program (`ax()` / `agent()`) | the metric function | instructions, demos, the optimized program | saved optimizer results, if they're saved at all | `metric\|AxGEPA\|AxBootstrapFewShot\|validationExamples\|applyOptimization\|setExamples` |

## Hosted and no-code
| platform | one agent = | signal shows up in | what changes | history | grep hints (in the export) |
|---|---|---|---|---|---|
| **n8n.** *Based on: two n8n workflow exports; n8n docs (workflow settings)* | one workflow, or the step you'd score | approval or review nodes; buttons or ratings you added; error workflows; **the sheet or table it writes to**, if a person corrects the output there | prompts in node parameters (e.g. an agent node's system message) | **Executions**, which are kept only if the workflow's settings save them ("Save successful/failed production executions"); tables the workflow writes | `approve\|reject\|review\|feedback\|systemMessage\|prompt\|messages\|noOp`. The older OpenAI node keeps its prompt under `prompt.messages`. **Would it run?** `uv run python scripts/check_n8n_export.py <file>.json` checks that every connection names a real node, finds unconnected nodes and placeholders, and lists needed credentials |
| **Dify chatflow / chatbot / agent.** *Based on: a Dify chatflow DSL export; Dify docs (feedback API, export)* | one app; one conversation = one run | end-user **like / dislike** with an optional comment (Service API `/app/feedbacks`); **annotations** | node prompts, knowledge settings, `features:` | **logs and annotations are not in the export** (Dify docs: "What the export leaves behind"); look in the app's Logs and Annotations | `features\|conversation_variables\|knowledge-retrieval\|annotation\|prompt_template`. Prompts in non-Latin scripts are often escaped: `uv run --with pyyaml python scripts/decode_dify.py <file>.yml` |
| **Dify workflow** (`mode: workflow` at the top of the export). *Based on: a Dify workflow DSL export; Dify docs* | one app; one execution = one run | Dify's API docs list feedback for chatflow, chatbot, agent and text-generator apps, **not workflow apps**: plan on adding your own signal (e.g. a review step or a table the output lands in) | node prompts, classifier instructions, knowledge settings | run logs live in the console, not in the export | same as above; decode first |

**Not covered yet:** CrewAI, Mastra, Google ADK, Semantic Kernel, Cursor, custom GPTs and Assistants, Zapier, Copilot Studio. Use the closest row and mark your answers "best-effort".
