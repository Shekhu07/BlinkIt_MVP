# Image regeneration prompt — corrected customer-journey illustration

Purpose: a 3-panel illustrated sequence of a loyal Blinkit customer over time, matching
the art style of the image already generated, but fixing two problems: it currently
shows basket diversity *increasing* with tenure (the opposite of this project's actual
finding — loyal, long-tenure customers stay narrow), and it uses green as the dominant
brand color plus a fabricated app UI, both inconsistent with the deck's real visual
system and real product.

## What must change from the original generation
- **The story**: same three time markers (Stage 1 / 6-12 months / 1+ year), but the
  basket contents should stay visually the SAME category mix across all three panels
  (fresh vegetables, rice/dal, milk, basic staples) — what changes across panels is
  confidence and ease (she looks more at-home, orders faster, larger quantity of the
  same staples), not variety. The third panel should NOT show new categories like
  electronics or expanded personal care — that's the exact claim this project's data
  contradicts.
- **Color system**: yellow (#F8CD1B) and black/ink as the dominant colors on any Blinkit
  branding (logo, bag, accents) — not green. Green may appear only as a minor secondary
  touch (e.g. a small produce/plant detail), never as the dominant brand color.
- **No app UI mockups**: drop the phone-screen panels entirely. Fabricated interface
  screens risk being mistaken for real product screenshots, and this deck is careful to
  only ever show real captures of the actual deployed product. Keep this purely as
  ambient/mood illustration — three character panels, no UI.

## Prompt to use in the image generation tool

```
A warm, hand-illustrated digital painting in three panels, consistent character and art
style across all three (same woman, same illustration technique — soft linework, warm
natural lighting, cozy Indian home interior with plants, curtains, morning light).

Panel 1, labelled "Stage 1 — Excited customer": a young woman in a saree stands by a
sunlit window, happily unpacking a Blinkit-branded grocery bag (bag design: yellow
#F8CD1B and black "blinkit" wordmark with a small lightning-bolt mark, NOT green) — bag
contains fresh vegetables, a small pack of rice or dal, a small oil bottle. Her
expression is curious, delighted, discovering the app for the first time.

Panel 2, labelled "6-12 months — Building trust": the same woman, same home, now more
at ease, holding a slightly larger version of the SAME grocery mix — more fresh
vegetables, more of the same staples (rice, dal, oil, milk) — not new product
categories. Her posture is relaxed and confident, comfortable with the routine.

Panel 3, labelled "1+ year — Loyal, but still narrow": the same woman, same setting,
now clearly at-home and habitual — ordering quickly, barely looking at the bag as she
unpacks it. The bag still contains essentially the SAME category mix as panels 1 and 2
(vegetables, staples, dairy) just in a well-worn, familiar rhythm — no electronics, no
personal care, no new categories. The visual message: loyalty grew, but what she buys
did not widen.

Style notes: warm earthy palette (terracotta, cream, sage green for plants/produce
only), soft golden natural light, no harsh outlines, illustrated/painterly rather than
photorealistic, consistent character design across all three panels. Blinkit branding
(logo, bag) must use yellow #F8CD1B and black/ink only — no green as a dominant brand
color anywhere. Do not include any phone, app screen, or UI element in any panel — this
is a pure character/mood illustration, no interface mockups.
```

## Caption text to pair with the regenerated image (unchanged from your original layout)
- Panel 1: "Stage 1 · Excited Customer — Discovering Blinkit and placing first orders"
- Panel 2: "6-12 Months · Building Trust — Relying on Blinkit for quality, speed, and variety"
  — note: consider trimming "and variety" here since panel 2 shouldn't visually suggest
  category variety increased; "quality and speed" alone matches the corrected art.
- Panel 3: "1+ Year · Loyal, but still narrow — Blinkit is her go-to, for the same few
  categories every time" — reworded from "her go-to for every need" to avoid implying
  category breadth, which is the opposite of this project's finding.
