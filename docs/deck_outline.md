# Deck Outline — Blinkit Category Adoption (Phase 6)

> **⚠️ Superseded (2026-07-29).** This early planning draft (N=25 survey figures, an 11th
> appendix slide) was replaced by the Design Labs import. The current, authoritative deck is
> `deck/design/Blinkit Category Nudge Case Study.dc.html` (10 slides, no appendix, N=31) — see
> `deck/design/CLAUDE.md` for its graded hard rules. Kept here for history only; don't build from it.

## Purpose & rules baked in
- **10 slides max including the title slide.** Titles are **key messages**, not labels.
- Structured around the **cross-part traceability thread** (`architecture.md` §8): every slide
  answers "which part is this, and what did the previous part tell us that led here?"
- One thread followed end to end: **quality-distrust → category avoidance → trust-nudge**.
- Satisfies the mandatory "**one place research confirmed AND one place it challenged** the AI
  findings" requirement (Slide 5).
- No fellow name anywhere. Both live links embedded (Slides 6, 8, 10).
- The Part 1 **workflow 1-slider** is an embedded appendix explainer (see note at end re: slide count).

Live links to embed:
- Discovery workflow: https://huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine
- MVP (Category Nudge Agent): https://huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent

---

## Slide 1 — Title
**Key message (title):** *"Why do Blinkit's most loyal users never widen their basket?"*
- Subtitle: turning a growth goal — *increase the % of MAU who buy from ≥1 new category each
  month* — into a discovery → research → problem → MVP story.
- Visual: the 4-part thread as a single left-to-right arrow (Discovery → Research → Problem → MVP).
- No name. Project/fellowship framing only.

## Slide 2 — The goal & the approach
**Title:** *"A growth metric, answered with evidence — not assumptions."*
- The Growth Team goal stated once, plainly.
- The 4-part method in one line each, emphasising each part **consumes the previous part's output**.
- Sets up the thread the rest of the deck follows.
- *Traceability anchor: this is the map for slides 3–8.*

## Slide 3 — Part 1: the discovery engine & its headline finding
**Title:** *"An AI engine read 15,820 reviews and found one dominant barrier: broken trust in product quality."*
- Funnel: **15,820 raw → 4,740 filtered → 1,094 gate-passing extractions.**
- The **Two-Step Gated Schema** in one line (gate on category-adoption behavior, then extract) —
  why it beats open-ended theming.
- Headline: **"Poor Quality & Unreliable Products" = 770 / 1,094 evidence (~70%)**, the top theme
  by a wide margin (next themes 10% / 7%).
- Embed/QR the **live discovery workflow link** (evaluator can test the extractor themselves).
- *From Part 1.*

## Slide 4 — Part 1: is the finding trustworthy?
**Title:** *"The finding holds up — validated by an LLM judge and aligned with Eternal's own growth narrative."*
- **LLM-judge validation: 16/20 confirmed, 4 unclear, 0 contradicted** (held-out theme-relevant sample).
- **Company corroboration:** Eternal's Q4 FY26 earnings call names **non-grocery assortment
  expansion** as a core growth dependency — the widening this project is trying to unlock.
- **Honest gap:** the call doesn't directly address quality/refund friction. State it.
- Takeaway: the AI theme is independently corroborated, not just model output.
- *(The "1.8% of NOV" figure is omitted — unverified, see the decision note in `deck_spec.md` Slide 4.)*
- *Still Part 1 → sets up why we took it to real users.*

## Slide 5 — Part 2: user research CONFIRMS and CHALLENGES the AI *(mandatory slide)*
**Title:** *"25 real users: quality fear is real — but it's only half the story."*
- **Confirmed:** quality incidents generalize beyond the affected category — quote:
  *"I only order the essential items now if anything urgent."*
- **Challenged (3 honest counter-findings):**
  1. One user churned to a **competitor (Zepto)** instead of just avoiding a category.
  2. **7 of 15** incident-havers reported **no behavior change** (resolution neutralizes it).
  3. **8 of 18** "stuck" users had **no incident at all** — low intent, not distrust.
- This is the confirm-AND-contradict requirement, made explicit.
- *From Part 2, built directly on the Part 1 theme.*

## Slide 6 — Part 3: the problem statement
**Title:** *"Loyal, high-frequency buyers default to what's proven safe — because one bad experience removes the benefit of the doubt."*
- **Segment:** repeat buyers (58% of respondents "stick to the same categories"), heavy/daily, mainstream.
- **Root cause:** an unresolved quality failure generalizes into category avoidance — for the
  **~50%** of the segment that's trust-driven (honest scoping, not overclaimed).
- **Workarounds users already use:** "essentials-only" retreat; platform-switching.
- *From Part 3 = Part 1 theme + Part 2 nuance combined.*

## Slide 7 — Part 3: why solving it matters (user + business)
**Title:** *"Users already told us the fix — and it sits directly on Eternal's stated growth path."*
- **User value (Q15, what users said would change their behavior):**
  refund/return guarantee **(13/31)** + visible quality/freshness signal **(10/31)** — the top two.
- **Business case:** Eternal's Q4 FY26 call ties growth to **non-grocery assortment expansion**,
  which only pays off if users actually try those categories — removing the trust barrier is
  upstream of the company's own stated growth plan.
- *Still Part 3 → defines exactly what the MVP must do.*

## Slide 8 — Part 4: the MVP (Category Nudge Agent)
**Title:** *"An AI agent that earns the first try — leading with a guarantee, not a generic 'try something new'."*
- What it does: matches a user's behavior to the friction theme → generates a **per-user, reasoned**
  nudge leading with the **refund guarantee + quality/freshness signal** (the two Q15 drivers).
- Why AI-native: reasoning is generated per user/theme, not a fixed template.
- Honest scope: targets the trust-driven ~50%, not the low-intent half.
- Embed/QR the **live MVP link** + one real screenshot of a generated nudge.
- *From Part 4 = the direct answer to Part 3.*

## Slide 9 — The thread, and the honesty
**Title:** *"One line runs through all four parts — and we're clear about what it doesn't solve."*
- The full traceability chain on one slide:
  *Theme (770/70%) → confirmed + challenged by users → problem (trust-driven avoidance) → nudge (guarantee-led).*
- The honest boundary: fixes the trust-driven half; the low-intent half needs a different lever
  (a candidate "next step" — the Trust-Concierge / basket-gap directions).
- *Synthesizes Parts 1–4.*

## Slide 10 — Impact & what's live
**Title:** *"A testable engine and a live agent — the whole thread is reachable, not just described."*
- Both **live links** (workflow + MVP), clearly labelled and public.
- The metric it moves and how you'd measure it (new-category trial rate in the nudged cohort).
- Next steps: Option 4 (pre-acceptance inspection), churn-save, scale beyond synthetic data.

---

## Embedded appendix — Part 1 Workflow 1-slider
**Title:** *"How the discovery engine works, end to end."*
- Pipeline diagram: Ingest (Play Store / Maps / App Store / MouthShut / CC) → TF-IDF prefilter →
  **Two-Step Gated LLM extraction (Groq)** → deterministic theme clustering → LLM-judge validation →
  concall corroboration.
- One callout: evidence counts are **DB-backed row counts, never LLM-estimated**.
- Per the brief this is a separate 1-slider embedded inside the deck.

### ⚠️ Slide-count decision needed
The brief says **10 slides max including title**, and also asks for a **1-slider workflow** embedded
inside the deck. Two clean readings:
- **(a)** Treat the workflow 1-slider as an **appendix** after slide 10 (doesn't count toward the 10) — most common interpretation.
- **(b)** Fold the workflow diagram into **Slide 3** and drop the standalone, keeping a hard 10.
Recommend **(a)**; confirm your preference before building.
