# Figma AI (First Draft / Make) prompt — 10-slide deck

Paste the block below into Figma's AI generation panel. Figma AI generates from
text only — it can't reach local files, so it will fill image slots with
placeholder imagery. After generation, manually swap in the real assets:
`deck/design/img/blinkit-logo.png`, the 4 real product screenshots
(`disc-01/02/04-*.png`, `mvp-02/03/04/07-*.png`), and the 5 new mood images
(`5l5k5qipEBWBOlqwbi2Gt.png`, `ImJ8MvyrLf8DFIGo7wDNS.png`,
`K3IxluDXz3Vxs_eAll-Sb.png`, `MSP32PKwJEu1inRgjgB06.png`,
`qpOds-FcDInIdeVSfjxA7.jpg`) per the placements noted on slides 1, 2, 4, 6, 7.

**Minimum font sizes by tool, at a 1920x1080 frame — carry these forward
whenever this content gets adapted to a different tool:**
- Figma: 26px minimum (used below, since this prompt targets Figma)
- Google Slides / PowerPoint: 14pt minimum
- Canva: 22px minimum

---

```
Design a 10-slide widescreen (16:9, 1920x1080) product case-study deck called
"Why do Blinkit's most loyal users never widen their basket?" — a quick-commerce
UX research and MVP case study. Editorial, data-dense, minimal style: think a
Stripe or Linear-style deck, NOT a marketing/pitch deck. No stock photography
in the base system — data cards, tables, real screenshots and a small set of
illustrative accent images only (noted per-slide below).

DESIGN SYSTEM (apply to every slide):
- Canvas: 1920x1080, background #F4F5F3 (flat, no gradients except slide 1's
  soft radial glow noted below)
- Font: Plus Jakarta Sans, weights 400/600/800
- Ink/text: #16130A. Body copy on white cards: #3A3628. Muted/caption text: #5A5545
- Accent yellow: #F8CD1B (primary brand accent, chips, highlights, CTA borders)
- Amber label color: #7A6100 (small uppercase eyebrow labels, section tags)
- Brand green: #318616 for graphic elements (donut rings, bars); #146634 for
  small green text (better contrast)
- Dark panel color: #16130A background with #F4F5F3 text, #F8CD1B accent text,
  #DAD8CE body text, #C9C7BC muted text — used for "chosen answer" / key-stat /
  synthesis panels, not every slide
- Tinted cards: light green #EDF5E9 + 1px border #CFE3C6 for "confirmed/positive"
  content; light yellow #FFF9DF + 1px border #F8CD1B or #F0DFA0 for
  "highlight/chosen" content; plain white + 1px #E7E8E2 border, 20px corner
  radius for neutral data cards
- Every slide (except slide 1) gets a small header row: a small Blinkit
  wordmark logo (use a placeholder wordmark reading "blinkit" in the brand's
  yellow/green/red multicolor lettering) at ~104px wide, a thin 1px vertical
  divider, then a small uppercase amber eyebrow label (e.g. "Part 1 · how the
  engine works")
- Each slide has a bold assertion-style H2 title (not a topic label) at
  ~46-58px, weight 800, tight letter-spacing
- Photographic/illustrative images (only on slides 1, 2, 4, 6, 7 — noted below)
  are framed identically: 1px #E7E8E2 border, 14px corner radius, soft drop
  shadow, contained in a small-to-medium panel — never full-bleed, never
  recolored
- STRICT MINIMUM FONT SIZE: 26px, with zero exceptions — this applies to every
  single piece of rendered text on every slide, including table cells, chips,
  footnotes, source citations, axis labels and single-character glyphs. Do not
  let any text node fall below 26px even for "decorative" or "minor" text.
  This deck targets a 1920x1080 Figma frame, where 26px is the enforced floor.

---

SLIDE 1 — Title
Background: #F4F5F3 with a soft warm-yellow radial glow in the top-right
corner (this is the ONLY gradient in the whole deck).
Top: Blinkit wordmark logo (~212px wide), a small yellow rounded bar + uppercase
label "Product case study · Blinkit · quick commerce".
Large H1 (~62px): "Why do Blinkit's most loyal users never widen their basket?"
Subhead paragraph: "Four parts: an AI discovery engine over public reviews,
primary user research, a problem definition, and a deployed AI-native MVP —
the Category Nudge Agent."
Below, a 2-column row of cards:
- Left, dark panel "The customer base we are designing into" with a 4-column
  stat grid: 31.8M avg. monthly transacting customers (16.9M a year earlier) ·
  331M orders in the quarter (~10.4 per customer) · 2,443 dark stores live
  (+200 in the quarter) · 86% YoY net order value growth (₹17,132 cr NOV).
  Small footnote citing "Blinkit segment, Eternal Q1 FY27 shareholders' letter
  and earnings call."
- Right, white card "Discovery on Blinkit today" — 3 numbered mini-rows
  (Intent-led search and category aisles / Home rails tuned to place and time /
  Complement prompts at cart), each with a short 1-2 line description, followed
  by a yellow-tinted callout: "The gap this study works in: every surface above
  ranks what to buy inside a category the customer already trusts. None of
  them argue why to try a category a bad order taught them to avoid."
Illustration placement: tuck a small framed illustration of a woman holding a
phone showing a grocery-delivery app, surrounded by a basket of fresh produce,
into a corner or as a third small element alongside the two stat cards — keep
it small, do not let it crowd the stat grid.

---

SLIDE 2 — Why it matters
Eyebrow: "The goal, framed". H2: "Heavy repeat buyers keep narrow baskets —
and most of them say so themselves."
Layout: 2-column grid.
Left: a dark panel with a huge yellow numeral "58%" and caption "of surveyed
users self-report that they mostly stick to the same categories" (source:
primary survey, 18 of 31 responses).
Right, stacked white cards:
- "This is a trust problem, not an awareness problem" — short paragraph about
  repeat customers already having seen other categories.
- "The company's own growth path runs through this behaviour" — two quoted
  lines from an Eternal earnings call about assortment/geographic expansion,
  with a small "Caveat" note that the call doesn't discuss quality/refund
  friction directly.
Illustration placement: a small framed illustration of a person in a kitchen
reading product reviews on their phone (deciding whether to trust a product
based on reviews/ratings) — place it inside or beside the "trust problem, not
awareness" card as a supporting visual.

---

SLIDE 3 — Discovery engine (no illustration — real screenshots only)
Eyebrow: "Part 1 · how the engine works". H2: "A five-stage pipeline hard-gates
on category-adoption relevance before it extracts anything."
Top-right: a small yellow-outlined pill link "Open the live extractor →".
A horizontal stat band: 15,820 public reviews ingested → 4,740 pass the
rule-based prefilter → 1,094 gate-passing extractions (highlighted in yellow),
plus a short "Why gate at all?" explanation alongside.
Below: 5 numbered step cards in a row (Ingest · Heuristic prefilter · Gated
extraction [dark/highlighted] · Deterministic clustering · LLM-judge
validation), each with a small icon badge, a stat line, and 2-3 check-marked
bullets.
Bottom: two screenshot placeholders side by side (a "kept" review example
labeled green-check "Kept — category behaviour" and a "dropped" example
labeled "Dropped — service complaint"), plus a right-hand column with a
yellow "Design decision · the gate" callout and a green "What the engine
measures" callout.

---

SLIDE 4 — Review findings
Eyebrow: "Part 1 · what the reviews said". H2: "Poor quality and unreliable
products is the dominant reason customers stop widening their baskets."
Layout: left 2x2 grid of white insight cards, right column a tall screenshot
placeholder labeled "Results Explorer".
Insight cards: (1) "One theme carries the segment" — big green "70%" stat;
(2) "The steep funnel is the gate working, not data loss" — restates
15,820 → 4,740 → 1,094; (3) "Where the top theme lands" — a horizontal bar
chart: Groceries 431, Electronics 96, Snacks & beverages 79, Household
essentials 39, Personal care 27; (4) green-tinted "Every count is a database
row" — explains frequencies are real pipeline exports, not LLM estimates.
Bottom: a full-width dark banner "The core problem" — "Customers are not
missing the other categories — they have decided those categories are unsafe
to buy here. One damaged, expired or fake item is read as evidence about the
whole category."
Illustration placement: a small framed funnel/data-conversion infographic
illustration placed as a compact accent next to insight card (2) — it should
support/echo the 15,820→4,740→1,094 numbers already in that card, not act as
a second full chart.

---

SLIDE 5 — Research confirmed & challenged (no illustration)
Eyebrow: "Part 2 · primary research". H2: "The survey confirmed the AI's cause
— and challenged how far it reaches."
Top-right: small white card "Sample, stated honestly" noting 31 survey
responses, no live interviews.
3-column layout:
- Left, white card "Quantitative validation": 3 small donut-ring stats (58%
  stick to same categories 18/31, 48% had a bad order in 3 months 15/31, 73%
  of those fully refunded 11/15), plus a segmented bar showing 11 agree / 9
  neutral / 11 disagree to "does a bad experience make you hesitant to try
  others" (mean 3.0/5).
- Middle, dark panel "What the survey challenged": 4 short findings — the
  behaviour change is an even 7/7/1 split not a rule; half the "stuck" group
  (8 of 18) had no incident at all; some customers churn to competitors
  instead of narrowing; packaging is a distinct sub-cause (fulfilment, not
  sourcing).
- Right, white card "Confirmed, in their words": 3 green-tinted verbatim
  quote blocks about avoiding categories after bad experiences, each
  attributed to an incident type (unresolved complaint / damaged electronics
  / expired dairy).
Bottom: full-width yellow "The verdict" banner: "Confirmed: a quality failure
does generalise into avoiding the whole category. Challenged: it does not do
so for everyone — so the fix is scoped to the trust-driven share, not all
stagnation."

---

SLIDE 6 — Problem framing canvas
Eyebrow: "Part 3 · problem framing canvas". H2: "One quality failure
generalises into permanent avoidance of an entire category."
Layout: 3x2 grid of cards, each with a small numbered uppercase eyebrow and a
bold sub-header:
01 · Who it's for — "Heavy, habitual repeat buyers."
02 · The root cause — "Trust, not discovery."
03 · How they cope today — "Two workarounds, both costly." (retreat to
essentials, or switch platforms)
04 · Why it's worth it for the user (green-tinted) — "They want to
consolidate — they just can't risk it." (27 of 31 named a concrete change
that would help; refund guarantee 13 picks, quality signal 10)
05 · Why it's worth it for the business (green-tinted) — "Basket width is the
growth lever the company has named."
06 · Scope limit, stated up front (dark panel) — "This addresses only the
quality- and trust-driven share of stagnation."
Bottom: a thin yellow evidence-base strip citing 1,094 gate-passing
extractions (70% quality-driven) and 31 survey responses.
Illustration placement: a small framed illustration of a family unpacking
fresh groceries at home — place it supporting the "why it's worth it for the
user" card (04), reinforcing the repeat-household-use theme, without
crowding the other 5 cards.

---

SLIDE 7 — Why trust, not discount
Eyebrow: "Part 4 · solution choice". H2: "A trust-led nudge wins because it
answers the blocker customers actually named."
Layout: 2-column, left wider.
Left: white card "Options considered" with a 4-column comparison table
(dark header row) of 4 rows: Discount/intro offer (fails both criteria) ·
Better merchandising (fails both) · Let users inspect before delivery
(partial on both) · Trust-led category nudge — chosen, highlighted yellow row
(passes both: solves refund certainty 13/31 + quality 10/31, differentiated
per-user). Footnote citing the full ranked Q15 driver list (refund 13,
quality 10, inspect 7, reviews 5, offers 5, nothing 4, human support 3,
packaging 1 write-in).
Right: a dark "Chosen solution" panel — "The Category Nudge Agent" — a nudge
that leads with the refund guarantee, then quality/freshness, in ranked
order — plus a short "Why not a discount" note (a discount pays someone to
repeat the experience that broke their trust).
Illustration placement: a small framed illustration of a retail/service
employee holding a "trust/quality guaranteed" shield icon with refund-
guarantee messaging — place it inside or beside the dark "Chosen solution"
panel as a compact supporting visual; this slide is tight on space so keep
the image small and don't let panel text wrap.

---

SLIDE 8 — The MVP, running (no illustration — real product screenshots only)
Eyebrow: "Part 4 · the MVP, deployed", plus a bold "Open the live agent →"
link. H2: "The agent runs today: a shopper-facing nudge, its reasoning, and
the push queue behind it." Top-right: small white card "Data disclosure — 8
synthetic user profiles, labelled SYNTHETIC in the product UI itself."
Layout: a horizontal filmstrip of 3 tall phone-screenshot placeholders
(labeled "Phone nudge," "Agent reasoning panel," "Lock-screen push queue"),
with small annotation callouts pointing to each: "Leads with the two
research-ranked trust drivers," "Deterministic ranker, integer weights — not
model confidence," "Copy generated live per user, not templated," "Five
users, four different categories — no collapse to one suggestion."

---

SLIDE 9 — How it works / breaks (no illustration)
Eyebrow: "Part 4 · architecture and limits". H2: "Deterministic logic decides
what to nudge; the LLM only writes the words."
Layout: left, a tall screenshot placeholder labeled "Reasoning panel — user
flagged out of primary scope" with a caption about an amber banner telling a
low-intent user the trust fix isn't theirs. Right column: a "Runtime flow"
stack of 5 rows (Input → Rule-based friction match → Rule-based adjacency
ranker → LLM nudge generation [dark, highlighted] → Output), a yellow "Two
integrity rules" callout (never invent statistics; never overclaim to
low-intent users), and a white "Where it breaks" card listing 4 honest
limitations (synthetic profiles, refund-promise fulfilment risk, packaging
needs an ops fix not a message, platform-switchers may never see the nudge).

---

SLIDE 10 — Measurement plan (no illustration)
Eyebrow: "Measurement · proposed, not yet measured". H2: "We would judge this
on new-category adoption, in three tiers, with trust guardrails." Top-right:
a solid yellow card stating plainly "Plan only. No experiment has been run...
so no result numbers appear on this slide."
Layout: left column — a dark "Primary metric" panel (% of monthly active
customers who purchase from at least one new category that month) and a white
"Honest scope limit" card. Right column — a "Measurement ladder" table (3
rows: Outcome / Mechanism / Durability, each with what's watched and what it
means) and a "Guardrails" 2x2 grid (return/refund rate must not rise,
complaint rate, order frequency/nudge fatigue, copy audit for invented
stats). Bottom: a 3-column "What we'd build next" row (inspect-before-
accepting / a relevance-led nudge for the low-intent half / real
behavioural data instead of synthetic profiles).

Keep every slide's information density high but organized — this is a
graded case-study deck, not a sales pitch, so favor clear data hierarchy
over decorative whitespace.
```
*.makeproxy-c.figma.site