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
- [x] **Personal Network / Alumni Groups** (Start: Day 8) — executed via the Phase 3 Google Form (`phase3_google_form.md`), not live outreach alone; 24 real responses collected as of 2026-07-21
- [ ] **Online Communities** (e.g., Reddit r/delhi, r/bangalore) — not needed; personal-network channel alone produced enough responses
- [ ] **Paid Panel** (Fallback if needed by Day 10) — not needed

## Survey Results Summary (real data, N=25, last updated 2026-07-22)
*Full per-respondent breakdown lives in `Survey_Responses.pdf` / the linked Google Sheet — this is the rollup used for segment/candidate selection.*
- **Segment size**: 14/25 (56%) answered "mostly stick to the same categories" on Q6 — this is the target segment for the %MAU growth goal.
- **Incident rate**: 13/25 (52%) had a bad order in the last 3 months (Q7=Yes). Failure types: damaged items dominate (10/13), plus 1 expired, 1 fake/duplicate, 1 other (rotten flowers + wrong size).
- **Resolution**: mostly resolved — 9 full refunds, 3 replacements, 1 unresolved. Support responsiveness is not the core problem; behavior change persists even when resolution works.
- **Theme confirmation (Q11, among the 13 incident-havers)**: exactly **6/13 (46%) clearly confirmed** a behavior change, **6/13 (46%) reported no change**, 1 ambiguous — a genuinely even split, not a landslide either way. Notable finds:
  - One respondent switched to a competitor (Zepto) entirely rather than avoiding a category on Blinkit — a platform-churn signal distinct from category-adoption stagnation, worth a separate thread in the problem statement.
  - One respondent generalized avoidance to "quick commerce apps" broadly (fresh/dairy/perishables), not Blinkit-specific — suggests the friction may be industry-wide, not a Blinkit-specific weakness.
  - One respondent's issue was packaging/fulfillment (fragile items crushed under groceries), not product-source quality — a distinct root-cause subtype worth flagging separately from "fake/expired/damaged-at-source."
- **Confidence drivers (Q15, ranked by picks)**: 1) "No questions asked" refund/return guarantee (11), 2) Better visible quality/freshness guarantees (9), 3) Reviews/ratings & inspect-before-accepting (5 each). Directly informs what the Part 4 Category Nudge Agent should emphasize.
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

## Theme-Confirmation Grid (finalized from survey data, N=25)
*Required deliverable per PRD Part 3: demonstrate where primary research validated AND where it challenged the AI-surfaced theme ("Poor Quality and Unreliable Products" blocking category-adoption behavior). Built entirely from the 25 survey responses — see decision note above.*

| Status | Evidence | Supporting quote |
|---|---|---|
| **Confirmed** | R2 — unresolved puja-item complaint led to a full stop on category exploration | *"I have stopped exploring new categories on Blinkit. I only order the essential items now if anything urgent."* |
| **Confirmed** | R1 — damaged electronics order generalized to category-level distrust | *"yes I am skeptical of buying electronic products from Blinkit and other similar applications"* |
| **Confirmed** | R24 — expired dairy generalized to an industry-wide avoidance pattern, not Blinkit-specific | *"I avoid buying any fresh products dairy or perishables items from quick commerce apps."* |
| **Challenged** | R5 — same failure mode (damaged item, full refund) produced platform switching, not in-app category avoidance. The AI theme predicts users stay on Blinkit but avoid new categories; this shows some users leave entirely instead | *"I have started using Zepto more"* (also rated cross-category hesitancy low, 1/5 — the stated attitude and the actual behavior diverge) |
| **Challenged** | R3, R7, R8, R12, R22, R25 — **6 of 13** incident-havers reported **no behavior change at all** despite a qualifying incident and, in several cases, actively considering multiple new categories afterward (e.g., R12 listed 6 categories still under consideration) — an exact even split against the 6 who did confirm | *"No change"* / *"No"* / *"not really"* (repeated across respondents) |
| **Challenged (segment-level)** | 6 of the 14 "mostly same categories" respondents had **no incident at all** (Q7=No) yet are still in the stuck segment — meaning quality/trust alone doesn't explain all category stagnation; for some it's simply lack of interest | R9: *"Nothing in particular — I just don't need those categories"* |
| **New sub-theme (neither confirms nor contradicts, refines root cause)** | R23 — the failure was packaging/fulfillment (fragile items crushed under groceries during packing), not product-source quality (fake/expired/defective) | *"often packed at the bottom of the bag under heavier groceries"* |

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
