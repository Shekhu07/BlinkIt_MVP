# Concept — Let the user choose the category (multi-option nudge)

> **Status: ON RECORD ONLY.** Raised 2026-07-30. Nothing here is built or wired into the
> deployed Space. The shipped MVP still sends **one** agent-selected, guarantee-led nudge per
> user (`mvp/agent.py` rule 3, "prefer the highest-ranked candidate").
>
> Two variants are specified below. **Variant A (operator-side override) is safe to build now.**
> **Variant B (shopper-facing category picker) must not be dropped into the trust nudge** — it
> changes which segment the MVP addresses and contradicts a rejection already argued on deck
> slide 7. See §4 for the cascade it would require.

## 1. The idea, as raised

> "In the nudge agent operator console, can't we give options to the user to buy products from a
> category he hasn't bought from, instead of just nudging him with a category of our own?"

## 2. The data already exists — this is a UI question, not a modelling one

`friction_matching.rank_suggestable_categories(profile, top_n=4)` already returns the top four
categories the user has **not** bought from: it scores basket adjacency and then filters
`if _norm(c) not in existing`, so "a category he hasn't bought from" is exactly what the pool
contains. The operator console already renders that pool in the **"Also considered — ranked"**
block with its integer adjacency weights.

(In the deployed clone `~/blinkit-category-nudge-agent` there is also a
`primary_suggested_category()` helper returning `pool[0]`, used to keep the push queue and the
checkout cart-filler pointed at the same category. It does **not** exist in this repo's `mvp/` —
see the divergence warning in `CLAUDE.md`. Variant A should reuse it in the clone rather than
add a second ranker.)

So nothing new has to be computed. The only open question is **who picks** — the ranker, the
operator, or the shopper — and that question is a product/scope decision, not an engineering one.

## 3. Variant A — operator-selectable alternatives (safe, additive)

Make the entries in "Also considered — ranked" clickable in the console: clicking `baby care`
regenerates the same trust-led nudge for that category instead of the ranker's `pool[0]`.

- **Shopper-facing behaviour is unchanged** — still one guarantee-led nudge for one category, so
  the Part 3 → Part 4 thread and every deck claim stay intact.
- **Strengthens the auditability story** rather than diluting it: the deterministic ranker
  proposes, a human can override, and an evaluator can watch the pick change live. That is a
  better demo of "the model never chooses the category" than a static list.
- **Contained**: `on_generate` takes an optional category override; the alternatives become
  buttons. No prompt change, no data change, no deck change.
- Keep the override **operator-only and labelled**, so it can't be mistaken for shopper choice.

## 4. Variant B — shopper-facing category picker (do NOT ship into the trust nudge)

Letting the shopper choose from several unpurchased categories is a *different intervention for a
different segment*, and the project has already argued against it in the trust context:

- **Deck slide 7 rejects the adjacent option outright.** "Better merchandising and category
  placement" → *"Awareness — ranked 3rd at 7% of evidence"* → rejected because *"these buyers
  already see the categories."* A picker is the same class of lever: it addresses choice and
  awareness, not trust.
- **Slide 2 states the finding it contradicts:** *"This is a trust problem, not an awareness
  problem."* These are daily/near-daily buyers who have seen the other categories for months.
- **No survey support.** Q15 (N=31, pick up to 2) ranked refund guarantee **13**, visible
  quality/freshness signal **10**, inspect-before-accepting **7**, item reviews **5**, intro
  offers **5**. Nothing in the instrument asked for, or surfaced, a want for more options.
- **It weakens the strongest thing about the MVP** — that it declines to overclaim. The single
  guarantee-led nudge is defensible precisely because it is scoped to the trust-driven share;
  a picker blurs the boundary the deck spends slide 9 and slide 10 drawing.

**Where Variant B genuinely belongs:** it is essentially **documented next step #2** —
*"A relevance-led nudge for the low-intent half. 8 of 18 stuck users had no bad experience at
all. A trust message is the wrong instrument for them; the open question is whether a cart-level
prompt moves them at all."* For low-intent users, choice/relevance **is** the right lever. Build
it as a **separate mechanic for that segment**, measured separately — not as a modification of
the trust nudge.

### Cascade required if Variant B were ever built into the shipped MVP
Not a UI-only change. All of the following would have to move together, or the artefacts
contradict each other:
1. `deck/design/Blinkit Category Nudge Case Study.dc.html` — slide 7's options table (the
   merchandising row's rejection no longer holds), slide 8's mechanic description, slide 10's
   next-steps list (item 2 would no longer be "next").
2. `docs/problem_statement.md` §6 — the scope statement that limits the MVP to the
   quality/trust-driven ~50%.
3. `mvp/agent.py` — system prompt rule 3 (prefer the highest-ranked candidate) and rule 4
   (never overclaim to low-intent users), plus the out-of-primary-scope banner logic.
4. `mvp/README.md` substitutions table, and `deck/NL Blinkit Category Adoption.pdf` +
   `NL_Blinkit_CategoryAdoption.pptx` re-export.
5. Redeploy both Spaces and re-verify.

At the time of writing the submission deadline is **4 Aug 2026, 3:59 PM IST** and the deck is
already built and verified, so this cascade is the reason Variant B is on record rather than in
progress.

## 5. If Variant B is built later, measure it separately

It targets the low-intent sub-segment, so folding its results into the trust cohort would read as
a failure of the wrong thing (the same warning as `deck` slide 10's honest-scope-limit card).
Report the two sub-segments separately: trial rate for trust-blocked users under the guarantee-led
nudge, versus trial rate for no-incident users under the choice-led prompt.

## 6. Related

- `docs/concept_trust_concierge_agent.md` — the pull/conversational variant of the same root
  cause, also on record only.
- `docs/problem_statement.md` §4 (Q15 drivers), §6 (scope limit).
- `docs/mvp_qa_log.md` — the running Part 4 decision log.
