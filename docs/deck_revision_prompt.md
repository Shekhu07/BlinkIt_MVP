# Claude Design Labs — revision prompt for the existing 10-slide deck

Use this **on the already-built deck** (the one whose current state is `Design.pdf`), not from
scratch. It is a change list keyed to slide numbers, so the visual system, layout and all
unmentioned content stay exactly as they are.

Companion to `deck_design_prompt.md` (the original build brief) — that file's ABSOLUTE RULE,
hard output constraints and visual system still apply and are restated below in short form.

**Why these changes:** two of them are graded blockers (the fellow's name is visible on the
deck; the Part 3 slide is missing two of the five mandatory problem-statement elements), and
the survey was re-frozen at N=31 on 2026-07-28, which moved every sample figure and re-ranked
the Q15 drivers. Full rationale in `problem_statement.md` §4 and `part2_research_tracker.md`.

---

```
You previously built me a 10-slide product case-study deck about a Blinkit PM fellowship
project (AI discovery engine → user research → problem definition → deployed MVP). I need
targeted revisions to that existing deck. Keep everything not mentioned below exactly as it
is — same visual system, same layout structure, same slide order, same 10-slide count.

## Rules that still apply (unchanged from the original brief)
- INVENT NOTHING. Every number, quote and label you may use is either already on the deck or
  listed explicitly below. Do not invent conversion rates, lifts, sample sizes, confidence
  scores, prices or user counts. If a panel seems to need a number I have not given you,
  write the qualitative claim instead.
- EXACTLY 10 slides. Do not add or remove a slide.
- Minimum 14pt-equivalent font, including footnotes, captions and table cells.
- Colour-blind safe: never encode meaning in colour alone; always pair with a word or icon.
- Slide titles are assertions (full sentences), never labels.
- Blinkit yellow #F8CD1B accent, ink #16130A, page #F4F5F3, white cards, Plus Jakarta Sans.

===========================================================================
CHANGE 1 — CRITICAL. Remove the person's name from the deck (slides 1 and 3)
===========================================================================
The deck currently prints these raw URLs:
  slide 1, both link cards: huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine
                            huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent
  slide 3, bottom-right sidebar: a third, truncated copy of the discovery URL
That path segment contains my name, and the deck is graded on containing no name anywhere.

Fix on all three: DELETE the visible URL string entirely. Render each link card as a
hyperlink whose visible text is a label only:
  card 1 eyebrow "LIVE · DISCOVERY WORKFLOW", link text "Open the live extractor →"
  card 2 eyebrow "LIVE · DEPLOYED MVP",       link text "Open the live agent →"
On slide 3, replace the truncated URL line with the plain sentence:
  "The full workflow is live and linked from the title slide."
Never render a raw URL as visible text anywhere in the deck. Keep the cards' size and
position so slide 1's composition does not change.

===========================================================================
CHANGE 2 — CRITICAL. Slide 6 must show all five required problem elements
===========================================================================
Slide 6 is graded against a fixed checklist of five elements: target segment, root cause,
existing user workarounds, why solving it creates USER value, why solving it makes BUSINESS
sense. The current six cards spend two slots on "How we know" and "Why now" — which are not
on the checklist — and omit workarounds and user value entirely.

Keep the same 3×2 grid, the same card styling, and keep the dark "SCOPE LIMIT" card in the
bottom-right exactly as it is. Replace the other five cards with these, in this order:

  01 · WHO IT'S FOR
  Heavy, habitual repeat buyers.
  High-frequency customers who default to the same narrow set of categories every month.
  18 of 31 surveyed describe themselves this way.

  02 · THE ROOT CAUSE
  Trust, not discovery.
  A damaged, expired or fake item teaches the customer that a category is unsafe to buy
  here — so they retreat to essentials, or leave for another app. It is not an awareness
  problem: these buyers already see the other categories every week.

  03 · HOW THEY COPE TODAY
  Two workarounds, both costly.
  Retreat to essentials only — "I only order the essential items now if anything urgent."
  Or switch platforms outright — "I have started using Zepto more." The first suppresses
  category adoption silently; the second is active share loss.

  04 · WHY IT'S WORTH IT FOR THE USER
  They want to consolidate — they just can't risk it.
  These customers already trust Blinkit for staples and would rather buy more in one app
  than juggle three. 27 of 31 named at least one concrete change that would let them —
  only 4 said "nothing in particular" — led by a refund guarantee (13 picks) and a visible
  quality signal (10). No new need is being invented.

  05 · WHY IT'S WORTH IT FOR THE BUSINESS
  Basket width is the growth lever the company has named.
  Restoring trust re-opens non-grocery categories for customers who already order
  frequently — no new acquisition required.

Then add a single thin footer line beneath the grid, 14pt, muted:
  "Evidence base: 1,094 gate-passing review extractions (70% quality-driven) and 31 survey
   responses (15 with a recent bad order) point at the same failure."
(That sentence preserves the "how we know" content the old card 03 carried, without spending
a checklist slot on it.)

===========================================================================
CHANGE 3 — Update every survey figure. The sample grew from 25 to 31.
===========================================================================
Replace on whichever slides they appear. Left = what the deck says now, right = correct.

  slide 2 hero stat:      56%           →  58%
  slide 2 hero sublabel:  "of surveyed users self-report that they mostly stick to the
                           same categories"  (unchanged wording)
  slide 2 source line:    "primary survey, 14 of 25 responses. No live interviews
                           conducted."  →  see CHANGE 6 for the replacement wording
  slide 5 sample box:     "25 survey responses"        →  "31 survey responses"
  slide 5 footer left:    "13 of 25 had a bad order in the last 3 months: 10 damaged ·
                           1 expired · 1 fake or duplicate · 1 other. Resolution: 9 full
                           refunds · 3 replacements · 1 unresolved."
                        →  "15 of 31 had a bad order in the last 3 months: 11 damaged ·
                           2 expired · 1 fake or duplicate · 1 other. Resolution: 11 full
                           refunds · 3 replacements · 1 unresolved."
  slide 5 "even split":   "Of the 13 with a bad order: 6 confirmed a change in behaviour,
                           6 reported no change, 1 ambiguous."
                        →  "Of the 15 with a bad order: 7 confirmed a change in behaviour,
                           7 reported no change, 1 ambiguous. The split stayed exactly even
                           when the sample grew."
  slide 5 "half stuck":   "6 of the 14 who stick to the same categories reported no bad
                           order."  →  "8 of the 18 who stick to the same categories
                           reported no bad order."
  slide 6 footer:         as written in CHANGE 2
  slide 7 footnote:       refund 11 · quality 9 · reviews 5 · inspect 5 · agent 3 ·
                           offers 3 · nothing 3
                        →  see CHANGE 4

Do not change the Part 1 engine numbers (15,820 / 4,740 / 1,094 / 770 / 70% / 16-of-20).
Those come from a different data source and are unaffected.

===========================================================================
CHANGE 4 — Slide 7: the driver ranking changed. One table row is now wrong.
===========================================================================
Replace the Q15 footnote under the table with:
  "Ranked survey drivers, Q15 'what would make you try a new category' (pick up to 2), N=31:
   no-questions-asked refund or return guarantee 13 · better visible quality and freshness
   guarantees 10 · inspect before accepting delivery 7 · item reviews and ratings 5 ·
   intro offers 5 · nothing in particular 4 · human support agent 3 · safer packaging for
   fragile items 1 (written in, not offered as an option)."

In the OPTIONS CONSIDERED table, the row currently reading "Surface item reviews and
ratings / Pre-purchase doubt — ranked 3rd driver, 5 of 25" is now factually wrong: that
option dropped to joint fourth. Replace that whole row with the option that overtook it:

  Option:          Let users inspect before accepting delivery
  Pain it solves:  Pre-purchase doubt — now the 3rd-ranked driver, 7 of 31
  Whole segment?:  Partly — helps at the door, not at the moment of choosing
  Differentiated?: No — an ops change any rival can match, and it slows every handover

Keep the chosen "Trust-led category nudge" row highlighted exactly as it is, but update its
"Pain it solves" cell to read: "The top two named blockers: refund certainty 13/31, then
quality 10/31".

===========================================================================
CHANGE 5 — Slide 5: add two findings that are currently missing
===========================================================================
(a) Add a fourth item to the CHALLENGED column, after "Half the stuck group had no incident":

  The rated answers are just as split.
  Asked directly whether a bad experience in one category makes them hesitant to try
  others (1–5): mean 3.0 — 11 of 31 agree, 11 of 31 disagree, 9 neutral.

This is the single strongest item on the slide: it is the deck's core claim, asked as a
direct question, and the answer is a dead-even split. Give it the same weight as the others.

(b) In the existing "Packaging is a distinct sub-cause" item, append one sentence:
  "The same respondent wrote in the fix unprompted — 'better and safer packaging guarantees
   for fragile items' — rather than picking any option offered."

===========================================================================
CHANGE 6 — Slide 5 and 2: reframe the missing-interviews note
===========================================================================
The deck twice states, flatly, that no live interviews were conducted. Keep the honesty —
do not delete or soften the fact — but state the trade-off rather than only the absence.

Slide 5, replace the "SAMPLE, STATED HONESTLY" box body with:
  "31 survey responses. No live interviews were conducted — a deliberate trade of depth for
   breadth against a fixed deadline. The form's open-ended fields carry the verbatims quoted
   here; six respondents consented to follow-up calls that were not run."

Slide 2, replace the hero card's source line with:
  "Source: primary survey, 18 of 31 responses. Survey-based; no live interviews."

===========================================================================
CHANGE 7 — Slide 10: add what happens next
===========================================================================
The deck currently ends on measurement and never says what would be built next, which is a
graded item ("open questions or follow-on experiments"). Keep the primary metric card, the
measurement ladder and the guardrails. Add a compact third band across the bottom titled
"WHAT WE'D BUILD NEXT", three items side by side, 14pt minimum:

  1 · Let users inspect before accepting
  The 3rd-ranked driver (7 of 31) and the highest-ranked thing this MVP deliberately does
  not do. It is an operations change, not a message — which is exactly why it was scoped out.

  2 · A relevance-led nudge for the low-intent half
  8 of 18 stuck users had no bad experience at all. A trust message is the wrong instrument
  for them; the open question is whether a cart-level prompt moves them at all.

  3 · Real behavioural data instead of synthetic profiles
  Every profile here is synthetic. The first real test is whether the friction match holds
  against actual order history.

===========================================================================
CHANGE 8 — Legibility and colour fixes
===========================================================================
(a) Several annotation captions are far below the 14pt floor and will fail the font check.
    Raise every one to at least 14pt equivalent, or delete it. The worst offenders are the
    grey explanatory lines beneath the "Also considered — ranked" panels on slides 8 and 9
    (the "Adjacency weight from the user's existing basket…" text), and the small captions
    under the three phone/panel screenshots on slide 8. Text baked inside a screenshot image
    is fine and does not need changing — only live text does.

(b) On slide 7's table, the "Whole segment?" and "Differentiated?" cells render "Yes" and
    "No" in the same green, so the colour carries no meaning. Prefix every one with an
    explicit glyph — "✓ Yes …" / "✗ No …" — and use ink for ✗ rows, green #146634 only for
    ✓ rows.

(c) On slide 4, change "Categories named inside the top theme, roughly proportional to
    volume:" to "Top five named categories inside the top theme, roughly proportional to
    volume:" — the five numbers listed do not sum to 770 and should not imply they do.

===========================================================================
CHANGE 9 — Optional, only if it fits without shrinking type
===========================================================================
On slide 3, add one muted 14pt line beneath the five-stage pipeline strip:
  "The engine answers the brief's discovery questions directly: why users repeat, what blocks
   new categories, what frustrations recur, and which unmet needs persist."
Skip this entirely if it forces any other element below 14pt.
```

---

## After the deck comes back

Check these before exporting, in this order — the first two are the ones that fail silently:

1. **Search the rendered deck for "Abhishek"** (and for "huggingface.co"). Both must return
   nothing. Then strip the PDF's Author/Creator metadata on export:
   `exiftool -Author= -Creator= -Producer= "NL Blinkit Category Adoption.pdf"`
2. **Count the slides.** Ten, including the title. Eleven is an automatic penalty.
3. Slide 6 shows all five checklist elements: segment · root cause · workarounds · user value ·
   business value.
4. Smallest live text ≥ 14pt. Zoom to 400% on slides 8 and 9 and check the grey annotations.
5. Both links resolve from the exported PDF (click them — anchor text still has to be a live
   hyperlink, not just styled text).
6. File < 40 MB, named in the "NL Blinkit…" convention, no name in the filename.
