# Extraction prompt v2 — PROPOSAL (not applied)

> **Status: ON RECORD ONLY.** Drafted 2026-07-24, committed 2026-07-24 as a record.
> This is *not* wired into the pipeline.
> `analysis/extract_themes.py` still runs the v1 prompt. The live 1,094 gate-passing /
> 770 (70%) top-theme numbers are unchanged and every doc, the deck, and both HF Spaces
> remain consistent with them.
>
> **Do not commit or apply without the full cascade** (re-extract → re-cluster → re-export →
> update every doc + deck → redeploy both Spaces). Applying it re-invokes the model over all
> 4,740 filtered reviews, which shifts the gate count and therefore the cited headline.

## Why this draft exists

The PRD says the discovery engine should help answer eight questions. The v1 extraction
prompt answers Q1/Q2/Q6 strongly, Q3/Q4/Q8 partially, and Q5/Q7 barely — the last two
deliberately, because review text rarely carries "what info I'd need" or a user's segment
(those are answered by the Part 2 survey). This v2 adds one structured Step-2 field per
under-covered question, while keeping **Step 1 (the gate) verbatim** so the core design
decision and its calibration are preserved.

## The proposed prompt

```python
prompt = (
    "You are an AI extracting specific user behavior from reviews of a quick-commerce app, "
    "to answer why users don't explore new product categories.\n"
    # ---- Step 1 — Relevance Gate (UNCHANGED: the core design decision) ----
    "Step 1 - Relevance Gate: Check if the text relates to: why a user keeps buying the same category, "
    "why a user has not tried an unfamiliar category, how users discover new products/categories, "
    "a specific moment of considering/trying/rejecting a category, trust or risk about trying something unfamiliar, "
    "or habitual/repeat-purchase patterns. If it is primarily about refunds, support, delivery timing/conduct, "
    "pricing, payments, or general app bugs with no explicit tie to category trial/avoidance, set mentions_category_behavior to false.\n"
    # ---- Step 2 — Extraction (EXPANDED to cover all 8 discovery questions) ----
    "Step 2 - Extraction: If mentions_category_behavior is true, fill EACH field using EXACTLY one of the "
    "allowed values below — never invent a new string; use 'unspecified'/'unknown' when unclear:\n"
    "- behavior_type: repeat_purchase | category_avoidance | discovery_friction | new_category_trial\n"
    "- category_mentioned: groceries | personal_care | pet_supplies | baby_products | electronics | "
    "household_essentials | snacks_beverages | other | unspecified\n"
    "- habit_signal: strong_habit | some_habit | none | unknown  (how entrenched the repeat-buying habit is)\n"
    "- discovery_channel: search | recommendation | ad_or_promo | browsing | word_of_mouth | not_applicable | unknown  "
    "(how the user finds, or would find, new products)\n"
    "- info_needed: quality_freshness_guarantee | return_refund_guarantee | reviews_ratings | "
    "inspect_before_accept | price_or_offer | brand_trust | none | unknown  (what would give them confidence "
    "to try a new category)\n"
    "- explorer_signal: explorer | stuck | unknown  (does the user read as someone who tries new categories, "
    "or one who sticks to the same few)\n"
    "- unmet_need: one short paraphrased phrase naming the recurring unmet need, or '' if none\n"
    "- underlying_reason: one sentence, paraphrased\n"
    "- sentiment: frustration | neutral_observation | satisfaction | curiosity\n"
    "- confidence: 0.0-1.0\n"
    "If mentions_category_behavior is false, leave the other fields blank or default. Maintain the Review ID provided.\n"
    'Respond ONLY with a JSON object of the exact shape {"extractions": [{"filtered_review_id": int, '
    '"mentions_category_behavior": bool, "behavior_type": str, "category_mentioned": str, "habit_signal": str, '
    '"discovery_channel": str, "info_needed": str, "explorer_signal": str, "unmet_need": str, '
    '"underlying_reason": str, "sentiment": str, "confidence": float}, ...]}.'
)
```

## Coverage — each PRD question → field

| # | PRD question | Field(s) |
|---|---|---|
| 1 | Why repeat the same category? | `behavior_type=repeat_purchase` + `habit_signal` |
| 2 | What prevents exploring new? | `behavior_type=category_avoidance` |
| 3 | How do users discover today? | `discovery_channel` (new) |
| 4 | Role of habits? | `habit_signal` (new) |
| 5 | Info needed before trying new? | `info_needed` (new) — maps 1:1 to survey Q15 + the MVP nudge |
| 6 | Frustrations that recur? | `sentiment` + `underlying_reason` |
| 7 | Which segments experiment? | `explorer_signal` (new) |
| 8 | Unmet needs across discussions? | `unmet_need` (new) |

Also tightens the audit-found enum leakage (7.2% of gate-passing rows carried invented
category strings like `electronic_items`) via the "use EXACTLY one allowed value" instruction.

## Companion changes required if ever applied

The prompt alone does not persist the new fields:

1. `Extraction` model in `analysis/extract_themes.py` — add columns `habit_signal`,
   `discovery_channel`, `info_needed`, `explorer_signal`, `unmet_need`.
2. `database/schema.sql` — same new columns (authoritative schema).
3. The insert loop in `analysis/extract_themes.py` — map the new JSON keys.
4. Token budget — 11 fields × 15 reviews crowds `max_completion_tokens=3500`; drop the batch
   to 10 or raise the limit, or the truncation warning fires.

## Two application paths (if the decision is ever made to use it)

- **Non-destructive enrichment** *(preferred)*: run only Step 2 over the existing 1,094
  gate-passing rows, writing the new columns without re-running the gate. `mentions_category_behavior`,
  the 1,094, and the 770 stay mathematically untouched; you still gain `info_needed` /
  `discovery_channel` / `explorer_signal` / `unmet_need` for the whole passing set.
- **Full re-run**: replace the v1 prompt and re-extract all 4,740. Higher fidelity, but moves
  the headline and triggers the full doc + deck + redeploy cascade. Only with explicit sign-off.

## Prompt-copy note

The gate wording is shared across three live files (`analysis/extract_themes.py`,
`discovery/extractor.py`, `discovery/batch.py` via `GATE_SPEC`). If v2's Step 1 ever changes,
all three must change together — but v2 deliberately leaves Step 1 identical, so no drift today.
