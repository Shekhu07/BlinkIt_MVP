# Design Labs prompt — slide 10 (final slide): new header, fix self-contradiction, add icons

Target slide: **slide 10** (last slide), currently headed "We would judge this on
new-category adoption, in three tiers, with trust guardrails" (Measurement · Proposed,
Not Yet Measured)

This is the closing slide and gets the most scrutiny — the content and narrative closure
are actually strong (verified against the deck's frozen N=31 figures and prior slides),
but there's one real accuracy problem, a header update, and an opportunity to add icons
consistent with the rest of the redesigned deck.

## Header change (decided)
Replace the current headline with: **"Adoption is the metric; the guardrails are the veto."**
This states the actual mechanism on the slide — a primary metric that says whether it
worked, and four guardrails that can each independently veto calling it a win (refund
rate, order frequency/fatigue, complaints, invented-stat audit) — rather than just
labelling the topic. Keep the same font, size, weight, and position as the current
headline; text swap only.

## Required fix (accuracy, not style)
The yellow "Plan only" banner states: *"No experiment has been run... so no result
numbers appear on this slide."* But the Measurement Ladder box directly below it shows:
*"SYNTHETIC DRY-RUN, 2026-08-03 — Gate and nudge generation ran end-to-end on all 8
synthetic profiles: 5/8 triggered correctly, 5/5 generated across 4 categories."* Two
numeric ratios appear on the same slide that claims none do. This is a self-contradiction
an evaluator will catch — even though the dry-run is a code-verification check (not a
user-behavior result), it's formatted exactly like every other real stat in this deck.

Fix: reword the dry-run line to remove the numeric ratios, keeping the substance
qualitative — e.g. "Verified end-to-end on all 8 synthetic profiles, spanning 4
categories — confirms the pipeline runs, not a substitute for real usage data, which
doesn't exist yet." Do not invent new numbers to replace the removed ones.

## Optional addition (icons)
Add small icons consistent with the Stitch icon set already used elsewhere in this deck
(`icon-s5-*`, `icon-s6-*`, `icon-s7-*` naming pattern) — one per major card:
- Primary Metric card → a target/bullseye icon
- Measurement Ladder card → a stepped-tiers icon
- Guardrails card → a shield/barrier icon
- "What we'd build next" section → a roadmap/forward-arrow icon
- Small flask/test-tube badge next to "SYNTHETIC DRY-RUN" — visually reinforces it is not
  real usage data

## What NOT to touch
- Don't change any number: the primary metric definition, the 3-tier ladder structure,
  the "7 of 31" / "8 of 18" references, or any guardrail text.
- Don't add "category breadth per user per month" to this slide — it's deliberately
  scoped out elsewhere due to space, and that decision still holds.
- Don't invent any new statistic anywhere on this slide, including as a replacement for
  the removed dry-run ratios.

---

## Prompt to paste into Design Labs

```
On the final slide ("We would judge this on new-category adoption, in three tiers, with
trust guardrails"), make one header change, one required fix, and one optional addition:

1. HEADER: replace the current headline with "Adoption is the metric; the guardrails are
   the veto." Keep the exact same font, size, weight, and position — text swap only.

2. REQUIRED: the yellow "Plan only" banner (top right) states no result numbers appear
   on this slide, but the "SYNTHETIC DRY-RUN, 2026-08-03" line inside the Measurement
   Ladder box currently reads "Gate and nudge generation ran end-to-end on all 8
   synthetic profiles: 5/8 triggered correctly, 5/5 generated across 4 categories" — two
   numeric ratios that contradict the banner's claim. Reword this line to remove the
   ratios while keeping the same substance, e.g.: "Verified end-to-end on all 8 synthetic
   profiles, spanning 4 categories — confirms the pipeline runs, not a substitute for
   real usage data, which doesn't exist yet." Do not introduce any new number in its
   place. Keep the same small, muted caption styling already used for this line.

3. OPTIONAL: add small icons consistent with this deck's existing Stitch icon set (used
   on other slides), one per section:
   - Primary Metric card → target/bullseye icon
   - Measurement Ladder card → stepped-tiers icon
   - Guardrails card → shield/barrier icon
   - "What we'd build next" section header → roadmap/forward-arrow icon
   - A small flask/test-tube badge next to "SYNTHETIC DRY-RUN" specifically, reinforcing
     that it is not real usage data
   Keep icons small and functional (clarifying which card is which at a glance), not
   decorative — consistent with how icons are used elsewhere in this deck.

Do not change any number, statistic, or the 3-tier ladder structure. Do not add
"category breadth per user per month" to this slide. Do not invent any new statistic,
including as a replacement for the dry-run ratios removed in step 2. Do not change the
eyebrow ("MEASUREMENT · PROPOSED, NOT YET MEASURED") or anything else on the slide beyond
what's listed in steps 1-3.
```
