# Claude Design prompt — the 10-slide Blinkit deck

Copy everything inside the fenced block below into Claude Design Labs as a single prompt.
It is deliberately long: **every real number is embedded in it**, because the three
previous Claude Design imports on this project all shipped invented figures (fabricated
A/B lifts, fake confidence scores, invented pricing) that had to be stripped out by hand.
A prompt that does not carry the data will hallucinate the data.

Reference for the visual density/structure: the NL Spotify case-study deck (10 slides,
assertion-led titles, 3–4 column layouts, dark emphasis panels, hero stat blocks).

---

```
You are designing a 10-slide product case-study deck as a set of 16:9 HTML slides.

## Subject
A PM fellowship graduation project on Blinkit (Indian quick-commerce). The strategic goal:
increase the % of Monthly Active Customers who purchase from at least one NEW category each
month. Four parts: (1) an AI discovery engine over 15,820 public reviews, (2) primary user
research, (3) problem definition, (4) a deployed AI-native MVP called the Category Nudge Agent.

## ABSOLUTE RULE — invent nothing
Every number, quote, theme name and label you may use is listed in the DATA APPENDIX at the
end of this prompt. Use ONLY those.
- Do NOT invent conversion rates, A/B lifts, p-values, sample sizes, confidence scores,
  funnel percentages, revenue figures, prices, or user counts.
- Do NOT invent persona names, quotes, or company statements.
- If a slide feels like it needs a number that is not in the appendix, write the qualitative
  claim instead, or label the panel "proposed — not yet measured".
- Placeholder/lorem text is not acceptable anywhere.
This project's grading depends on real-vs-invented being unambiguous.

## Hard output constraints (these are graded)
- EXACTLY 10 slides. A title slide, if used, counts as one of the 10. No appendix slide.
- The fellow's name must appear NOWHERE.
- Minimum font size 14pt equivalent — nothing smaller, including footnotes and table cells.
- Colour-blind safe. Never encode meaning in red/green alone; pair colour with a label or icon.
- All body text must be readable against its background (check contrast on dark panels).
- 16:9. Dense but not cramped; assume the reader is scanning on a laptop.

## Slide titles are assertions, not labels
Every slide title must state the finding as a full sentence. "Problem" is wrong.
"Loyal buyers stop exploring after one bad order" is right. Put a small letterspaced
uppercase eyebrow above or below each title naming the section.

## Visual system
- Brand: Blinkit yellow #F8CD1B as the single accent, near-black ink #16130A, warm off-white
  page #F4F5F3, white cards #FFFFFF with a 1px #E7E8E2 border and ~20px radius.
- Use a dark panel (#16130A, light text) once or twice per deck for emphasis — hero stats,
  core insights, guardrails. Do not make every slide dark.
- Typeface: Plus Jakarta Sans (or a similar geometric sans) throughout. Weights 400/600/800.
- Layout: 2–4 column grids. Small tables with a filled header row are encouraged.
- Hero stats: very large numeral, short label beneath, source line under that.
- Green #146634 for "confirmed/positive", amber #7A6100 for "caveat", but ALWAYS with a word.
- No emoji as section markers. No gradient hero. No centered-everything.

## The 10 slides

1. TITLE + THE GOAL. The metric being moved, the four-part approach in one line, and the two
   live links. Keep it sparse — this is the only sparse slide.

2. WHY CATEGORY STAGNATION IS THE PROBLEM WORTH SOLVING. Frame the goal: heavy repeat buyers
   with narrow baskets. Include the segment size stat (58% of surveyed users self-report
   sticking to the same categories). Set up that this is a trust problem, not an awareness one.

3. THE AI DISCOVERY ENGINE — HOW IT WORKS. This slide must carry the workflow explanation
   (it is a required deliverable, so fold it in here rather than a separate appendix slide).
   Show the 5-stage pipeline as a left-to-right strip: Ingest → Heuristic prefilter →
   Two-Step Gated extraction (LLM) → Deterministic clustering → LLM-judge validation.
   Add a panel "what the engine measures" and the live workflow link.
   Call out the design decision: the relevance GATE. Explain that an early ungated run only
   surfaced generic service complaints, so extraction now hard-gates on category-adoption
   relevance before extracting anything.

4. WHAT 15,820 REVIEWS SAID. The funnel (15,820 → 4,740 → 1,094) as three shrinking blocks,
   the ranked themes with their evidence counts, the source mix, and the validation result.
   Make the 70% top theme the hero number. Include the honest note that the steep funnel is
   the gate working, not data loss.

5. USER RESEARCH CONFIRMED *AND* CHALLENGED THE AI (this slide is mandatory — it must show
   both). Two columns: CONFIRMED (3 verbatim quotes) vs CHALLENGED (the even 6/6 split, the
   competitor-switching case, the no-incident stuck users, the packaging sub-cause).
   State the sample honestly: 31 survey responses, no live interviews.

6. PROBLEM FRAMING CANVAS. Five numbered boxes: (1) the true problem, (2) who it's for,
   (3) how we know, (4) what value solving it creates, (5) why now. Mirror the density of a
   classic framing canvas — short bold lead-ins, then 1–2 lines each.

7. WHY A TRUST-LED NUDGE, NOT A DISCOUNT. Show the solution options considered and why the
   chosen one wins — a small comparison table (option / pain solved / whole segment? /
   differentiated?) plus a "chosen solution" panel. Ground it in the ranked survey drivers:
   refund guarantee first, quality/freshness signal second.

8. THE MVP, RUNNING. Annotated screenshots of the deployed Category Nudge Agent: the operator
   console, the phone nudge, the auto-nudge queue, the checkout cart-filler. Callout labels
   pointing at: deterministic friction matching (no LLM), live LLM nudge generation, the
   ranked candidate panel, the honest out-of-scope path. Include the live MVP link.
   Leave four clearly-marked image placeholders sized for phone/console screenshots.

9. HOW IT WORKS + WHERE IT BREAKS. The runtime flow (profile → deterministic friction match →
   deterministic adjacency ranker → LLM nudge generation → rendered nudge), the key properties,
   and an edge-cases panel. Emphasise the two integrity rules: the agent may never invent
   statistics in its copy, and low-intent users are told the trust fix does not apply to them.

10. HOW WE'D KNOW IT WORKED. The primary metric (% MAU purchasing from ≥1 new category that
    month), a tiered measurement ladder, guardrails, and the honest scope limit — this only
    addresses the trust-driven share of stagnation, not the low-intent share.
    Label the whole slide as a plan: no experiment has been run, so show NO result numbers.

## Tone
Confident, specific, and candid about limits. The strongest thing about this project is that
it says what it does not know. Preserve that — do not smooth the caveats away.

---

# DATA APPENDIX — the only numbers you may use

## Part 1 — discovery engine (all DB-backed, real)
- 15,820 raw reviews ingested (deduplicated).
- Source mix: Play Store 8,058 · Google Maps 4,098 · source-not-recorded 2,532 ·
  App Store 530 · MouthShut 520 · ConsumerComplaints.in 76.
  ("source not recorded" = real scraped reviews whose originating platform was never captured.
  There are also 6 mock reddit rows which are EXCLUDED from all displays — do not show them.)
- Heuristic prefilter → 4,740 reviews. It drops: empty text (2,254), under 5 words (7,006),
  and 5-star reviews (1,820).
- Two-Step Gated LLM extraction → 1,094 gate-passing extractions (~23% of 4,740).
- Ranked themes (deterministic DB row counts, never LLM-estimated):
  1. "Poor Quality and Unreliable Products" — 770 of 1,094 (70%)
  2. "Convenience and Price Sensitivity" — 114 (10%)
  3. "Discovery Friction and Limited Options" — 78 (7%)
- Behaviour split among gate-passing: category_avoidance 842 · repeat_purchase 124 ·
  discovery_friction 101 · new_category_trial 19.
- Top theme spans categories roughly proportional to volume: groceries 431 · electronics 96 ·
  snacks & beverages 79 · household essentials 39 · personal care 27.
- LLM-judge validation on a held-out theme-relevant sample: 16 of 20 confirmed, 4 unclear,
  0 contradicted (80%).
- Models: Groq llama-3.1-8b-instant for extraction/clustering/validation;
  llama-3.3-70b-versatile for the Part 4 agent. (Not Gemini, not OpenAI.)

## Part 2 — primary research (real, N=31 survey; ZERO live interviews)
- 31 survey responses. Be explicit that live interviews were not conducted.
- 18/31 (58%) self-report "mostly stick to the same categories" — the target segment.
- 15/31 (48%) had a bad order in the last 3 months.
  Failure types: 11 damaged · 2 expired · 1 fake/duplicate · 1 other.
  Resolution: 11 full refunds · 3 replacements · 1 unresolved.
- Behaviour-change split among the 15: 7 confirmed a change, 7 reported no change, 1 ambiguous.
- 8 of the 18 "stuck" respondents had NO incident at all — stagnation there is low intent.
- Q14 ("a bad experience in one category makes me more hesitant to try others", 1-5):
  mean 3.0 — 11/31 agree (4-5), 11/31 disagree (1-2), 9 neutral. A rated echo of the same split.
- Ranked confidence drivers (Q15, "what would make you try a new category", pick up to 2):
  "No questions asked" refund/return guarantee 13 · Better visible quality/freshness
  guarantees 10 · Inspect before accepting delivery 7 · Item reviews/ratings 5 ·
  Intro offers 5 · Nothing in particular 4 · Human support agent 3 ·
  Safer packaging for fragile items 1 (free-text write-in).
  NOTE: inspect-before-accepting is now the clear THIRD driver (it was tied-third at N=25).
  Item reviews/ratings is now tied FOURTH — do not label it third on any slide.
- 2 respondents raised pricing vs competitors unprompted.
- Verbatim quotes you may use (do not alter):
  - "I have stopped exploring new categories on Blinkit. I only order the essential items now
    if anything urgent." (unresolved puja-item complaint)
  - "yes I am skeptical of buying electronic products from Blinkit and other similar
    applications" (damaged electronics)
  - "I avoid buying any fresh products dairy or perishables items from quick commerce apps."
    (expired dairy — generalised to the whole category, not just Blinkit)
  - "I have started using Zepto more" (platform switching instead of category avoidance)
  - "often packed at the bottom of the bag under heavier groceries" (packaging/fulfilment
    failure — a distinct sub-cause from product-source quality)
  - "Nothing in particular — I just don't need those categories" (low-intent, no incident)

## Part 3 — problem statement
- Target segment: heavy, habitual repeat buyers who default to existing categories.
- Root cause: a quality/reliability failure (damaged, expired, fake) generalises into
  category avoidance — or, for some, into leaving the platform entirely.
- Existing workarounds: retreat to "essentials only", or switch platform (Zepto).
- HONEST SCOPE LIMIT, must appear on the deck: this addresses only the ~50% of category
  stagnation that is quality/trust-driven. The low-intent half will not move on this nudge.

## Part 4 — the MVP (Category Nudge Agent, deployed)
- 8 synthetic user profiles, explicitly labelled SYNTHETIC (no real customer data was
  available; this is stated in the product UI itself).
- Deterministic friction-matching layer (rule-based, no LLM) maps a profile to a Part 1 theme.
- Deterministic adjacency ranker produces the candidate new-category list (integer weights).
- Live Groq call generates the nudge copy + reasoning per user.
- Nudge leads with the two top-ranked survey drivers: refund guarantee, then quality/freshness.
- Three surfaces: operator console · auto-nudge queue · checkout cart-filler.
- Auto-nudge eligibility gate: cadence is Daily or Weekly AND tenure > 6 months →
  5 of the 8 synthetic profiles qualify.
- Cart-filler: free-delivery threshold ₹199 and delivery fee ₹35 are ILLUSTRATIVE demo
  constants — label them as such if shown.
- Integrity rules enforced in the agent's prompt: it may never invent statistics, ratings or
  buyer counts in nudge copy; and for a low-intent user with no incident it must say the trust
  fix does not apply rather than overclaim.

## Live links (both public, must appear in the deck)
- Discovery workflow: https://huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine
- Deployed MVP: https://huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent
(If the deck must not reveal the account name, put these behind shortened links.)

## Things you must NOT put on the deck
- Any A/B test result, conversion rate, uplift %, or p-value — no experiment has been run.
- Any live-usage funnel or outcome metric — the MVP has never been shipped to real users.
- Any per-user confidence score — the only defensible "confidence" figure is the real theme
  evidence share (770/1,094 = 70%).
- Any product pricing presented as real Blinkit pricing.
- The Eternal "1.8% of NOV inventory losses" figure. DECIDED 2026-07-24: omitted, unverified.

## The company corroboration you MAY use (real, DB-backed, live in the discovery app)
From Eternal's Q4 FY26 earnings call (28 Apr 2026):
- Analyst: "a large part of our growth narrative from here on depends in some sense on either
  growing the non-grocery assortment and going outside of the metro cities."
- CFO: "It's a function of assortment expansion, geographical expansion as well as more demand
  densification in the cities where we are present today."
Use these to make the business case: the company's own stated growth path depends on customers
widening into non-grocery categories — which is exactly the behaviour this project unblocks.
Also state the honest gap: the call does NOT directly discuss product-quality or refund friction.
```

---

## Two things to fix while you're in there

**1. Your current deck is 11 slides; the PRD limit is 10 (hard).** The prompt above solves it
the way the Spotify deck does — the workflow explainer is folded into slide 3 rather than
living as a separate appendix slide.

**2. The `1.8% of NOV` figure — DECIDED 2026-07-24: omitted.** It had no source document in the
repo and was never run into the database, so it was not reproducible. `deck_spec.md` and
`deck_outline.md` Slide 4 / Slide 7 now use the **Q4 FY26 assortment-expansion commentary**
instead, which is DB-backed and rendered live in the discovery app. The figure still appears in
`problem_statement.md` §5 and in `analyze_concalls.py` — those are Part 3 / pipeline artifacts,
not deck inputs, and are left untouched pending a separate decision.

---

# Prompt 2 — placing the screenshots

Paste this as a **follow-up prompt** once the 10 slides exist (or append it to Prompt 1 if you
want the frames laid out from the start). The screenshots live in `deck/screenshots/` — upload
them to Design Labs if it accepts images, otherwise the prompt below builds correctly-sized
empty frames with the filename printed inside, and you drop the real files in afterwards.

```
Add the product screenshots to the deck. They are real captures of two deployed apps, so they
are the proof the work exists — give them room, don't shrink them into thumbnails.

## How to place them
For each image below I give a FILENAME and an ASPECT RATIO (width ÷ height). Build a frame at
exactly that ratio. If you cannot embed the image itself, render an empty placeholder frame
with a 2px dashed #C4C5B9 border, the filename centred inside in 14pt monospace, and the ratio
beneath it — so the frame can be filled later without the layout shifting.

Never letterbox, never stretch, never crop a placeholder to a different ratio than stated.

## Critical layout warning
Three of these are FULL-PAGE captures with a very tall 0.61 ratio. On a 16:9 slide a
0.61-ratio image at full slide height fills only about a third of the width. So:
- Use the CROPPED images (ratios 0.36–1.09) as the primary visuals.
- Use a full-page 0.61 image ONLY as a narrow side column, or crop it to its top ~45%
  (which contains the profile card and the generated nudge) and treat it as ~1.1 ratio.
- Never place a 0.61 image as a slide's main hero — it will read as a sliver.

## Slide 3 — the discovery engine
Two frames side by side, equal size, with a bold label above each:
- LEFT · label "KEPT — category behaviour" · `disc-01-extractor-pass.png` · ratio 1.25
- RIGHT · label "DROPPED — service complaint" · `disc-02-extractor-reject.png` · ratio 1.25
Beneath both, one line: "Same engine, same review box — the gate is the difference."
This pairing IS the slide's argument; give the two frames at least half the slide.

## Slide 4 — what the reviews said
One frame, right two-thirds of the slide:
- `disc-04-results-explorer.png` · ratio 0.91
Left third carries the funnel numbers and the top-theme stat as text. Do not duplicate in text
any number that is already legible inside the screenshot.

## Slide 8 — the MVP, running (the annotated slide)
This is the deck's centrepiece. Model it on an annotated product teardown: screenshots in the
middle, small callout boxes around them, thin leader lines pointing from each callout to the
part of the UI it describes.

Frames:
- `mvp-02-phone-nudge.png` · ratio 0.41 · the shopper's view. Place LEFT, full column height.
- `mvp-03-reasoning-ranked.png` · ratio 0.97 · the agent's reasoning. Place CENTRE.
- `mvp-07-lockscreen.png` · ratio 0.36 · push payloads. Place RIGHT, full column height.

Callout boxes (each ≤ 12 words, 14pt, white card with a 1px #E7E8E2 border and a thin leader
line to its target):
- → phone, at the two coloured strips: "Leads with the two research-ranked trust drivers"
- → phone, at the product row: "No invented pricing — labelled illustrative"
- → reasoning card, at the ranked bars: "Deterministic ranker, integer weights — not model confidence"
- → reasoning card, at the footer: "Copy generated live per user, not templated"
- → lock screen: "Five users, four different categories — no collapse to one suggestion"

## Slide 9 — how it works and where it breaks
One frame, left half:
- `mvp-04-out-of-scope.png` · ratio 1.03
Callout pointing at the amber banner: "The product itself says when the fix does NOT apply".
Right half carries the runtime flow and the edge-case list as text.
Treat this image as the emotional centre of the honesty argument — do not shrink it.

## Optional / reserve frames
Use only if a slide looks empty; otherwise leave them out rather than padding:
- `mvp-05-auto-queue.png` · ratio 1.09 · eligibility gate + funnel + queue
- `mvp-08-cart-filler.png` · ratio 1.02 · checkout filler and candidate pool
- `mvp-01-console-full.png` · ratio 0.61 · full console (side column or top-45% crop only)

## Screenshot styling
- Give each frame a 1px #E7E8E2 border, 14px corner radius, and a soft shadow
  (0 8px 24px rgba(0,0,0,.10)). The apps already have their own rounded cards, so keep the
  outer frame restrained.
- Do NOT add browser chrome, fake URL bars, laptop mockups, or drop the images inside a
  stock device frame — the phone shots already contain their own device frame.
- Do NOT recolour, filter, or add gradient overlays to the screenshots.
- Do NOT crop out the "Synthetic demo data" pill or the "Illustrative demo item" label if they
  fall inside a frame — those labels are deliberate and part of the credibility story.

## Caption rule
Every frame gets one 14pt caption beneath it, and each caption must say what the reader is
looking at — never "screenshot of the app". Example: "Live extraction — the gate rejects a
delivery complaint that isn't tied to a category."
```

## After Claude Design returns the slides
Check, in this order: exactly 10 slides · no name anywhere · nothing under 14pt ·
every number traceable to the appendix above · both live links resolve · export under 40MB ·
filename starting "NL Blinkit".
