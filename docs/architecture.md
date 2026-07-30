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

**A v2 prompt exists but is deliberately NOT wired in (2026-07-25).** `docs/extraction_prompt_v2_proposal.md` holds an expanded schema covering all eight of the PRD's discovery questions rather than the four this gate asks. It is kept **on record only**: adopting it would re-run extraction and move the 1,094 gate-passing / 770 top-theme headline, which is cited across the docs, the deck, and both deployed Spaces. Treat it as a documented "what we'd do with more runway", not as pending work — do not wire it in without also re-running the pipeline, re-exporting `discovery/data/results.json`, and updating every downstream number.

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
2. Cross-references it against the validated friction themes from Part 1+3 (the real top theme, **"Poor Quality and Unreliable Products"** — 770/1,094 gate-passing extractions; the nudge leads with a refund/return guarantee plus a quality/freshness signal, the two top-ranked Q15 confidence drivers — rather than just a generic "try this!" banner)
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
- **Delivery layer** (as built): a **Gradio** app deployed free on HuggingFace Spaces. The
  originally planned FastAPI + Streamlit/HTML combination was replaced because HF gated the
  Docker SDK behind a paid plan; the FastAPI variant is retained as `mvp/app_fastapi.py` for
  local/API use. UI is an operator console (synthetic-user picker → profile → agent reasoning)
  beside a phone mockup of the in-app nudge — see §6.4.

### 6.4 UI design system (both deployed apps)
Both live deliverables share one visual language, imported from Claude Design projects
("Blinkit Discovery Engine redesign" and "Blinkit category nudge agent redesign"):
Blinkit yellow (`#F8CD1B`/`#f8cb46`) on near-black ink, Plus Jakarta Sans, rounded white
cards on a warm grey canvas, and a dark panel for machine reasoning.

**Design chrome is reproduced faithfully, but never the mockups' numbers or copy.** Both
mockups shipped with invented data (the discovery mock had 4,200 filtered / fabricated
secondary themes / 84% validation; the MVP mock had invented confidence scores and product
pricing). All of it was replaced with the real pipeline export and live LLM output, and the
substitutions are tabulated in each app's README. This is the same real-vs-mock rule as the
rest of the project.

**Gradio hardening rules — regressions here are easy and were hit repeatedly:**
- **Gradio auto-prefixes `css=` on 4.x but NOT on 6.x — write selectors that survive both.**
  Both Spaces run `gradio` unpinned, so a rebuild on 2026-07-30 pulled **6.21.0**. Gradio 4
  rewrote every custom selector with the container class
  (`gradio-app .gradio-container.gradio-container-4-44-1 .contain .nb-dark .h`); Gradio 6 injects
  it verbatim. Our colour rules therefore collapsed to `(0,1,0)`/`(0,2,0)`, tied Gradio's own
  `.gradio-container-6-21-0 .prose *` `(0,2,0)`, and lost on load order — everything fell back to
  `var(--body-text-color)` `#27272A`. That still reads on white cards but rendered `#27272A` on
  `#16130A` (**1.25:1, invisible**) in the dark reasoning panel and phone frame.
  **Fix: repeat the class** (`.nb-dark.nb-dark.nb-dark .h`) — raises specificity without changing
  what it matches, beats `.prose *` on 6.x, keeps inline styles winning, and preserves the
  relative order among our own rules. Applies on both majors, and costs no dependency change.
- **Do NOT try to fix this by pinning Gradio.** It was attempted first and took both Spaces down
  twice: `gradio==4.44.1` alone resolved `huggingface_hub` 1.x, which removed `HfFolder` that
  Gradio 4 imports (`ImportError`, 503); pinning the hub too then failed with
  `ValueError: When localhost is not accessible, a shareable link must be created`. A Space build
  failure takes a submission link **fully offline**, which is strictly worse than a contrast bug.
  Both Spaces were reverted to unpinned and fixed in CSS instead. Diagnose this class of bug by
  comparing the *same selector's* computed colour local vs live — reading the CSS is useless,
  it looks correct under both versions.
- **Do not wire `gr.File` / `gr.UploadButton` as an event input** on the pinned Gradio
  (4.44.1 / gradio_client 1.3.0). API-schema generation raises
  `TypeError: argument of type 'bool' is not iterable`, the startup self-check fails, and the
  app never binds a port — a boot-time crash, not a cosmetic bug. `show_api=False` does not
  avoid it, and the component renders fine until it is attached to a `.click()`. The discovery
  app's Bulk Run tab takes **pasted text** (CSV / JSON / one-per-line) for exactly this reason.
  Re-test before assuming a Gradio upgrade fixes it.

### 6.5 Evaluator-run bulk mode (discovery app)
The discovery Space has a third tab, **Bulk Run**, so an evaluator can test the *workflow* and
not only read pre-computed findings. It re-implements the real guardrail chain in-memory
(`discovery/batch.py`): Stage 0 dedup (same md5 key as `ingest_master_json.py`), Stage 1 the
`prefilter.py` heuristics (empty / <5 words / rating==5), Stage 2 the Two-Step Gate batched 15
per call as in `extract_themes.py`, Stage 3 deterministic (category × behavior_type) counts.
Every dropped row is returned with the guardrail that dropped it — the filtering *is* the demo.

Three scope limits, all deliberate:
- **50-row cap**, enforced as an error rather than a silent truncation. Both Spaces share one
  free-tier Groq key; an uncapped run could exhaust the quota and take both submission links
  offline.
- **No theme naming.** Stage 3 stops at row counts; naming macro-themes off ≤50 rows would
  manufacture findings. The real themes come from 1,094 gate-passing extractions.
- **No persistence.** Nothing writes to `data/results.json`, Postgres, or any artifact; the
  headline funnel (15,820 / 4,740 / 1,094 / 770) is unaffected by anything an evaluator runs.

`GATE_SPEC` in `discovery/extractor.py` is the single copy of the gate wording in that app;
both the single-review and bulk prompts compose from it, so they cannot drift.

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
