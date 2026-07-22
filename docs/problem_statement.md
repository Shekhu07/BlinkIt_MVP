# Part 3: Problem Statement

## Status
Locked 2026-07-22. Built from Part 1 (AI discovery engine, real Two-Step Gated extraction) and Part 2 (real 24-response Phase 3 survey — see `part2_research_tracker.md` for the full theme-confirmation grid). No mock or placeholder data.

---

## 1. Target Segment

**Repeat Blinkit buyers who default to their existing categories and rarely explore new ones.**

- In the Phase 3 survey (N=24), **13/24 (54%)** described their recent behavior as "mostly stick to the same categories" — this is the population the growth goal is about (increase % of MAU purchasing from at least one new category monthly).
- These are not occasional or lapsed users: most order "Daily" or "2–3 times a week," across staple categories (groceries, fresh produce, snacks). They are heavy, habitual users of the platform who have simply never widened their basket.
- Demographically unremarkable — spans Tier 1/2/3 cities, students through working professionals, 18–45+. This is a mainstream, not a niche, segment, which matters for the size of the opportunity.

---

## 2. Root Cause

**A quality/reliability failure (damaged, expired, or fake/duplicate item) generalizes into either category-specific avoidance or, in some cases, platform-level abandonment — but this alone doesn't explain all category stagnation.**

This is the real, evidence-backed version of Part 1's top theme: **"Poor Quality and Unreliable Products,"** 770 of 1,094 gate-passing extractions (70%) in the discovery engine, spanning groceries, electronics, snacks, household essentials, and personal care roughly proportional to category volume.

The Phase 3 survey both **confirms** and **complicates** this root cause:

**Confirmed** — quality incidents do generalize beyond the affected category:
- *"I have stopped exploring new categories on Blinkit. I only order the essential items now if anything urgent."* (respondent whose puja-item order arrived damaged/wrong-sized and whose complaint went unresolved)
- *"yes I am skeptical of buying electronic products from Blinkit and other similar applications"* (damaged electronics order)
- *"I avoid buying any fresh products dairy or perishables items from quick commerce apps."* (expired dairy order — notably generalized to the *entire quick-commerce category*, not just Blinkit)

**Challenged** — the mechanism is not uniform, and quality alone doesn't fully explain the segment:
- One respondent had the identical failure mode (damaged item, fully refunded) but instead of avoiding a category on Blinkit, **switched to a competitor (Zepto) entirely** — a platform-churn risk distinct from, and arguably more severe than, category-adoption stagnation.
- **5 of 12** respondents who had a qualifying incident reported **no behavior change at all**, and in at least one case continued actively considering 6+ new categories afterward — resolution (most incidents got a full refund or replacement) often neutralizes the effect.
- **6 of the 13** "stuck" respondents had **no incident in the last 3 months at all**, yet are still in the target segment — for a meaningful share of the stagnant population, the barrier isn't a personal bad experience, it's simply low intent ("I just don't need those categories").
- A distinct sub-cause surfaced that isn't about product-source quality: **packaging/fulfillment failure** — fragile items (e.g., stationery) arriving crushed because they were packed under heavier groceries, not because the product itself was defective at the source.

**Working root cause statement**: for the portion of the stuck segment that *is* driven by quality/trust (roughly half of incident-havers, and plausibly more given how the fear generalizes even without a personal incident), an unresolved or generically-handled quality failure removes the benefit of the doubt a user would otherwise extend to an unfamiliar category — they default to what's already proven safe rather than risk a repeat failure in something new.

---

## 3. Existing User Workarounds

Two distinct workaround patterns emerged directly from the survey, both real quotes:

1. **Retreat to "essentials only"** — rather than switching platforms, some users simply stop exploring anything beyond what they already trust: *"I only order the essential items now if anything urgent."* This directly suppresses the new-category-adoption metric without the user leaving the platform.
2. **Platform switching** — some users route around the friction entirely by shifting spend to a competitor: *"I have started using Zepto more."* This is a more expensive workaround for Blinkit's business, since it's not just a missed category-adoption opportunity but active share loss.

Both workarounds are evidence that users aren't simply giving up on quick-commerce — they're actively managing around a specific, nameable friction, which means a targeted fix has a real behavioral lever to pull.

---

## 4. Why Solving This Creates User Value

Users in the target segment are not disengaged — they're heavy, habitual Blinkit users who've simply narrowed their basket to what they already trust. The Phase 3 survey directly asked what would change that (Q15, ranked by responses):

1. **A clear "no questions asked" return/refund guarantee** — the single most-picked driver (11 of 24 picks)
2. **Better visible quality/freshness guarantees** (e.g., certified/verified brand tags) — 8 picks
3. Reviews/ratings for the specific item, and an option to inspect before accepting delivery — 5 picks each

None of these require inventing a new need — they're asking Blinkit to extend the same confidence they already have in their staple categories to an unfamiliar one. Solving this doesn't just reduce complaints; it directly unlocks the exploration behavior these users are already primed for (recall: only 6 of 13 stuck respondents cite an actual bad experience — the rest simply haven't been given a reason to trust an unfamiliar category yet).

---

## 5. Why Solving This Makes Business Sense

Real corroboration from Eternal Limited's (Blinkit's public parent) Q4 FY26 earnings call (2026-04-28, investor relations transcript):

> Analyst (Jignanshu Gor, Bernstein): *"as a large part of our growth narrative from here on depends in some sense on either growing the non-grocery assortment and going outside of the metro cities."*

> Akshant Goyal (CFO), on the 60% CAGR growth guidance: *"It's a function of assortment expansion, geographical expansion as well as more demand densification in the cities where we are present today and we might also get into newer cities."*

Management has explicitly tied Eternal's forward growth guidance to **non-grocery assortment expansion** — the same category-adoption behavior this project is investigating. The transcript does not directly address product quality or refund friction (an honest gap, not glossed over), but the strategic dependency is clear: if quality/trust friction is real and left unaddressed, it is a **headwind against a growth lever leadership is already betting on**.

There's a second, sharper business argument the survey surfaced that the concall doesn't cover: the CFO's transcript notes orders-per-customer declined (3.6 → 3.35) but attributes this to new-customer dilution, not existing-customer disengagement — *"We haven't seen too much impact on customer retention."* The Phase 3 finding of at least one respondent actively **switching to a competitor** after a quality incident is a direct, named counter-signal worth raising: quality-driven churn may be an under-measured contributor to the metrics leadership is already watching, not just a category-adoption-rate problem.

---

## 6. What This Means for Part 4

The MVP (Category Nudge Agent) should:
- Target users who resemble the "stuck" segment (heavy, habitual, narrow-category buyers).
- Lead with the two highest-ranked confidence drivers — a refund/return guarantee callout and a quality/freshness signal — rather than a generic "try something new" nudge.
- Be honest in its scope: this addresses the ~50% of stagnation that's quality/trust-driven, not the portion driven by simple lack of interest — the problem statement above should not overclaim that fixing quality alone converts the entire stuck segment.
