# Design Labs prompt — fix overflow caused by the 26px font-size floor

Context: every font size across the deck was bumped from the old 19-25px range up to a
26px minimum, to meet the fellowship guideline's floor for a Figma 1920×1080 frame. This
was verified directly (headless browser, measuring actual rendered overflow per slide)
on the coded reference file. Result: **6 slides held up fine** (1, 3, 4, 8, 9, and 2's
tiny +27px is a pre-existing font-descender artifact, not new). **4 slides now overflow**
and need layout rework, not just a font swap:

| Slide | Overflow (approx, at 1920×1080 scale) |
|---|---|
| 5 — "Research: confirmed & challenged" | ~291px |
| 6 — "Problem framing" | ~96px |
| 7 — "Why trust, not discount" | ~196px |
| 10 — "Measurement plan" | ~377px (worst) |

General approach for all four: **cut content, don't shrink text below 26px.** The floor
is a hard requirement — the fix has to come from removing/shortening copy, tightening
padding and line-height, or resizing cards, never from going back under 26px.

---

## Slide 5 — "Research: confirmed & challenged" (~291px over)
This slide accumulated the most added content across several earlier passes this
session (triangulation strip, assortment tag, "what the research challenged" card with 3
findings). Trim in this order:
1. Drop the 3rd item in the "What the research challenged" card (the packaging
   sub-cause) — it was already flagged as lowest priority when added; keep only the
   even-behavior-split finding and the churn-to-Zepto quote.
2. If still over, cut one of the 3 "Confirmed, in their words" quote cards down to 2 —
   keep the two most load-bearing (the puja-item and electronics-skepticism quotes are
   the strongest; the expired-dairy quote is the most cuttable).
3. Tighten card padding and line-height slightly across the slide before removing any
   more content.

## Slide 6 — "Problem framing" (~96px over)
Smallest overflow of the four — likely fixable without cutting content:
1. Tighten line-height and card padding on the framing-element list first.
2. If still over, shorten the longest bullet's wording rather than removing a whole
   framing element (segment / root cause / workarounds / user value / business value /
   scope limit all need to stay — this slide's job is covering all five required
   elements plus the scope limit, so cut words, not sections).

## Slide 7 — "Why trust, not discount" (~196px over)
1. If the real customer quote from the earlier cleanup pass is present ("yes I am
   skeptical of buying electronic products..."), shorten its surrounding caption/label
   text rather than the quote itself.
2. Tighten the options-considered table's row padding and the "Chosen solution" panel's
   padding.
3. If still over, shorten the "Why not a discount" explanation to one sentence instead
   of two.

## Slide 10 — "Measurement plan" (~377px over, worst)
This slide already went through a full content rebuild earlier (hero metric + 3
guardrails + one honest-limit line + one next-step line + closing line) — it's already
lean, so this needs padding/spacing discipline more than further cuts:
1. Tighten padding on all 4-5 blocks first — this slide has the least redundant content
   left to cut, so spacing discipline should do most of the work.
2. If still over, the closing bookend line (tying back to the 31.8M Q1 FY27 figure) is
   the most cuttable single element if a hard choice is needed — but try padding/spacing
   fixes on every other block first, since losing the bookend line weakens the deck's
   ending.
3. Do not cut any of the 3 guardrails or the honest-limit line — those are required
   content, not padding.

---

## Prompt to paste into Design Labs

```
The font-size floor across this deck was raised to 26px minimum (compliance requirement
for a Figma 1920×1080 frame). Four slides now overflow their frame as a result and need
layout fixes — text must stay at 26px or larger, so fix this by cutting/shortening
content and tightening spacing, never by shrinking text back down.

Slide 5 ("Research: confirmed & challenged"), overflowing by roughly 291px: first, drop
the 3rd item (packaging sub-cause) from the "What the research challenged" card, keeping
only the even-behaviour-split finding and the churn-to-Zepto quote. If still overflowing,
cut the "Confirmed, in their words" quote cards from 3 to 2, keeping the puja-item and
electronics-skepticism quotes and dropping the expired-dairy one. Tighten padding and
line-height throughout before cutting further.

Slide 6 ("Problem framing"), overflowing by roughly 96px: tighten line-height and card
padding first — this is the smallest overflow and likely fixable without removing
content. All five required framing elements (segment, root cause, workarounds, user
value, business value) plus the scope limit must stay; if still over after tightening
spacing, shorten wording within the longest bullet rather than removing a section.

Slide 7 ("Why trust, not discount"), overflowing by roughly 196px: shorten the caption
around the electronics-skepticism customer quote (keep the quote itself intact), tighten
the options-considered table's row padding and the "Chosen solution" panel's padding, and
if still over, cut the "Why not a discount" explanation to a single sentence.

Slide 10 ("Measurement plan"), overflowing by roughly 377px (the worst of the four):
tighten padding across all blocks first — this slide is already lean content after an
earlier rebuild, so spacing discipline should resolve most of this. If a cut is still
needed, the closing line tying back to the 31.8M Q1 FY27 figure is the most expendable
single element, but exhaust padding/spacing fixes on every other block first. Do not cut
any of the 3 guardrails or the honest-limit line.

Do not shrink any text below 26px on any slide as a shortcut. Do not touch slides 1, 2,
3, 4, 8, or 9 — they already fit correctly at the new 26px floor.
```
