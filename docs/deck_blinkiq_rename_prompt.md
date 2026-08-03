# Design Labs prompt — rename the agent to BlinkIQ across slides 1, 7, 8

Target file: `deck/design/Blinkit Category Nudge Case Study.dc.html`

The agent's name has changed from "Blink & Try It" to **BlinkIQ**. The underlying HTML
text has already been updated directly in the three spots below — this prompt is for
Design Labs to restyle/re-render those same spots so the visual treatment (weight, size,
kerning, wrap) suits the new, shorter name, since "BlinkIQ" is a single word rather than
a three-word phrase and may sit differently in each layout.

---

## Prompt to paste into Design Labs

```
The Category Nudge Agent in this deck is named BlinkIQ (previously "Blink & Try It").
The text has already been swapped in three places — check the visual treatment still
works for each, since BlinkIQ is a single word and the old name was three:

1. Slide 1 (title slide), intro paragraph: "...a deployed AI-native MVP — BlinkIQ, the
   Category Nudge Agent." BlinkIQ is bolded inline inside a lighter paragraph. Confirm
   the bold/regular contrast still reads clearly with the shorter word — it should not
   look like an orphaned bold fragment.

2. Slide 7 ("Chosen solution" dark panel): headline reads "BlinkIQ — the Category Nudge
   Agent" — BlinkIQ large and bold (34px, 800 weight), "— the Category Nudge Agent" in a
   lighter sub-treatment (22px, 400 weight, muted colour) on the same line. Check this
   doesn't leave excess empty space where the old longer name used to fill the line —
   rebalance the two segments' relative size/spacing if BlinkIQ now looks too small or
   isolated next to the longer descriptor.

3. Slide 8 h2 headline: "BlinkIQ: a nudge with a reason attached" (48px, 800 weight,
   max-width 1150px). Confirm it doesn't wrap and doesn't leave the line looking short
   and unbalanced now that the name portion is a single word — if it reads too sparse,
   suggest a tracking/size adjustment for just the "BlinkIQ" token, not a full headline
   rewrite (the copy itself is locked).

For all three: do not change any other slide, do not alter layout, colours, or any other
copy. Do not reintroduce "Blink & Try It" anywhere. Do not invent new claims, stats, or
taglines. Output before/after visual notes only — I will confirm before you apply.
```

---

## Notes for whoever runs this
- Only slides 1, 7, 8 contain the agent name — confirmed by a full-file grep before writing
  this prompt.
- This is a restyle pass, not a copy pass — the wording is already final and locked; Design
  Labs should only judge whether size/weight/spacing needs a nudge now that "BlinkIQ" is
  shorter than "Blink & Try It".
