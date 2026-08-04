# Design Labs prompt — slide 10: full content rebuild

Target slide: **slide 10** (last slide). This replaces the current five-card body
content with a smaller, better-weighted structure: one hero metric, two supporting
ideas, and one closing line — instead of five same-weight information cards. Keep the
header and eyebrow; everything below them is a rebuild.

## What stays exactly as-is
- Eyebrow: "MEASUREMENT · PROPOSED, NOT YET MEASURED"
- Header: "Adoption is the metric; the guardrails are the veto."
- The yellow "Plan only" banner (top right) — still accurate, still needed.

## What's removed
- The Measurement Ladder table (3-tier table) — replaced by the hero metric alone.
- The "SYNTHETIC DRY-RUN" pipeline-verification line — this is a QA detail, not
  evaluator-relevant content, and it's what caused the earlier self-contradiction bug.
  Move it to speaker notes if you want it preserved at all; do not keep it on-slide.
- The 3-card "What we'd build next" grid — replaced by one line.
- The 4-guardrail flat list — replaced by 3 guardrails, reframed as risks each one catches.

## New body structure (4 blocks)

**1. Hero metric — largest visual weight on the slide**
"% of monthly active customers who purchase from at least one new category that month"
— sub-line: "Measured against the nudged segment's own prior month, not a headline
average." (Unchanged text, just needs to visually dominate — biggest type, most
prominent card, everything else reads as supporting it.)

**2. Guardrails, reframed as "how this could fool us" — 3, not 4**
- A nudge into a genuinely bad category → return/refund rate and complaint rate in
  nudged categories must not rise.
- A nudge that cannibalizes habitual reorder → reorder rate must not fall; opt-outs
  capped per user.
- Copy that invents trust it hasn't earned → sampled nudges audited for invented
  statistics; any hit is a release blocker.
(Same substance as the current guardrails card, cut from four to three and each framed
as the specific risk it catches rather than a flat checklist item.)

**3. One honest limit — a single sharp line, not a paragraph**
"About half the stuck segment (8 of 18) reported no incident at all — a trust message is
the wrong fix for them."

**4. What's next — one line, not a 3-card grid**
"The first real test: swap synthetic profiles for actual order history and see if the
friction match still holds."

**5. Closing line — bookends the deck back to slide 1's opening numbers**
"Blinkit's own Q1 FY27 numbers put monthly transacting customers at 31.8M — even a
modest shift in this metric moves millions of orders into a new category for the first
time." (This is the real, already-sourced figure from slide 1 — do not introduce any
number not already used elsewhere in this deck.)

## What NOT to do
- Do not invent any new statistic, percentage, or projection anywhere in this rebuild —
  every number used above is already sourced elsewhere in this deck (the metric
  definition, the 8-of-18 figure, and the 31.8M Q1 FY27 customer count).
- Do not add "category breadth per user per month" — still out of scope here.
- Do not restore the 4th guardrail, the ladder table, the dry-run stat line, or the
  3-card roadmap grid — this is a deliberate simplification, not an oversight.

---

## Prompt to paste into Design Labs

```
Rebuild the body content of the final slide ("Adoption is the metric; the guardrails are
the veto.") — keep the eyebrow, header, and yellow "Plan only" banner exactly as they
are, but replace everything below them with this simpler structure:

1. A hero metric block, given the largest visual weight on the slide: "% of monthly
   active customers who purchase from at least one new category that month" with the
   sub-line "Measured against the nudged segment's own prior month, not a headline
   average." This should visually dominate — biggest type, most prominent placement —
   with everything else on the slide reading as support for it, not as an equal.

2. A guardrails block with exactly 3 items (cut from the current 4), each framed as the
   specific risk it catches rather than a flat checklist:
   - "A nudge into a genuinely bad category" → return/refund rate and complaint rate in
     nudged categories must not rise.
   - "A nudge that cannibalizes habitual reorder" → reorder rate must not fall; opt-outs
     capped per user.
   - "Copy that invents trust it hasn't earned" → sampled nudges audited for invented
     statistics; any hit is a release blocker.

3. One single-line honest limit (not a paragraph): "About half the stuck segment (8 of
   18) reported no incident at all — a trust message is the wrong fix for them."

4. One single-line "what's next" (not a 3-card grid): "The first real test: swap
   synthetic profiles for actual order history and see if the friction match still
   holds."

5. A closing line at the bottom of the slide, visually distinct as the deck's final
   statement: "Blinkit's own Q1 FY27 numbers put monthly transacting customers at 31.8M —
   even a modest shift in this metric moves millions of orders into a new category for
   the first time."

Remove entirely: the Measurement Ladder table, the "SYNTHETIC DRY-RUN" line (you may move
it into speaker notes, but it must not remain visible on the slide), and the 3-card "What
we'd build next" grid.

Do not invent any new statistic — every number in this rebuild (the metric definition,
"8 of 18," and "31.8M") is already used elsewhere in this deck. Do not add "category
breadth per user per month." Do not change the eyebrow, header, or the yellow banner.
```
