# Design Labs prompt — slide 8: fix layout balance and visual consistency

Target slide: **slide 8**, "BlinkIQ decides, nudges, and explains itself" (The MVP, Deployed)

This is the deck's centerpiece slide — the deployed product teardown — so it needs to
read as deliberately built, not assembled. The content/copy is good; the problems are
layout: unbalanced whitespace, a disconnected floating element, and inconsistent step
styling across the three columns.

## Issues to fix
1. **Large empty space bottom-right.** The 3 stacked callout cards (trust drivers / no
   invented pricing / nothing generated until matched) end well above where the three
   screenshot columns end, leaving a tall blank gap beneath them.
2. **The floating black circle/arrow between columns 1 and 2** isn't aligned to anything
   it's meant to connect — it needs either a clear anchor point or removal.
3. **Missing step-3 marker.** Steps ① and ② have numbered circle badges; "Separately: The
   auto-nudge queue" has none, breaking the pattern.
4. **Header baseline/line-wrap inconsistency** across the three column headers, a
   downstream effect of #3.
5. **Uneven screenshot heights** — column 1 (operator console, wider desktop screenshot)
   runs much taller than columns 2/3 (narrower phone mockups), so the row doesn't read as
   a clean three-up sequence and captions land at different heights.

## What NOT to touch
- Keep the header ("BlinkIQ decides, nudges, and explains itself"), eyebrow, and "Open
  the live agent" button exactly as they are.
- Keep the "Data disclosure" card content and position.
- Keep all three screenshots and their captions' text content — this is a layout/spacing
  fix, not a content rewrite.

---

## Prompt to paste into Design Labs

```
Slide 8 ("BlinkIQ decides, nudges, and explains itself") has layout problems that need
fixing without changing any copy or screenshots:

1. Fill the empty space at the bottom-right of the slide. The three callout cards on the
   right (trust drivers / no invented pricing / nothing generated until matched) end well
   above where the three screenshot columns end, leaving a large blank gap. Either resize
   these three cards to distribute evenly across the full available height (larger
   padding, more breathing room per card), or add a 4th element that's actually useful —
   e.g. a short closing statement tying the three steps together, or extend the "Data
   disclosure" card's visual weight to balance the column. Do not just stretch empty
   padding — make the added height purposeful.

2. Remove or properly anchor the floating black circle with the yellow arrow that
   currently sits between the "Operator clicks Generate nudge" and "Shopper sees the
   nudge" columns. If it's meant to represent the flow moving from step 1 to step 2,
   align it vertically with a specific reference point in both screenshots (e.g. level
   with the "Generate nudge" button in column 1 and the top of the notification in
   column 2) rather than floating at an arbitrary height. If it can't be cleanly
   anchored, remove it — the numbered ① ② badges already communicate sequence.

3. Give the third panel ("Separately: The auto-nudge queue") a visual marker consistent
   with the numbered circles on the first two, but distinct enough to signal it's a
   parallel/separate flow rather than "step 3" — e.g. a differently-styled badge (a
   different icon or shape, not a plain number) rather than no marker at all.

4. After fixing #3, re-align all three column headers to a consistent baseline, and check
   that none of the three headers wrap to a different number of lines than the others —
   adjust column width or font size slightly if needed to even this out.

5. Even out the three screenshot heights so the row reads as one clean three-up sequence
   — scale or crop the operator-console screenshot (column 1) so its bottom edge lines up
   reasonably with the phone mockups in columns 2 and 3, rather than running noticeably
   taller.

Do not change the header, eyebrow, "Open the live agent" button, the "Data disclosure"
card's content, or any of the three screenshots' images or caption text — this pass is
layout and alignment only.
```
