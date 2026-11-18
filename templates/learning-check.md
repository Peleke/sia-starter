# Learning check: <agent name>

Is the agent learning, or are you? Three questions, answered with evidence. For an agent you own. Where to find the evidence on your platform: [docs/where-to-look.md](../docs/where-to-look.md) in your copy of the kit.

**Step zero: write the agent's job in one sentence.** If its prompt doesn't say, write your assumption in the notes. Every answer below depends on it.

| agent | its job, in one sentence | platform (see where-to-look) | repo / export @ commit | would it run as stored? | did you run it? |
|---|---|---|---|---|---|
| | | | | yes / no (reasons below) | yes / no |

_Notes (reasons it wouldn't run, assumptions you made):_


**One agent** = one unit whose output you could score. **One loop** = one signal source feeding one artifact that changes (say, user corrections → a memory file). If the agent has several, copy the table once per loop. Things that only steer the next step inside one run (a tool loop, a retry, a self-check) get a one-line note, not a table.

**No loop at all?** Write "no loop found" as the outcome, and fill one table for the loop you'd want (mark it "proposed"). Its answers will be no; that's the honest start.

**One run** = one complete task. For a chat app, one conversation. Anything that resets when the run ends (retries, redrafts, conversation variables) is not a lasting update.

## Loop: <name the loop>

| question | yes / partial / no | evidence (`path:line [node-id]`; for "no", where you looked) |
|---|---|---|
| **Q1** When it gets something wrong, what tells it? | | |
| **Q2** When that happens, what changes, and how much? | | |
| **Q3** Is it measurably better over time? | | |

**Outcome for this loop:** <no loop found / not learning / learning, unmeasured / learning, measured> <add "(partial loop)" if Q1 or Q2 is partial>

## How to answer
| | yes | partial | no |
|---|---|---|---|
| **Q1** outside signal | A signal the model can't produce by reviewing itself reaches the agent without anyone carrying it: a test, CI, a tool error or exit code (raw result kept), a user, a label, a human click. It has to say whether the *output was right*; a format or execution failure alone doesn't count | A signal like that exists but a person has to carry it to the agent (e.g. a CI test whose failure only reaches a developer); or the only judge is a separate LLM that hasn't been checked against people | Only the model reviewing itself (a second call to the same model counts as reviewing itself), or nothing |
| **Q2** lasting update | The signal causes a change that survives across runs, is applied without a person, and is recorded in a unit you can diff (lines, directives, a score) | A change persists across runs but its size isn't recorded; or a result is computed once (e.g. by an optimizer) and then used for many later runs in the same process, but never saved; or a person has to apply it | Nothing outlasts one run. Retries, redrafts and checks inside a single task or conversation count as no, even when they change the next step. So do changes that are computed but never applied |
| **Q3** measured gain | A score on held-out examples (not the set the optimizer chose on), compared with a baseline, recorded more than once | A held-out set or a baseline exists, but they aren't run together | No held-out number. A single test case is not a held-out set. Evidence that lives outside the repo, unseen, is also no |

**Outcomes** (every combination lands in exactly one):
- **No loop found:** nothing feeds any artifact. Fill the proposed loop.
- **Not learning:** Q1 is no, or Q2 is no, **or a person both carries the signal and applies the change with no held-out score (Q3 no)**. That's you learning, not the agent.
- **Learning, unmeasured:** Q1 and Q2 are yes or partial; Q3 is no or partial; and it isn't the person-both case above.
- **Learning, measured:** Q1 and Q2 are yes or partial; Q3 is yes.
- Add **(partial loop)** when Q1 or Q2 is partial.

**Headline for the agent:** the best loop's outcome, naming the loop. Example: "learning, unmeasured (design-taste loop); other loops: not learning".

## Worked edge cases (from real agents we checked)
| case | Q1 | Q2 | Q3 | outcome |
|---|---|---|---|---|
| Agent writes "learnings" after reviewing its own session | no | yes | no | not learning |
| Agent edits its memory files from users' corrections in chat | yes | partial (no size record) | no | learning, unmeasured (partial loop) |
| User approves or rejects outputs; the choice is stored and reused | yes | partial | no | learning, unmeasured (partial loop) |
| People edit the prompts, and keep a change only if a pre-registered eval improves | yes | partial (a person applies it) | yes | learning, measured (partial loop) |
| The author edits the prompts after noticing failures; no eval | partial (a person carries it) | partial (a person applies it) | no | not learning (you're the loop) |
| A reflect or check node: the same model grades its own draft and retries within the run | no | no (resets each run) | no | not learning (note it; no table) |
| A daily CI test checks one question; a failure emails a developer, who may edit the prompt | partial | partial (a person applies it) | no (one test isn't a held-out set) | not learning (you're the loop) |
| A template or export nobody has ever changed, with no feedback path | — | — | — | no loop found |
| An optimizer improves the prompt from labeled examples, applied in the process, never saved; scored on its own selection set | yes | partial | no | learning, unmeasured (partial loop) |
| The optimizer's best configuration is printed and never applied | yes | no | no | not learning |
| A human approve/reject gate whose rejections are only logged | yes | no | no | not learning |
| Hand-written demos that a person updates | no | no | — | not learning |
| A separate LLM grades the output; never checked against people | partial | — | — | depends on Q2 |

**If the only thing that changes the prompt is you, you're the one learning, not the agent.**

## First fix
<the cheapest "no" to turn into a "partial" or "yes", and the evidence that would show it>

---
Agent version: `learning-check` in brunnr (optional; see the README section "Agent versions").
