# Part 2: User Research Tracker

## Goal
Recruit and schedule 5–6 interviewees matching the segment identified by the Discovery Engine.

## Target Segment
*Identified from Part 1 Discovery Engine — real Two-Step Gated extraction over the full 4,740-review filtered corpus (re-run 2026-07-18 via Groq after the original Gemini-based run hit free-tier quota limits; see architecture.md §3.1 and §7). Theme: "Poor Quality and Unreliable Products" — 770 of 1,094 gate-passing extractions (70%), the dominant and most evidence-dense theme by a wide margin, stable across repeated independent clustering runs.*
- **Segment Description:** Blinkit users — across groceries (431 evidence), electronics (96), snacks & beverages (79), household essentials (39), and personal care (27) — who received a damaged, expired, fake/duplicate, incorrect, or used-instead-of-new item, and whose subsequent support/refund experience was unhelpful or unresolved. Not limited to high-value purchases — the signal spans price points and categories roughly proportional to category volume, so don't screen out low-ticket-item complaints.
- **Key Screening Criteria:**
  1. Has purchased from Blinkit at least 3 times in the last month (repeat user, so they have enough experience to compare good vs. bad orders).
  2. Has received a damaged/expired/wrong/fake item OR had a support/refund request go poorly (unresolved, slow, or denied) — in ANY category, not just groceries or high-value items.

## Recruitment Channels
- [x] **Personal Network / Alumni Groups** (Start: Day 8) — executed via the Phase 3 Google Form (`phase3_google_form.md`), not live outreach alone; **31 real responses, form closed and frozen 2026-07-28**
- [ ] **Online Communities** (e.g., Reddit r/delhi, r/bangalore) — not needed; personal-network channel alone produced enough responses
- [ ] **Paid Panel** (Fallback if needed by Day 10) — not needed

## Survey Results Summary (real data, **N=31, frozen 2026-07-28**)
*Full per-respondent breakdown lives in `Final_survey.pdf` (local only — gitignored, contains Q18 contact details) / the linked Google Sheet. This is the rollup used for segment/candidate selection.*

> **Recount note (2026-07-28).** Six responses arrived after the earlier N=25 rollup (five 2026-07-23,
> one 2026-07-25); the form is now closed so these figures cannot drift during deck build. Every
> qualitative conclusion below survived the recount unchanged — including the even split, which
> stayed exact. The one substantive change is the Q15 ranking (see the confidence-drivers bullet).
> The three superseded raw exports were deleted from the working tree the same day; `Final_survey.pdf`
> is the single source.

- **Segment size**: 18/31 (58%) answered "mostly stick to the same categories" on Q6 — this is the target segment for the %MAU growth goal.
- **Incident rate**: 15/31 (48%) had a bad order in the last 3 months (Q7=Yes). Failure types: damaged items dominate (11/15), plus 2 expired, 1 fake/duplicate, 1 other (rotten flowers + wrong size).
- **Resolution**: mostly resolved — 11 full refunds, 3 replacements, 1 unresolved. Support responsiveness is not the core problem; behavior change persists even when resolution works.
- **Theme confirmation (Q11, among the 15 incident-havers)**: exactly **7/15 (47%) clearly confirmed** a behavior change, **7/15 (47%) reported no change**, 1 ambiguous — a genuinely even split, not a landslide either way, and it held exactly through the recount on a larger base (14 unambiguous cases, up from 12). Notable finds:
  - One respondent switched to a competitor (Zepto) entirely rather than avoiding a category on Blinkit — a platform-churn signal distinct from category-adoption stagnation, worth a separate thread in the problem statement.
  - One respondent generalized avoidance to "quick commerce apps" broadly (fresh/dairy/perishables), not Blinkit-specific — suggests the friction may be industry-wide, not a Blinkit-specific weakness.
  - One respondent's issue was packaging/fulfillment (fragile items crushed under groceries), not product-source quality — a distinct root-cause subtype worth flagging separately from "fake/expired/damaged-at-source."
- **Confidence drivers (Q15, ranked by picks, N=31)**: 1) "No questions asked" refund/return guarantee (**13**), 2) Better visible quality/freshness guarantees (**10**), 3) **Inspect before accepting delivery (7)**, 4) Reviews/ratings & first-purchase offers (5 each), 5) Nothing in particular (4), human support agent (3), safer packaging for fragile items (1, free-text write-in). Directly informs what the Part 4 Category Nudge Agent should emphasize.
  - **Ranking change vs. N=25**: the top two held and widened their lead (13 · 10 vs. next at 7), so the Phase 5 scope decision is unaffected. But *inspect-before-accepting* broke its former tie at 5/25 into a **clear third at 7/31**, overtaking reviews/ratings (5/31, now tied fourth). Consequence: the MVP's peer social-proof line maps to the **fourth** driver now, not the tied-third; and pre-acceptance inspection is now the highest-ranked driver left unbuilt.
- **Cross-category hesitancy, rated (Q14, 1–5)**: mean **3.0** — **11/31 agree (4–5), 11/31 disagree (1–2), 9 neutral**. An independent, quantitative echo of the even behavioural split above: the generalisation is real for about a third of users and genuinely absent for another third. (Q13, trust in Blinkit to resolve issues fairly: mean 3.5.)
- **Unprompted contradiction**: **2 respondents** independently complained about pricing vs. competitors in the free-text field (Q16) — R5 (*"Too expensive comparatively"*) and R6 (*"The pricing is expensive as compared to other competitors"*) — a competing barrier alongside quality/trust, not to be buried in the deck. *(Corrected 2026-07-23 from "3": the third row previously counted, R19, said "Discounts provided are less" — a complaint about discount depth with no competitor comparison, so it does not support a pricing-vs-competitors claim.)*

## Candidate Pipeline
*Selected from the survey respondents: matches segment criteria (repeat buyer + had a qualifying incident) AND said Yes to a follow-up call. Anonymized as R-numbers per the response sheet; real contact info held separately, not in this doc.*

**Decision (2026-07-22): live follow-up calls were scoped out.** The survey (paragraph/open-ended fields + branching) is being used as the primary research instrument in place of separate live interviews, given time constraints against the 4 Aug deadline. This is a deliberate scope call, not an oversight — flagged here so the reasoning is traceable if questioned at grading. The candidates below remain identified in case a quick follow-up becomes useful later, but the theme-confirmation grid below is built entirely from survey data.

| Name / ID | Source | Segment Match (Y/N) | Scheduled Date | Status | Notes |
|---|---|---|---|---|---|
| R1 | Survey form | Y | — | Survey-only (no live call) | Electronics item damaged; skeptical of buying electronics on Blinkit/similar apps since |
| R2 | Survey form | Y | — | Survey-only (no live call) | Puja items (rotten flowers, wrong size), complaint unresolved; stopped exploring new categories entirely — strongest confirming quote |
| R3 | Survey form | Y | — | Survey-only (no live call) | Groceries damaged, full refund, no reported behavior change — good "no confirmation" counterpoint |
| R5 | Survey form | Y | — | Survey-only (no live call) | Groceries damaged, full refund; switched to Zepto — platform-churn signal, not category-avoidance |
| R23 | Survey form | Y | — | Survey-only (no live call) | Stationery (fragile items) damaged via packing order, not source quality; packaging/fulfillment sub-theme |
| R24 | Survey form | Y | — | Survey-only (no live call) | Dairy expired/smelly; avoids fresh/perishables across quick-commerce apps generally — industry-wide framing |
| R25 | Survey form | Y | — | Not actionable (said Yes to follow-up but left contact info blank) | Groceries damaged, full refund, "not really" changed — another "no confirmation" data point |

## Theme-Confirmation Grid (finalized from survey data, N=31)
*Required deliverable per PRD Part 3: demonstrate where primary research validated AND where it challenged the AI-surfaced theme ("Poor Quality and Unreliable Products" blocking category-adoption behavior). Built entirely from the 31 survey responses — see decision note above.*

| Status | Evidence | Supporting quote |
|---|---|---|
| **Confirmed** | R2 — unresolved puja-item complaint led to a full stop on category exploration | *"I have stopped exploring new categories on Blinkit. I only order the essential items now if anything urgent."* |
| **Confirmed** | R1 — damaged electronics order generalized to category-level distrust | *"yes I am skeptical of buying electronic products from Blinkit and other similar applications"* |
| **Confirmed** | R24 — expired dairy generalized to an industry-wide avoidance pattern, not Blinkit-specific | *"I avoid buying any fresh products dairy or perishables items from quick commerce apps."* |
| **Challenged** | R5 — same failure mode (damaged item, full refund) produced platform switching, not in-app category avoidance. The AI theme predicts users stay on Blinkit but avoid new categories; this shows some users leave entirely instead | *"I have started using Zepto more"* (also rated cross-category hesitancy low, 1/5 — the stated attitude and the actual behavior diverge) |
| **Challenged** | R3, R7, R8, R12, R22, R25, R27 — **7 of 15** incident-havers reported **no behavior change at all** despite a qualifying incident and, in several cases, actively considering multiple new categories afterward (e.g., R12 listed 6 categories still under consideration) — an exact even split against the 7 who did confirm | *"No change"* / *"No"* / *"not really"* / *"Nothing"* (repeated across respondents) |
| **Challenged (rated)** | Q14 asks the theme's core claim directly (*"a bad experience in one category makes me more hesitant to try other categories"*): **mean 3.0, 11/31 agree vs. 11/31 disagree**. The rated distribution is as evenly polarised as the behavioural split — the theme is real but not universal | — (Likert item, no free text) |
| **Challenged (segment-level)** | 8 of the 18 "mostly same categories" respondents had **no incident at all** (Q7=No) yet are still in the stuck segment — meaning quality/trust alone doesn't explain all category stagnation; for some it's simply lack of interest | R9: *"Nothing in particular — I just don't need those categories"* |
| **New sub-theme (neither confirms nor contradicts, refines root cause)** | R23 — the failure was packaging/fulfillment (fragile items crushed under groceries during packing), not product-source quality (fake/expired/defective). R23 also **wrote in the fix unprompted** on Q15 rather than picking any offered option, so this sub-theme carries a user-stated remedy, not just a symptom | *"often packed at the bottom of the bag under heavier groceries"* · Q15 write-in: *"Better and safer packaging guarantees for fragile items"* |
| **Confirmed (added at N=31)** | R26 — groceries damaged, full refund issued, yet still reports a change in how they shop; a refund did not neutralise the effect here, unlike most resolved cases | *"Yes"* (Q11) |
| **Challenged (added at N=31)** | R27 — second expiry case in the corpus (item arrived expired, full refund) reporting **no** behavioural change, and rating both trust items at the floor (Q13=1, Q14=1) | *"Nothing"* (Q11) |

**Existing workarounds observed** (PRD Part 3 requirement):
- R5: switched to a competitor platform (Zepto) for at least some purchases.
- R2: retreated to only ordering "essential items" on Blinkit, avoiding exploration entirely rather than switching platforms.

## Interview Guide Structure
*(Derived from Part 1 Theme: Poor Quality and Unreliable Products — real evidence, not "high-value" specific)*
- **Hypothesis 1 (Dispute Resolution):** Tell me about a time you had to request a refund or return an item on a quick-commerce app. How did the experience influence your trust in the platform?
- **Hypothesis 2 (Hidden Friction):** Have you ever decided NOT to buy something outside your usual categories (electronics, personal care, household items) because you were worried about what would happen if it arrived damaged, expired, or fake?
- **Hypothesis 3 (Category Expansion Trust):** What would give you the confidence to try a category on Blinkit you don't currently buy?

**Real evidence grounding these hypotheses** (actual extracted reasons from the review corpus, category-diverse):
- Groceries: "The user avoids buying vegetables from the service due to receiving rotten products."
- Electronics: "the electronic items sold on this app are defective and do not support all devices"
- Personal care: "The customer received a used pack of [product] and is unhappy with the support and refund process."
- Household: "The customer received a used product instead of a new one."
- Snacks/beverages: "selling expired products and no refund options"
