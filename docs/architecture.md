# Architecture — Full Project
## Blinkit | PM Fellowship Graduation Project | Category Adoption Growth Problem

---

## 1. Problem Recap

Growth Team goal: **increase the % of Monthly Active Customers who purchase from at least one new category every month**, on Blinkit. The project has four parts — an AI discovery engine, primary research, problem framing, and a deployed AI-native MVP — and this document describes how all four connect as one system, not four disconnected exercises.

---

## 2. End-to-End System View

```
┌─────────────────────┐     ┌──────────────────────┐     ┌───────────────────────┐     ┌─────────────────────────┐
│   PART 1             │     │   PART 2              │     │   PART 3                │     │   PART 4                 │
│   Discovery Engine   │ --> │   User Research        │ --> │   Problem Definition    │ --> │   AI-Native MVP           │
│   (automated, at     │     │   (5–6 interviews,     │     │   (synthesis doc,       │     │   (deployed agent/        │
│   scale, AI-driven)  │     │   manual, targeted)     │     │   no new infra)         │     │   feature, production)    │
└─────────────────────┘     └──────────────────────┘     └───────────────────────┘     └─────────────────────────┘
        │                            │                              │                              │
        v                            v                              v                              v
   Ranked themes +           Confirmed/contradicted           Target segment,               Live system that acts
   evidence, segment          themes, direct quotes,           root cause, business           on the validated
   hypotheses                 workaround patterns              case (with concall data)       insight in real time
```

Each part **consumes the output of the previous part as its primary input.** This is the throughline the deck needs to make explicit — Part 2's interview guide is built from Part 1's themes, Part 3's problem statement is built from Part 1+2 combined, and Part 4's MVP directly targets the root cause named in Part 3. Nothing is built in isolation.

---

## 3. Part 1 — AI-Powered Discovery Engine (Architecture Summary)

*(Full detail lives in the Part 1–specific architecture doc already built; summarized here for the whole-project view.)*

```
Data Sources (Play Store, App Store [JSON dump], MouthShut, ConsumerComplaints, Eternal concalls)
   -> Ingestion (Celery + Redis, dedup via SHA-256)
   -> Pre-filter (TF-IDF, drop non-relevant noise)
   -> LLM Extraction (Gemini 1.5 Flash, structured JSON: behavior_type, category, reason, confidence)
   -> Theme Clustering (embedding similarity / LLM merge pass)
   -> Validation Sampling (human + LLM-judge cross-check)
   -> Postgres storage + FastAPI query endpoint
```

**Output artifact carried into Part 2**: a ranked list of themes (e.g., "trust deficit on personal-care brand sourcing," "no discovery trigger at right moment," "habitual reordering via saved carts") each tagged with a likely user segment. This ranked list is what determines *which* segment you recruit for interviews — not a guess made independently.

**Supplementary signal**: Eternal Ltd's (Blinkit's public parent) earnings call transcripts, manually reviewed, logged against themes as `corroborates | contradicts | unrelated_context`. This becomes direct ammunition for Part 3's business case.

### 3.1 LLM Extraction — Gated Schema (revised)

**Why this matters — a calibration failure found and fixed during the build**: an initial run of the extraction step against the full ~11,000-review corpus surfaced four macro-themes (broken refund/support, quality control failures, inflated pricing/COD, delivery partner misconduct) that were all general service-quality issues, not category-adoption behavior. None connected credibly to the strategic goal. Root cause: the extraction prompt was doing open-ended theme generation instead of hard-gating on relevance to category exploration, discovery, or repeat-purchase habits — so the LLM clustered on whatever was most prevalent in the raw text (service complaints, which dominate review corpora by volume), rather than what was relevant to the research question. The extraction step was rewritten to gate strictly on relevance before extracting anything.

**Revised extraction logic — two-step gate-then-extract:**

*Step 1 — Relevance gate.* The prompt requires the model to check whether the text relates to: why a user keeps buying the same category, why a user has *not* tried an unfamiliar category, how users discover new products/categories, a specific moment of considering/trying/rejecting a category, trust or risk specifically about trying something unfamiliar, or habitual/repeat-purchase patterns. Text that is primarily about refunds, support, delivery timing/conduct, pricing, payments, or general app bugs — **with no explicit tie to category trial/avoidance** — is rejected at this step (`mentions_category_behavior: false`) rather than forced into a theme.

*Step 2 — Structured extraction (only if Step 1 passes):*
```json
{
  "mentions_category_behavior": true,
  "behavior_type": "repeat_purchase | category_avoidance | discovery_friction | new_category_trial",
  "category_mentioned": "groceries | personal_care | pet_supplies | baby_products | electronics | household_essentials | snacks_beverages | other | unspecified",
  "underlying_reason": "one sentence, paraphrased, not a quote",
  "sentiment": "frustration | neutral_observation | satisfaction | curiosity",
  "confidence": 0.0-1.0
}
```

**Few-shot calibration**: the prompt includes worked examples distinguishing genuine category-behavior signal from complaints that merely *mention* a category incidentally (e.g., a wrong-item refund complaint that happens to name "baby wipes" is correctly rejected — it says nothing about why the user chose or avoided that category).

**Expected effect**: the surviving dataset after re-running Step 1 against the existing 11,000-review corpus is expected to shrink substantially (to an estimated low hundreds of extractions) — this is the correct outcome, not a regression. A high `mentions_category_behavior: false` rate is itself a data point worth carrying into Part 3: category-behavior signal is genuinely scarce and mostly implicit in review data, which says something about how invisible this problem is to users themselves.

**Downstream implication for segment/theme selection**: no segment or theme should be locked in for Part 2 recruitment until the gated re-extraction has run and produced a theme ranking that plausibly connects to category-adoption behavior specifically, not general app service quality.

---

## 4. Part 2 — User Research (Structure, Not Infra)

No new technical architecture here — this is a research design layer, but it's structurally dependent on Part 1's output:

- **Segment selection**: pick the 1–2 segments Part 1's themes point to most strongly (e.g., "grocery-only repeat buyers who've never purchased personal care")
- **Interview guide**: each Part 1 theme becomes a hypothesis to probe, not a question to lead with — e.g., don't ask "do you distrust personal-care brands on Blinkit," ask open questions that let the friction surface unprompted, then map answers back to the theme
- **Artifact produced**: interview notes/transcripts, a synthesis grid (theme x confirmed/contradicted x supporting quote) — this grid is the direct input to Part 3

---

## 5. Part 3 — Problem Definition (Synthesis Layer)

Also not a technical build — a synthesis document that must show, explicitly:

| Requirement | Source |
|---|---|
| Target segment | Part 1 theme ranking + Part 2 recruitment |
| Root cause | Part 1 extraction reasons, confirmed/refined by Part 2 quotes |
| Existing workarounds | Part 2 interviews (rarely visible in review data) |
| Why it creates user value | Part 2 — direct user framing |
| Why it makes business sense | Part 1 discovery + Eternal concall corroboration (§3, supplementary signal) |

The deliverable explicitly asks you to show where primary research **validated or challenged** the AI-surfaced insights — so Part 3's write-up should include at least one instance of contradiction, not just confirmation. That's a more credible research narrative than "everything the AI found was correct."

---

## 6. Part 4 — AI-Native MVP (Architecture)

### 6.1 Recommended MVP shape
Given the problem (category-repetition, discovery friction) and your existing FastAPI/Celery/n8n comfort, the strongest-fit MVP is:

**"Category Nudge Agent"** — an AI agent that:
1. Takes a user's recent basket/order history (mocked/synthetic data if you don't have Blinkit's real order data — this is expected and fine for a fellowship MVP)
2. Cross-references it against the validated friction themes from Part 1+3 (i.e. the "Post-Purchase Support & Refund Friction" theme; the nudge leads with a strong support/return guarantee — rather than just a generic "try this!" banner)
3. Outputs a specific, reasoned category suggestion + the *reason* framed to counter the specific friction identified — this is the part that makes it "AI-native" rather than a static rules-based recommender: the reasoning is generated per-user based on which theme applies to them, not a fixed lookup table

### 6.2 Component architecture

```
┌────────────────┐     ┌───────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│ Synthetic/mock  │ --> │ Friction-Matching  │ --> │ Groq Agent            │ --> │ API endpoint /     │
│ user order data │     │ Layer (rules +     │     │ (generates the        │     │ lightweight UI      │
│                 │     │ theme lookup)      │     │ nudge copy + reason)  │     │ (deployed, live)     │
└────────────────┘     └───────────────────┘     └─────────────────────┘     └──────────────────┘
```

- **Data layer**: synthetic order histories (5–10 representative user profiles built from Part 2 segment insights) stored in Postgres/JSON — clearly labeled as synthetic in the deck, this is standard for fellowship-scale MVPs without production data access
- **Friction-matching layer**: maps a user profile's behavior pattern to the closest theme from Part 1's theme store
- **Agent layer**: Groq API call (`llama-3.3-70b-versatile`) that generates the actual nudge text and reasoning, constrained to reference the matched friction theme — this is where the "AI-native" requirement is satisfied, not just calling an LLM for the sake of it
- **Delivery layer**: a minimal FastAPI endpoint + simple front end (Streamlit or a lightweight HTML page) — this must be **deployed to production** per the deliverable requirement (e.g., Render/Railway/HuggingFace Spaces — reuse whatever hosting pattern you used for ArthaAI)

### 6.3 Why this MVP choice over alternatives
- A pure "workflow" (no agentic reasoning) would satisfy the letter of the requirement but under-deliver on "AI-native" — the brief explicitly lists "an AI agent" as one acceptable MVP form, and an agent that reasons per-user about *why* a nudge is relevant is a stronger product story than a static recommendation widget
- It directly closes the loop: Part 1 finds why users don't explore, Part 2 confirms with real users, Part 3 defines the problem, Part 4 builds the thing that solves it — a reviewer should be able to trace one thread through all four parts

---

## 7. Full-Project Tech Stack

| Layer | Choice | Used in |
|---|---|---|
| Task orchestration | Celery + Redis | Part 1 ingestion, Part 4 background jobs if needed |
| Scraping | `google-play-scraper`, `BeautifulSoup`, `Playwright` (MouthShut, CC), JSON parsing (App Store) | Part 1 |
| Pre-filter | TF-IDF (scikit-learn) | Part 1 |
| LLM | Groq (Llama 3.3 70B) | Part 1 extraction/clustering/validation, Part 4 agent reasoning — switched from Gemini 1.5 Flash (deprecated/removed from the API) after the Gemini free tier's 20-requests/day cap made a multi-thousand-review batch run infeasible |
| Storage | PostgreSQL | Part 1 themes/evidence, Part 4 synthetic user profiles |
| API layer | FastAPI | Part 1 query endpoint, Part 4 MVP endpoint |
| Automation | n8n (optional) | Scheduling Part 1 ingestion, could trigger Part 4 nudge generation on a cadence |
| Deployment | Render/Railway/HuggingFace Spaces (reuse ArthaAI pattern) | Part 4 production deployment |
| Deck | Google Slides/PPT/Figma/Canva (per submission guidelines) | Final deliverable |

---

## 8. Cross-Part Traceability (for the deck narrative)

This is the single most important structural point for evaluators: your deck should be able to answer, at every slide, **"which part does this come from and what did the previous part tell us that led here?"**

```
Theme (Part 1) --> Confirmed/contradicted by [user quote] (Part 2) --> 
Problem statement: [segment] + [root cause] (Part 3) --> 
MVP feature: [specific nudge mechanic addressing that root cause] (Part 4)
```
Pick 1–2 threads and follow them fully through all four parts rather than presenting each part as a disconnected section — this is what separates a "checklist" submission from a "product thinking" submission.
