# Design Labs prompt — slide 7: clean up speaker notes + fill the empty space

Target slide: **slide 7**, "Trust beats price: customers said so themselves" (Solution
Choice). This addresses the two items left open after the name-reveal fix
(`deck_slide7_name_reveal_prompt.md`).

## 1. Speaker notes cleanup (required)
The speaker notes field currently contains an unexecuted edit instruction typed directly
into the notes: *"Change the header for this slide. also remove the Ranked survey
drivers part from the bottom half."* That's a leftover to-do, not real speaker notes —
it should read like the rest of the deck's notes (a factual summary an evaluator/speaker
would actually use), not an instruction to whoever is editing the slide.

## 2. Fill the empty bottom space (my recommendation: real quote)
Of the three options discussed earlier — a real customer quote, a citation strip, or a
"why not the runner-up" note — the quote is the strongest fit: the header claims
"customers said so themselves," but nothing on this slide currently shows an actual
customer's words, only paraphrased rankings in the table. Using this space says:
if you want a different option instead (citation strip or runner-up note), tell me and
I'll redraft this part before you apply anything.

---

## Prompt to paste into Design Labs

```
On slide 7 ("Trust beats price: customers said so themselves"), two fixes:

1. Replace the current speaker notes with a factual summary (no embedded instructions):
   "Options considered and why the trust-led nudge wins. Grounded in the ranked survey
   drivers: refund guarantee 13 of 31, quality/freshness 10 of 31."

2. In the empty space at the bottom of the slide (below the options-considered table),
   add one real customer quote that grounds the header's claim ("customers said so
   themselves") in an actual voice rather than paraphrased numbers. Use this quote,
   already sourced elsewhere in this deck's research (slide 5's confirmed-findings
   panel): "yes I am skeptical of buying electronic products from Blinkit and other
   similar applications" — attributed as "Damaged electronics" (same attribution used
   where this quote already appears). Style it to match the deck's existing quote-card
   pattern: light tinted background, 1px border, rounded corners, italic quote text,
   bold coloured attribution line underneath.

Keep all type at or above 19px (14pt). Do not change the options-considered table, the
"Chosen solution" panel, or anything on any other slide. If the quote doesn't fill the
space well on its own, tell me rather than stretching it — options at that point are a
citation strip ("Ranked survey drivers, Q15 'what would make you try a new category'
(pick up to 2), N=31") or a short "why not the runner-up" note, both discussed earlier.
```
