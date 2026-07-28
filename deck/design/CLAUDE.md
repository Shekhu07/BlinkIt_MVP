# Blinkit category-stagnation case study deck

Main file: `Blinkit Category Nudge Case Study.dc.html` (10 slides, 1920×1080, deck-stage).
Snapshots in `versions/`: v1 (pre-branding), v2 (logo + tinted cards, screenshot-led slides 3-5),
v3 (NextLeap-style chart pages on slides 3-5). **v3 is no longer the live file** — the main file
has since taken the three fixes listed under "Recent changes" below. Snapshot a v4 before the next
structural edit.

## Hard rules (graded)
- Exactly 10 slides, no appendix slide. Title slide counts as one.
- Invent nothing beyond two sourced sets: the DATA APPENDIX in the original brief, and (slide 1 only) Blinkit's
  published Q1 FY27 metrics from Eternal's shareholders' letter/earnings call — 31.8M avg monthly transacting
  customers (16.9M YoY), 331M quarterly orders, 2,443 dark stores, NOV +86% YoY to Rs 17,132 cr, AOV slightly down.
  Slide 1's "Discovery on Blinkit today" card describes public app surfaces only and says so.
  No A/B results, conversion rates, uplifts, p-values, live-usage funnels, per-user confidence
  scores, real Blinkit pricing, or the Eternal inventory-loss "1.8% of NOV" figure.
- The fellow's name appears nowhere in visible text. No raw URL is ever rendered as visible text: slide 1's two
  cards are label-only hyperlinks ("Open the live extractor →" / "Open the live agent →") whose
  hrefs carry the Hugging Face URLs; slide 3 says the workflow is linked from the title slide.
  Discovery-engine screenshots were cropped to remove the HF account badge; keep them cropped and
  never substitute an uncropped capture — the account pill carries the name along the top edge.
  **Known residual:** the name still sits inside those two `href` values and in the `data-props`
  block, so it surfaces in a PDF link annotation and on hover. No deck edit fixes that; it needs
  the Spaces moved to an HF organization account (requires Pro).
- Min type 14pt (~19px) on **anything rendered**, including chips, captions, table cells and
  footnotes. Single-character decorative glyphs count — four chips were shipped at 17px once.
- Colour-blind safe: green #146634 / amber #7A6100 always paired with a word or glyph.
- Assertion-style slide titles + small letterspaced uppercase eyebrow above each.

## Verification — `scrollWidth/scrollHeight` on the section is NOT sufficient
A `<section>` keeps reporting exactly 1920×1080 while an inner grid overflows and visibly clips
content behind the band beneath it. A broken slide 10 passed review this way once. Check the
sections **and** sweep every container:

```js
[...document.querySelectorAll('section[data-label] *')]
  .filter(e => e.scrollHeight - e.clientHeight > 20 && e.clientHeight > 0)
  .map(e => e.closest('section').getAttribute('data-screen-label')
            + ' +' + (e.scrollHeight - e.clientHeight))
```

Expected: exactly one entry, `02 Why it matters +27` — a font-descender artefact on the 58%
numeral, not clipping. Any other entry means a slide is broken. Also confirm all 10 sections
measure 1920×1080, and that no rendered text computes below 19px (ignore `<style>`/`<script>`
nodes, which report 16px).

## Slide 10 has a hard height budget — read before touching it
Its two-column grid gets **exactly 612px** and is the tightest thing in the deck. Measured:

| Attempt | Needed | vs 612 |
|---|---|---|
| before the current fix | 627 | +15 (was clipping) |
| one new line added to each column | 723 | +111 |
| a 5th guardrail as its own item, 2-col | 723 | +111 |
| a 5th guardrail, guardrails grid → 3 columns | 739 | +127 (worse — narrower cells wrap more) |
| a 5th guardrail + tighter ladder padding | 699 | +87 |
| **merged into the nudge-fatigue cell + ladder padding 14px → 10px (current)** | **612** | **0** |

The slide now sits at exactly 612 with zero slack. Anything added must be paid for by removing
something — say what you removed.

## Survey figures (N=31, frozen 2026-07-28, revised up from 25)
58% stick to same categories (18 of 31) · 15 of 31 had a bad order (11 damaged · 2 expired ·
1 fake · 1 other; 11 refunds · 3 replacements · 1 unresolved) · 7/7/1 behaviour split ·
8 of 18 stuck users with no incident · rated hesitancy mean 3.0 (11 agree / 11 disagree / 9 neutral).
Q15 drivers: refund 13 · quality 10 · inspect 7 · reviews 5 · offers 5 · nothing 4 · agent 3 ·
packaging 1 (write-in). Part 1 engine numbers unchanged.

**Inspect-before-accepting is the THIRD driver (7); item reviews are FOURTH (5).** They were tied
third at N=25 — never label reviews as the third driver, and never describe the MVP's peer
social-proof line as mapping to the third-ranked driver.

Stale N=25 figures that must never reappear: 56%, 14 of 25, 13 of 25, 11/25, 9/25, 5/25,
6 of 13, 6 of 14, 8 of 14.

## Recent changes (already applied to the main file)
1. Slide 2's `data-speaker-notes` said 56% while the slide said 58% — corrected.
2. Four glyph chips (`!`, `%`, `✓`) sat at 17px, under the 19px floor — raised to 19px.
3. Slide 10 gained the **order-frequency counter-metric**, folded into the nudge-fatigue cell
   ("Order frequency and nudge fatigue — reorder rate must not fall; opt-outs capped per user"),
   paid for by the ladder padding reduction. It guards the failure where a push nudge degrades the
   habitual reorder flow it interrupts.

**Category breadth per user per month is deliberately NOT on slide 10** — there is no room. It is
the companion to the primary metric that catches the hollow win (adoption rises, breadth flat) and
lives in the project's `script.md` §5.1 as spoken material. Do not add it without removing something.

## Visual system
Yellow #F8CD1B accent, ink #16130A, page #F4F5F3, white cards + 1px #E7E8E2 + 20px radius,
Plus Jakarta Sans 400/600/800. Dark panels used sparingly (slides 2, 4, 5, 6, 7, 9, 10 accents).
Brand green #318616 (sampled from the logo) is the second accent — graphics only (numeral badges,
donut rings), never small text; small green text stays #146634 for contrast. Meaning-tinted cards:
confirmed/value = #EDF5E9 + 1px #CFE3C6; chosen/highlight = #FFF9DF + 1px #F8CD1B or #F0DFA0;
neutral = white; limit/caution = dark #16130A. Page stays flat #F4F5F3 on every slide — the ONLY
gradient in the deck is the soft yellow radial glow top-right of slide 1. No gradient page washes.
Logo lockup: img/blinkit-logo.png (transparent, cropped from press kit) at 104px + 1px #D8D9D2
divider, left of the eyebrow on slides 2-10; 240px above the eyebrow on slide 1.
Screenshot frames: 1px #E7E8E2, 14px radius, shadow 0 8px 24px rgba(0,0,0,.10). No recolouring,
no browser chrome or device mockups around captures.

## Screenshots in use (in `img/`)
- slide 3: `disc-01-extractor-pass-crop.png`, `disc-02-extractor-reject-crop.png` — 452x246 proof
  thumbnails in the bottom band (the workflow chart is the hero now, not the captures)
- slide 4: `disc-04-results-explorer-crop.png` — 596x576 right rail
- slide 8: `mvp-02-phone-nudge.png` (0.41), `mvp-03-reasoning-ranked.png` (0.97), `mvp-07-lockscreen.png` (0.36)
- slide 9: `mvp-04-out-of-scope.png` (1.03)
Unused reserve captures live in the attached `screenshots` folder (auto-queue, cart-filler, full console).
All three `disc-*-crop` files use `object-fit:cover; object-position:top`, so the top of the image
is what shows — the crop must remove the account pill from the top, not anywhere else.

## Slides 3-5 layout (NextLeap-style chart pages)
Slide 3 = workflow infographic: funnel hero band (15,820 -> 4,740 -> 1,094) + 5 numbered step cards
with green tick bullets (step 3 dark) + gate-proof thumbnails + gate/measures rail.
Slide 4 = 4 numbered insight cards (2x2) + category bar chart (real extraction counts) + Results
Explorer rail + dark "core problem" band.
Slide 5 = three columns: quantitative validation (three #318616 donut rings + the 11/9/11 rated
split bar) / dark "what the survey challenged" / green-tinted "confirmed, in their words" quotes,
closed by a yellow "the verdict" band. Chips are 34-40px rounded squares with a numeral or glyph
(no icon set in the project — do not hand-draw icons).

## Props / tweaks
`showDemoConstants` (bool) — the ₹199 / ₹35 illustrative-constant caveat on slide 8.
