# Part 4 MVP — Q&A Log (Category Nudge Agent / % MAU new-category-adoption metric)

## Status
Running log of questions and answers discussed while scoping the Part 4 MVP, kept separate from the locked docs (`architecture.md`, `problem_statement.md`, `implementation-plan.md`) so the reasoning trail doesn't clutter those. Started 2026-07-22.

---

## Q: What are the plans for the AI-Native MVP Build?

The MVP is the **Category Nudge Agent** (architecture.md §6): given a user's order history, it matches them to a validated Part 1/3 friction theme, then has an LLM generate a per-user reasoned nudge that counters that specific friction — not a static template.

Component architecture:
```
Synthetic/mock user order data --> Friction-Matching Layer --> Groq Agent --> API endpoint / lightweight UI
```

Build sequence (Days 14–19 of `implementation-plan.md` Phase 5):
1. Day 14–15 — synthetic user profile dataset (5–10 profiles, clearly labeled synthetic)
2. Day 15–16 — friction-matching layer (profile → closest Part 1 theme)
3. Day 16–17 — Groq agent layer (`llama-3.3-70b-versatile`, generates nudge + reasoning)
4. Day 17–18 — delivery layer (FastAPI endpoint + minimal front end)
5. Day 18–19 — deploy to production (Render/Railway/HuggingFace Spaces), end-to-end live test
6. Milestone: MVP live at a stable URL by end of Day 19

Scope guardrail (`problem_statement.md` §6): lead with the two highest-ranked confidence drivers, and stay honest that this only fixes the quality/trust-driven half of stagnation, not the low-intent half.

---

## Q: What were the two options for our AI-Native MVP?

Only one comparison is documented, in `architecture.md` §6.3 ("Why this MVP choice over alternatives"):
1. **A pure "workflow" (no agentic reasoning)** — a static, rules-based recommendation widget. Satisfies the letter of the deliverable but under-delivers on "AI-native" since there's no per-user reasoning.
2. **The Category Nudge Agent** (chosen) — reasons per-user about *why* a nudge is relevant, generating nudge copy + reasoning dynamically per matched friction theme rather than from a fixed lookup table.

Rationale for picking option 2: the brief explicitly allows "an AI agent" as an MVP form, and it's the only option that closes the full Part 1→2→3→4 traceability thread.

---

## Q: List all the possible ways to build this MVP, per `problem_statement.md` and `implementation-plan.md`.

Neither doc actually lists build alternatives — both commit to one design (Category Nudge Agent). But the raw material for multiple nudge-mechanic variants exists in `problem_statement.md` §3–§4:

**Based on ranked confidence drivers (§4, Q15 survey):**
1. Return/refund-guarantee nudge — top driver, 11/25 picks
2. Quality/freshness-verification nudge — second driver, 9/25 picks
3. Social-proof nudge (item reviews/ratings) — tied third, 5/25 picks
4. Pre-acceptance inspection nudge (inspect before accepting delivery) — tied third, 5/25 picks

**Based on workaround patterns (§3):**
- Counter the "essentials-only retreat" (users who narrowed their basket but stayed on Blinkit)
- Counter platform-churn (users shifting to a competitor) — flagged in §3 as more expensive but out of scope for a category-adoption MVP

Guardrail that applies to all options: `implementation-plan.md` §5 requires a **single nudge mechanic**, not several, to avoid MVP scope creep. `problem_statement.md` §6 requires staying honest that the fix addresses only the ~50% of stagnation that's quality/trust-driven.

---

## Q: Can we go with Option 1+2, and put Option 4 as a backup for later?

Yes — this matches §6's explicit instruction to lead with the two highest-ranked drivers, and stays within the single-nudge-mechanic guardrail (1+2 are combined into one nudge, not two separate mechanics).

**Decision recorded 2026-07-22** in both `problem_statement.md` §6 and `implementation-plan.md` Phase 5:
- Built now: refund/return guarantee + quality/freshness-verification signal, combined into one nudge.
- Deferred backlog item: pre-acceptance-inspection option (Q15 tied-third driver) — revisit only if time remains after the Day 19 milestone is hit.

---

## Q: How does nudging on the refund/return guarantee and quality/freshness signal help increase % MAU who purchase from at least one new category every month?

The causal chain, grounded in `problem_statement.md`:

1. **The bottleneck is trust, not awareness.** The target segment (56% of survey respondents, §2) already buys heavily and habitually — they're not category-stagnant from lack of exposure. §4: "only 8 of 14 stuck respondents cite an actual bad experience — the rest simply haven't been given a reason to trust an unfamiliar category yet." The blocker is a risk calculation at the point of trying something new, not a discovery problem.

2. **The two chosen drivers directly neutralize that specific risk.** Q15 shows users themselves named these as what would change their behavior (11/25 and 9/25 picks — the two biggest levers). A guarantee + a verified quality/freshness signal removes the exact downside (getting burned again, no easy recourse) keeping users locked into "what's already proven safe" (§2's own framing).

3. **Per-user, per-category targeting makes it a repeatable trigger**, not ambient messaging. A blanket homepage banner doesn't move the metric because it's generic and ignored; the agent generates the reassurance specifically for the nudged category and the matched friction theme, firing at the actual decision point — which is what a *monthly, repeatable* new-category-purchase metric requires.

4. **Honest scope limit** (§6, reconfirmed here): this only unlocks the ~50% of the stuck segment whose stagnation is quality/trust-driven. The other half (§2: 6/14 stuck respondents had no incident at all — genuinely low intent) won't move on this nudge alone. The MVP is a targeted fix for an evidence-backed half of the shortfall, not a claim to fix the whole metric.

Net path: **remove the named risk → user tries a new category for the first time → repeats monthly if the experience holds → % MAU with ≥1 new category rises**, bounded to the trust-driven half of the stagnant population.

---

## Q: List all the tech-stack options suggested for building the AI-native agent.

From `architecture.md` §6.2 and §7, layer by layer — options suggested vs. what was actually built:

| Layer | Options suggested | As built |
|---|---|---|
| Data layer (synthetic profiles) | Postgres OR JSON | JSON (`mvp/data/*.json`) — no DB dependency, runs on the Space |
| Friction-matching layer | Rules + theme lookup (deterministic, no LLM) | Deterministic Python rules (`friction_matching.py`) |
| Agent layer (LLM) | Groq `llama-3.3-70b-versatile` (switched from Gemini 1.5 Flash — deprecated + 20-req/day cap) | Groq `llama-3.3-70b-versatile` |
| Delivery / API layer | FastAPI endpoint + front end (Streamlit OR lightweight HTML) | Both: FastAPI+HTML (`app_fastapi.py`) AND Gradio UI (`app.py`, added as HF's free entrypoint) |
| Deployment / hosting | Render / Railway / HuggingFace Spaces (reuse ArthaAI pattern) | HuggingFace Spaces (Gradio SDK, ZeroGPU) |
| Orchestration (optional) | Celery + Redis; n8n for cadence | Not used — nudges generate on-demand |

As-built substitutions from plan: JSON over Postgres (zero DB dependency on the Space); Gradio added (not in original Streamlit/HTML list) because HF's Gradio SDK was the free path once Docker was paywalled; Celery/Redis + n8n skipped as overkill for a single on-demand nudge.

---

## Q: List all the AI-agent prototype concepts that could help users (Part 4).

No pre-existing list was found in the docs — only the shipped Category Nudge Agent and its rejected non-agentic alternative (`architecture.md` §6.3). The following concepts are supportable from `problem_statement.md`; A is built, B–E are unbuilt directions:

| # | Agent concept | What it does for the user | Grounded in |
|---|---|---|---|
| A | **Category Nudge Agent** *(built + deployed)* | Reasons per-user why a specific new category is safe to try, leading with refund + quality signals | §4 Q15 drivers |
| B | **Trust-Concierge Agent** | Conversational pull: user asks "is X category reliable here?" → agent answers with guarantee + freshness evidence for that category | §2 trust bottleneck |
| C | **Post-Incident Recovery Agent** | Detects a bad-experience signal, proactively rebuilds confidence (apology + guarantee + safe re-try) instead of letting the user retreat to essentials | §3 "essentials-only retreat" |
| D | **Churn-Save Agent** | Targets users drifting to a competitor; targeted win-back tied to the friction they hit | §3 platform-switching |
| E | **Basket-Gap Agent** | Analyzes a habitual basket, spots the untried adjacent category, pitches it with a relevance hook (helps the low-intent half) | §2 low-intent segment |

---

## Q: Spec the Trust-Concierge Agent (concept B) as a buildable prototype, kept as a concept.

Full buildable spec written to `docs/concept_trust_concierge_agent.md`, stamped **CONCEPT — not built, not on the critical path** (does not replace the shipped Category Nudge Agent; not wired into the deployed Space). Key points:
- **Pull-based, conversational** (user asks about a category's reliability) vs. the shipped agent's push/one-shot nudge. Same root cause, opposite interaction model.
- **Reuses 3 of 4 layers**: friction themes JSON, `friction_matching.py`, and Groq `llama-3.3-70b-versatile` unchanged. New: a small intent+category classifier, chat memory, and a `gr.ChatInterface` delivery layer (new `app_concierge.py`, shipped files untouched).
- **Prompt guardrails** carried over + tightened (hardcoded category allowlist to block hallucinated categories/features per `edge-cases.md`; lead with the two trust drivers; never overclaim; stay on task).
- **Effort**: ~half a day (3 of 4 layers reused).
- **Honest trade-off**: stronger *demo* / more "AI-native", but a **weaker %MAU lever** — pull-based, so it only reaches users who already thought to ask, structurally missing the unmotivated part of the stuck segment. Same ~50% trust-driven scope ceiling.
- **Recommendation**: keep as a "next step / vision" deck slide; the Category Nudge Agent stays the core MVP.

---

## Q: Which nudge-mechanic options remain open?

Of the four Q15-driver nudge mechanics: **Option 1 (refund guarantee) + Option 2 (quality/freshness)** are combined and shipped live. **Option 3 (social-proof / item reviews)** and the two §3 targeting variants (essentials-retreat, platform-churn) are unpursued. **Option 4 (pre-acceptance inspection nudge, Q15 tied-third, 5/25 picks)** is the deliberately-deferred backlog item the user has said they still want to try — the next Phase 5 experiment. See memory `project_phase5_mvp.md`.
