# Claude Design prompt — rebuild Slide 2 only

Paste everything below the line into Claude Design Labs. It is self-contained: it repeats the
visual system and the invent-nothing rule so it can be run without the full deck prompt.

**Why this rebuild:** the current Slide 2 leads with "58% of surveyed users self-report sticking
to the same categories." That figure comes from a 31-response survey — the weakest evidence in
the project (roughly ±17pp at that sample size) — and it was doing the heaviest job on the
earliest substantive slide, while the 1,094-extraction corpus didn't appear until Slide 4. It is
also redundant with Slide 5, which exists to present the survey. The 58% moves to Slide 5; Slide 2
becomes the business-opportunity and competitive-stakes slide it should have been.

---

I need you to rebuild Slide 2 ofthe existing 10-slide product case-study deck. Everything
else in the deck stays as it is. Match the existing visual system exactly — this slide has to sit
inside the current deck without looking like it came from somewhere else.

## The deck this belongs to

A product case study on Blinkit (Indian quick commerce). The growth goal being moved is:
**increase the % of monthly active customers who purchase from at least one new category each
month.** The deck's argument is that heavy repeat buyers keep narrow baskets, and that this is a
**trust problem, not an awareness problem** — they have already seen the other categories in the
app.

Slide 2's job in that argument: establish **why this problem is worth solving at all** — the size
of the prize, the company's own strategic commitment to it, and what it costs if it goes unsolved.

## ABSOLUTE RULE — invent nothing

Every number, quote and claim you may use is in the DATA APPENDIX at the end. Use ONLY those.

- Do NOT invent market-share figures, competitor metrics, growth rates, user counts, revenue,
  or category counts.
- Do NOT invent quotes or company statements.
- Do NOT rate, score, or rank competitors on any dimension. See the prohibition below — this is
  the single most important constraint on this slide.
- If a panel feels like it needs a number that is not in the appendix, write the qualitative
  claim instead, or label the panel "proposed — not yet measured".
- No placeholder or lorem text anywhere.

This project is graded on real-vs-invented being unambiguous.

## THE ONE THING NOT TO DO ON THIS SLIDE

Do **not** build a competitor comparison table — no grid of Blinkit vs Zepto vs Instamart vs
BigBasket scored on "discovery experience", "assortment strength", "personalisation quality" or
anything similar.

We have **no researched competitor data**. The review corpus behind this project contains no
competitor evidence, and the only competitor datapoint in the entire project is a **single survey
respondent** who moved to Zepto. A four-platform grid built on that would be fabrication, and it
would undo the credibility the rest of the deck is built on.

Competitive pressure belongs on this slide as a **named, honestly-sized risk** — see the appendix —
not as a scored comparison.

## Hard output constraints (these are graded)

- ONE slide, 16:9, to sit as slide 2 of 10.
- The fellow's name must appear NOWHERE.
- Minimum font size 14pt equivalent — nothing smaller, including footnotes, captions and table
  cells. Do not solve density problems by shrinking type; cut content instead.
- Colour-blind safe. Never encode meaning in red/green alone; always pair colour with a word or icon.
- All body text readable against its background; check contrast on any dark panel.
- Dense but not cramped. Assume a reader scanning on a laptop. **4 panels maximum** — this slide
  is currently at risk of over-stuffing.

## Slide title must be an assertion, not a label

State the finding as a full sentence. "Business opportunity" is wrong. Something in the shape of
"Blinkit's own growth plan runs through the behaviour we're fixing" is right. Put a small
letterspaced uppercase eyebrow above the title naming the section.

## Visual system (match exactly)

- Brand: Blinkit yellow `#F8CD1B` as the single accent, near-black ink `#16130A`, warm off-white
  page `#F4F5F3`, white cards `#FFFFFF` with a 1px `#E7E8E2` border and ~20px radius.
- One dark panel (`#16130A`, light text) is appropriate on this slide for the hero stat. Only one.
- Typeface: Plus Jakarta Sans (or a similar geometric sans), weights 400/600/800.
- Layout: 2–3 column grid. Small tables with a filled header row are fine.
- Hero stats: very large numeral, short label beneath, source line under that.
- Green `#146634` for "confirmed/positive", amber `#7A6100` for "caveat" — always with a word.
- No emoji as section markers. No gradient hero. No centered-everything.

## What this slide must contain

Four panels, in this priority order:

1. **The hero stat — the scale of the behaviour.** In the project's own review corpus, category
   *avoidance* outnumbers successful new-category *trials* by roughly **44 to 1** (842 vs 19).
   Make this the hero number in the dark panel. It is the strongest single argument that the
   opportunity is real, and it comes from the largest dataset in the project. Show the two raw
   counts alongside the ratio so it is auditable.

2. **The size of the prize.** Blinkit's own scale, so the reader can see what even a small shift
   in this behaviour is worth. Use the Q1 FY27 figures in the appendix. Do not compute a revenue
   opportunity from them — state the scale and let it speak.

3. **The company's own strategic commitment.** Assortment expansion is one of three long-term
   growth pillars named by Blinkit's CEO, and an analyst on the earnings call framed the growth
   narrative as depending on non-grocery assortment. This is the strongest business argument in
   the deck: the company is already saying this problem matters, in its own words.

4. **What it costs if unsolved — honestly sized.** Users who hit friction don't only narrow their
   basket; at least one left for a competitor entirely. Present this as a **risk worth tracking,
   explicitly n=1**, and immediately pair it with the counter-signal: Eternal's own retention
   cohorts are improving. Showing the risk *and* the evidence against it being systemic is more
   credible than showing either alone — do not drop the counter-signal to make the risk look bigger.

## Tone

Confident, specific, and candid about limits. The strongest thing about this project is that it
says what it does not know. Preserve that — do not smooth the caveats away. A caveat rendered as a
small labelled amber note is better than a caveat deleted.

---

# DATA APPENDIX — the only material you may use on this slide

## The hero stat (real, database-backed)

From 1,094 gate-passing extractions over 15,820 public reviews:

| Behaviour extracted | Count |
|---|---|
| Category avoidance | **842** |
| Successful new-category trial | **19** |

Ratio: **~44:1**. Source line to use: *"1,094 gate-passing extractions from 15,820 public reviews."*

## Blinkit scale — Eternal Q1 FY27 (quarter ended 30 June 2026)

These figures already appear on slide 1, so keep the framing consistent.

- **31.8M** average monthly transacting customers (**16.9M** a year earlier)
- **331M** orders in the quarter (**≈10.4** orders per customer)
- **2,443** dark stores live (**+200** in the quarter)
- **86%** YoY net order value growth · **₹17,132 cr** NOV

Source line: *"Blinkit segment, Eternal Q1 FY27 shareholders' letter and earnings call."*

## Company statements (real, verbatim — do not paraphrase into new claims)

CEO Albinder Dhindsa, Q1 FY27 shareholders' letter:
> "We continue to focus our efforts on our three pillars of long-term growth — assortment
> expansion, geographical expansion, and demand densification."

Analyst (Bernstein), Eternal Q4 FY26 earnings call, 28 Apr 2026:
> "a large part of our growth narrative from here on depends in some sense on either growing the
> non-grocery assortment and going outside of the metro cities."

CFO Akshant Goyal, Q4 FY26 earnings call:
> "It's a function of assortment expansion, geographical expansion as well as more demand
> densification in the cities where we are present today."

## The competitive risk (real, but tiny — size it honestly)

- One survey respondent stopped using Blinkit for some purchases after a damaged order that was
  fully refunded: *"I have started using Zepto more."* **This is n=1.** Label it as a risk to
  track, never as a trend, and never as a market-share claim.
- **Required counter-signal, must appear beside it:** Eternal reports customer retention cohorts
  *improving* — Q4 average **46%**, most recent cohort **50%**. Churn does not appear to be a
  broad systemic problem in the company's own aggregate data.

## Things you must NOT put on this slide

- Any competitor comparison table, scorecard, or rating of any platform on any dimension.
- Any market-share, competitor revenue, competitor user-count or competitor category-count figure.
- The **"1.8% of NOV" inventory-loss figure.** It is real but hand-transcribed and not
  reproducible from the project repo, so it is deliberately excluded from the entire deck.
- The **58%** survey figure — it is moving to Slide 5. It must not appear on this slide.
- Any computed revenue opportunity, TAM, or "if we lift X by Y%" arithmetic. No such modelling
  has been done.
- Any A/B lift, conversion rate or experiment result. No experiment has been run.
