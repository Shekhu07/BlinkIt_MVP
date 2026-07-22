# Concept Spec — Trust-Concierge Agent (Part 4, future direction)

## Status: CONCEPT — not built, not on the critical path

This is a buildable prototype spec for an **alternative** Part 4 agent shape, kept as a
future-direction concept. It does **not** replace the shipped MVP (the Category Nudge Agent,
live on HuggingFace — see `mvp/` and `implementation-plan.md` Phase 5). Nothing here is
wired into the deployed Space. Use this as a "where this could go next" slide/spec, or as
the basis for a later build if time allows after the deck.

Grounded in the same locked research as the shipped MVP: `problem_statement.md` §2 (trust
root cause), §4 (Q15 confidence drivers). Same honest scope limit applies (see §7).

---

## 1. One-line definition

A **pull-based, conversational** agent: the user asks whether an unfamiliar category is
reliable on Blinkit, and the agent answers with category-specific trust evidence (refund
guarantee + quality/freshness signals), instead of the app pushing a one-shot nudge card.

Contrast with the shipped **Category Nudge Agent** (push, one-shot). Same root cause, opposite
interaction model.

| | Category Nudge Agent (shipped) | Trust-Concierge (this concept) |
|---|---|---|
| Trigger | App-initiated (push) | User-initiated (pull) |
| Interaction | Single generated nudge | Multi-turn Q&A |
| Reaches | Users who need a prompt | Users already curious but hesitant |
| Metric lever | Broader (proactive) | Narrower (only self-selecting askers) |

---

## 2. What it does (user flow)

1. User is hesitant about a category they've never bought (e.g. electronics, fresh meat).
2. User asks the agent, e.g. *"Is it safe to order electronics here?"*
3. Agent classifies the category + intent, matches to the relevant friction theme, and replies
   with: the applicable return/refund guarantee, the quality/freshness signals for that
   category, honest caveats where they exist, and a low-risk first-try suggestion.
4. User can follow up ("what if it arrives damaged?") — multi-turn, context retained.

---

## 3. Architecture — reuse vs. new

The matching + agent-reasoning layers are **reused wholesale** from the shipped MVP; only the
delivery layer and prompt change.

```
User question ──► Intent+Category classifier ──► Friction-Matching ──► Groq chat agent ──► Chat UI
   (new)              (new, small LLM step)        (REUSE                 (REUSE model,       (new:
                                                    friction_matching.py)  new system prompt)   gr.ChatInterface)
```

| Layer | Reuse or new | Notes |
|---|---|---|
| Friction themes data | **Reuse** | `mvp/data/friction_themes.json` unchanged |
| Friction-matching | **Reuse** | `mvp/friction_matching.py`; match on the category the user names instead of a stored profile |
| LLM / model | **Reuse** | Groq `llama-3.3-70b-versatile` |
| Intent+category classifier | **New** | 1 small LLM call (or keyword map) to extract {category, intent} from free-text |
| Conversation memory | **New** | Keep last N turns; pass as chat history |
| Delivery layer | **New** | `gr.ChatInterface` (Gradio) instead of the dropdown UI; or a FastAPI `/chat` endpoint |

Net new code is roughly: one classifier function, one chat-oriented system prompt, and a
`gr.ChatInterface` wrapper (~1 file, `app_concierge.py`). No changes to the shipped files.

---

## 4. Prompt spec (agent layer)

System prompt must enforce the same guardrails as the shipped agent, adapted for chat:

- **Only reference real Blinkit categories** — pass a hardcoded allowed-category list in
  context (per `edge-cases.md`: prevents hallucinated categories/features like a fake loyalty
  program). This risk is *larger* in free-form chat, so the constraint is stricter here.
- **Lead with the two ranked trust drivers** (refund guarantee + quality/freshness signal) when
  the matched theme is trust-driven; for low-intent/no-trust questions, answer honestly and do
  not manufacture a guarantee as if it addresses their real reason.
- **Never overclaim** — if Blinkit genuinely can't guarantee something for a category, say so.
  A concierge that oversells is worse than the nudge because it invites a trust violation.
- **Stay on task** — decline off-topic requests; this is a category-trust assistant, not a
  general chatbot.
- Return conversational prose (not JSON), but keep answers short and specific.

---

## 5. Interface

**Option 1 (recommended for a demo): Gradio `gr.ChatInterface`** in a new `app_concierge.py`.
Free HF Gradio SDK, same ZeroGPU no-op shim as the shipped app. Fastest path to a live link.

**Option 2: FastAPI `POST /chat`** ({session_id, message} → {reply}) added to `app_fastapi.py`,
with a minimal chat HTML widget. Use if you want an API surface as well.

---

## 6. Build effort estimate

Small — ~half a day, because 3 of 4 layers are reused:
1. `classify_question()` — extract category + intent (1 Groq call or keyword map). ~1–2 hrs.
2. Chat system prompt + `concierge_reply(history, message)`. ~1–2 hrs.
3. `gr.ChatInterface` wrapper + local smoke test. ~1 hr.
4. Deploy as a second Space (or a tab in the existing one). ~30 min.

---

## 7. Honest scope + trade-offs (must appear on any deck slide using this)

- **Strength**: reads as more "AI-native" (a genuine multi-turn agent) and serves the exact
  moment of doubt.
- **Weakness on the metric**: pull-based, so it only reaches users who already thought to ask
  — structurally misses the unmotivated part of the stuck segment that a proactive nudge can
  reach. Weaker %MAU lever than the shipped push agent.
- **Same ~50% ceiling**: only addresses the trust-driven half of stagnation (`problem_statement.md`
  §2); does nothing for the low-intent half, who wouldn't ask.
- **Higher hallucination surface**: free-form chat widens the risk in `edge-cases.md`; the
  category-allowlist constraint is mandatory, not optional.

**Recommendation**: keep as a "next step / vision" concept in the deck. The shipped Category
Nudge Agent is the stronger *product argument* for the growth metric because it reaches users
who aren't already motivated; the concierge is the stronger *demo* but a narrower lever.
