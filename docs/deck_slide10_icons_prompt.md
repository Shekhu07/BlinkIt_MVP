# Design Labs prompt — slide 10: add the generated icons (cropped, defects fixed)

Target slide: **slide 10** (last slide), following the content rebuild in
`deck_slide10_rebuild_prompt.md`. This adds icons from your newly generated icon sheet —
with two fixes, since the sheet itself has visible defects that can't go on the slide.

## What's usable from the generated sheet, and what isn't
- **Person-with-groceries icon** (top left) → use for the hero Primary Metric card.
- **Shield-with-checkmark icon** (top right) → use for the Guardrails card.
- **Bar-chart-with-arrow icon** (bottom, appears twice) → do not use either copy — the
  two are visually identical (redundant) and the second one's only label, "Adontetic
  moflic," is garbled AI-generated text, not a real word.
- **The "blinkit" logo lockup at the bottom of the sheet** → do not use. It's a
  fabricated logo (checkmark-in-box) that doesn't match this deck's actual Blinkit logo
  asset (`img/blinkit-logo.png`, the lightning-bolt mark) already used on every slide.
  Keep using the real logo asset everywhere, including here.
- **Baked-in text labels on the sheet** ("Active customers trying new categories",
  "guardirails") → do not use these as-is. "guardirails" is misspelled. Crop to just the
  icon artwork and apply the slide's own typography for labels instead.

## What to do
Crop the person-icon and shield-icon out of the sheet as standalone icon graphics (no
text baked in), and place them:
- Person-with-groceries icon → next to/above the Primary Metric card headline
- Shield-with-checkmark icon → next to/above the Guardrails card headline

Both icons already use the deck's yellow/black palette, so no recolouring needed.

---

## Prompt to paste into Design Labs

```
I've generated an icon sheet with 4 icons. Two are usable for slide 10 (the final
slide), two are not — please crop and use only the following:

1. Crop out the person-surrounded-by-grocery-items icon (top left of the sheet) as a
   standalone icon with no text. Place it next to or above the Primary Metric card's
   headline on slide 10.

2. Crop out the shield-with-checkmark icon (top right of the sheet) as a standalone icon
   with no text. Place it next to or above the Guardrails card's headline on slide 10.

Do NOT use: either of the two bar-chart-with-arrow icons (they're duplicates, and one is
labelled with garbled text, "Adontetic moflic," which isn't a real word), and do NOT use
the "blinkit" logo lockup shown at the bottom of the sheet — it's a different logo design
than this deck's actual logo asset, which must stay the one already used on every other
slide.

Do not carry over any of the sheet's own text labels ("Active customers trying new
categories", "guardirails" — note this is misspelled) — use only the icon artwork itself,
and apply this slide's own headline/label typography instead.

Both icons already match the deck's yellow/black colour palette — no recolouring needed.
Keep icon size small and functional, consistent with icon sizing used on other slides in
this deck, not oversized or decorative.
```
