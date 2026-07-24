# Implementation Plan — Full Project
## Blinkit | PM Fellowship Graduation Project
## Submission Deadline: 4 August 2026, 3:59:00 PM IST (strict, no late acceptance)

---

## 1. Project Summary

Four parts, one connected narrative: build an AI discovery engine to find why users don't explore new categories on Blinkit → validate the strongest finding with real user interviews → frame a clear problem statement → build and deploy an AI-native MVP that addresses it. All four feed a single 10-slide deck plus two live deliverables (the discovery workflow link and the deployed MVP link).

Today's date context: roughly 3 weeks available until the deadline. Plan below assumes a ~20-working-day runway with buffer built in before the hard cutoff.

---

## 2. Phase-by-Phase Plan

### Phase 0 — Setup (Day 1)
- [x] Confirm Blinkit's current Play Store package ID (live App Store re-scraping dropped due to strict bot protection, but real historical App Store data — 530 rows — was ingested via `data/blinkit_reviews.json` and the master JSON dump; see CLAUDE.md)
- [x] Register Reddit API app (Dropped: Scoping to Play Store / MouthShut / CC only)
- [x] Stand up Postgres schema for Part 1 (raw_reviews, filtered_reviews, extractions, themes, theme_evidence, validation_samples, company_disclosures)
- [ ] Reuse Celery + Redis config from existing news-tracker project (Redis is running via docker-compose for the Postgres/Redis stack, but the Part 1 scripts run as direct Python invocations, not yet wired through Celery tasks)
- [x] Confirm Gemini API access via Google AI Studio — **confirmed but switched off**: Gemini's free tier caps at 20 requests/day (and "Gemini 1.5 Flash" itself is deprecated/removed from the API entirely as of 2026-07-18). Moved to **Groq** (`llama-3.1-8b-instant` / `llama-3.3-70b-versatile`) for both Part 1 extraction and the planned Part 4 agent reasoning — see architecture.md §7.
- [x] Block out interview recruitment channels for Part 2 (personal network, online communities) — see `interview_recruitment_kit.md` for outreach templates; actual recruitment execution still pending (Phase 3)

### Phase 1 — Discovery Engine Build (Days 2–8)
*(Detailed sub-tasks in the Part 1–specific implementation plan; summarized here)*
- [x] Days 2–4: Ingestion — Play Store, Google Maps, App Store, ConsumerComplaints (via 11k+ `MASTER_Blinkit_Reviews.json`); deduped — 15,820 raw reviews in Postgres
- [x] Days 4–5: Pre-filtering (heuristic filter — short/5-star reviews dropped) — 4,740 filtered reviews
- [x] Days 5–7: LLM extraction (Two-Step Gated Schema, batched Groq `llama-3.1-8b-instant` calls, structured JSON) — **re-run for real 2026-07-18** end-to-end over all 4,740 filtered reviews (the original run had silently stalled at 150/4,740 on Gemini's free-tier quota); 1,094 gate-passing extractions (~23%)
- [x] Days 7–8: Theme clustering + ranking — **redesigned 2026-07-18** to cluster real category×behavior_type combinations with deterministic, DB-backed `evidence_count` (not LLM-estimated). Top theme: **"Poor Quality and Unreliable Products," 770/1,094 evidence (70%)**, stable across repeated independent runs. See `docs/architecture.md` §3.1 and §7.
- [x] **Milestone**: ranked theme list with real evidence — done, see above. This is now the actual, evidence-backed Part 2 segment basis (not the earlier assumption).

### Phase 2 — Validation + Supplementary Signal (Day 9, parallel)
- [x] Sample-validate top themes (LLM-judge cross-check against a held-out theme-relevant sample, not random reviews) — **fixed and re-run 2026-07-18**; original script validated against arbitrary raw reviews (mostly unrelated 5-star "good"/"nice" noise). Real result: 16/20 confirmed, 4/20 unclear, 0 contradicted.
- [x] Review Eternal (Blinkit's parent) Q4 FY26 earnings call transcript (real, fetched 2026-07-18 from investor relations, not fabricated), log corroborating/contradicting points against the real top theme — result: transcript doesn't directly address quality/refund friction (an honest, expected finding per §5 Cross-Project Risks below), but does confirm non-grocery assortment expansion is a real strategic growth driver for Eternal, useful for Phase 4's business-case argument.
- [x] **Updated 2026-07-22**: reviewed Eternal's Q1FY27 shareholders' letter (quarter ended June 30, 2026, published 2026-07-22 — the fellow's own copy) — this closes the Q4 FY26 gap: management now explicitly quantifies inventory losses from expiry/damage/loss-in-transit (1.8% of NOV, concentrated in perishables), directly corroborating the Part 1 top theme with company-reported data, not just an inferred strategic dependency. Also carries current assortment-expansion commentary from Blinkit's CEO and retention-cohort data that tempers the survey's competitor-switching finding. See `problem_statement.md` §5 and `analyze_concalls.py`.

### Phase 3 — User Research (Days 8–13, overlapping with late Phase 1/2)
- [x] Day 8–9: Finalize target segment based on Part 1 theme ranking; write interview guide (each Part 1 theme → open-ended probe, not leading question) — **redone 2026-07-18 against the real Part 1 theme** ("Poor Quality and Unreliable Products," 770 evidence) after the original extraction turned out to be running on incomplete/mock data; see `part2_research_tracker.md` and `interview_recruitment_kit.md`
- [x] Days 9–11: Recruit respondents matching the segment — **done via the Phase 3 Google Form** (`phase3_google_form.md`), not the originally planned live-outreach-only recruitment; 24 real responses collected as of 2026-07-21 (`mock_interview_notes.md` remains an unused placeholder). 6 candidates identified who both match the segment (repeat buyer + qualifying incident) and agreed to a follow-up call — see `part2_research_tracker.md` Candidate Pipeline (R1, R2, R3, R5, R23, R24).
- [x] Days 11–13: Conduct interviews — **scoped decision (2026-07-22): live follow-up calls skipped**, using the survey (**final N=25**; 24 responses were in as of 2026-07-21, a 25th arrived 2026-07-22) as the primary research instrument instead, given deadline constraints. **Note the PRD gap**: Part 2 of the brief asks for *"5–6 user interviews"*; zero were conducted. The substitution is deliberate and documented, but it is a deviation from an explicit numbered requirement — six consenting candidates (R1, R2, R3, R5, R23, R24) remain identified if any are still reachable before the deadline. This is a deliberate, documented scope call (see decision note in `part2_research_tracker.md`), not a skipped task — the survey's open-ended/paragraph fields carry the qualitative depth a live call would have added.
- [x] Day 13: Build the theme-confirmation grid (theme × confirmed/contradicted × supporting quote) — **done, from survey data alone**; see the finalized grid in `part2_research_tracker.md`, including 3 confirming quotes, 3 challenging findings (competitor-switching instead of category-avoidance, no-behavior-change despite incident, segment-level stagnation unexplained by quality/trust), and one new sub-theme (packaging/fulfillment, distinct from product-source quality).
- [x] **Risk flag resolved**: interview recruitment is no longer the critical path — the survey substituted for both recruitment and interviewing. Phase 3 is complete; Phase 4 (problem statement) is now unblocked.

### Phase 4 — Problem Definition Synthesis (Days 13–14)
- [x] Write the problem statement covering: target segment, root cause, existing workarounds, why it creates user value, why it makes business sense (pull in Eternal concall corroboration here) — **done 2026-07-22**, see `problem_statement.md`
- [x] Explicitly document at least one place where interviews confirmed AND one place where they challenged the AI-surfaced themes — **done**, see `problem_statement.md` §2 (3 confirming quotes, 3 challenging findings including platform-churn and segment-level stagnation unexplained by quality/trust) and the full grid in `part2_research_tracker.md`
- [x] **Milestone**: problem statement is locked — see `problem_statement.md`. This defines exactly what Part 4's MVP must address (§6 of that doc).

### Phase 5 — AI-Native MVP Build (Days 14–19)
- [x] **Scope decision (2026-07-22)**: nudge mechanic = refund/return guarantee callout + quality/freshness-verification signal, combined into one nudge (Q15 top two drivers, see `problem_statement.md` §6). Pre-acceptance-inspection option (Q15 tied-third driver) is deferred as a **backlog item for later**, not part of the Phase 5 build — revisit only if time remains after the Milestone below is hit.
- [x] **Enhancement (2026-07-24): peer social-proof line added to the nudge** — maps to the "Sentiment-Targeted Social Proof" pillar of the external Category-Expansion playbook and to Q15's tied-third driver (item reviews/ratings, 5/25). Implemented as a third trust line beside refund + freshness (`social_proof_line` in `agent.py`, rendered on the phone card and PM panel in `app.py`). Stays inside the single-nudge guardrail (a line, not a new mechanic). **Hard constraint enforced in the prompt: no fabricated numbers/ratings/counts** — the playbook's own examples ("Over 1,200 buyers rated 5/5") are invented and were NOT imported; the line is qualitative peer reassurance only, and is empty for out-of-primary-scope (low-intent) users. Verified live across all 8 profiles: zero digits in any social-proof line, empty on the two out-of-scope profiles.
- [ ] **Backlog — Cart-Threshold "Fillers" as micro-trials** (from the Category-Expansion playbook, Pillar 4): at checkout, when a user is short of a free-delivery/discount threshold, surface a low-cost item (~₹60) from a category they've *never* bought, turning the threshold top-up into a zero-friction new-category trial. **Why it's backlog, not Phase 5:** (a) it's a *different surface and mechanic* (checkout carousel, not a push nudge) — adding it now would break the single-nudge-mechanic guardrail; (b) strategically it's most valuable because it targets the segment the Phase-5 agent deliberately punts on — **low-intent/no-incident users** (6/14 of the stuck segment), where a trust guarantee doesn't apply, because a cheap micro-trial needs no pre-existing intent. Sits alongside the deferred pre-acceptance-inspection option as a "what's next" deck item. Note: the playbook's own example uses Home Care / Stationery (non-grooming), consistent with the category-spread fix shipped 2026-07-24.
- [x] Day 14–15: Build synthetic user profile dataset (5–10 profiles reflecting the Part 2 segment's real behavior patterns) — clearly label as synthetic — **done 2026-07-23**: 8 profiles in `mvp/data/synthetic_profiles.json`, each tied to a real Part 2 pattern (unresolved incident, resolved-but-eroding, packaging failure, low-intent/no-incident, platform-churn risk); file `_meta.SYNTHETIC=true`
- [x] Day 15–16: Build the friction-matching layer (maps a user profile to the closest Part 1/3 theme) — **done**: `mvp/friction_matching.py`, deterministic rule-based (no LLM); maps to `mvp/data/friction_themes.json` (real locked Part 1 numbers), with an honest out-of-primary-scope path for no-incident/low-intent users
- [x] Day 16–17: Build the Groq agent layer (switched from Gemini — see Phase 0) — generates the nudge + reasoning, constrained to reference the matched friction theme (not generic copy) — **done**: `mvp/agent.py`, Groq `llama-3.3-70b-versatile`, JSON-mode, leads with refund guarantee + quality/freshness signal per the scope decision; tested live against the Groq API
- [x] Day 17–18: Build the delivery layer (FastAPI endpoint + minimal front end) — **done**: two variants — `mvp/app.py` (Gradio UI, the free HF Spaces entrypoint) and `mvp/app_fastapi.py` (FastAPI + HTML with a JSON `/api/nudge` endpoint, for local/API use and Render). Both smoke-tested end-to-end locally against live Groq.
- [x] Day 18–19: Deploy to production (reuse ArthaAI's HuggingFace Spaces pattern or equivalent), test end-to-end live — **DONE 2026-07-23**: live on a HuggingFace Gradio Space, returning nudges end-to-end (friction match → live Groq call → nudge). **Switched from Docker SDK**: HF gates Docker behind a paid plan on the fellow's account, so the delivery layer was ported to the free Gradio SDK. Deployed on **ZeroGPU** hardware (CPU-basic was not selectable on the account) — the app is CPU-only, so `app.py` registers a no-op `@spaces.GPU` function purely to pass ZeroGPU's startup check. `GROQ_API_KEY` set as a Space secret.
- [x] **Milestone**: MVP is live at a stable URL — **DONE 2026-07-23**. (Paste the final Space URL into the deck + deliverables checklist in Phase 6.)
- [x] **Post-launch UI pass (2026-07-23)**: both live apps redesigned from Claude Design projects into one shared visual language (see `architecture.md` §6.4). The MVP is now an operator console + phone mockup; the discovery app is a console (two tabs at the time of this pass, three since the Bulk Run addition below). In both, the mockups' invented numbers/copy were replaced with the real pipeline export and live LLM output — substitutions tabulated in `mvp/README.md` and `discovery/README.md`. `agent.py`'s output schema was extended (headline/body/refund_line/fresh_line/cta/product/why_user/why_category) with the five hard rules unchanged; `data/synthetic_profiles.json` gained display-only fields, still labelled SYNTHETIC. Verified headlessly: 0 WCAG AA contrast failures, identical light/dark render, no mobile overflow.
- [x] **Bulk Run tab on the discovery app (2026-07-23)**: evaluators can paste up to 50 of their
  own reviews and run them through the same guardrails as the real corpus — dedup → prefilter
  heuristics → Two-Step Gate → deterministic category×behavior counts — with every dropped row
  labelled by the guardrail that removed it (`discovery/batch.py`, `architecture.md` §6.5). Answers
  "can the workflow be tested, or only its output read?" Deliberately capped and non-persistent:
  the shared free-tier Groq key is protected by a hard 50-row error, nothing writes to
  `results.json`, and theme *naming* is not run on a sample that small. Headline numbers unchanged.
  Note: this had to take **pasted text rather than a file upload** — `gr.File` as an event input
  crashes app startup on the pinned Gradio (see the new hardening rule in `architecture.md` §6.4).

### Phase 6 — Deck Build (Days 19–22)

> **Status correction (2026-07-23, from the docs audit).** A first-pass deck **already exists and
> is committed**: `deck/NL_Blinkit_CategoryAdoption.pptx` (built by `deck/build_deck.py`, commit
> `3b6d841`). The checkboxes below stayed unticked, understating actual progress. It is **not yet
> compliant**, so they remain open until the blocker is cleared:
> - 🔴 **11 slides — the PRD hard limit is 10** (slide 11 is the "Appendix · How the discovery
>   engine works" 1-slider). The PRD counts the title slide within the 10 and carves out no
>   exception for an appendix, and `deck_spec.md` is written as "10 slides + appendix", which is
>   what produces the overage. Fold the workflow slide into slide 3 or drop a slide.
> - ✅ Already passing: 58.8 KB (limit 40 MB), zero text runs under 14 pt, `NL Blinkit…` naming,
>   fellow's name absent from all slide text and raw XML, all four hyperlinks resolve HTTP 200.
> - 🟡 Residual: the deck's `tinyurl` links resolve to `…/spaces/Abhishek292000/…`, exposing the
>   fellow's name in the address bar on click. The deck file itself is clean.

- [ ] Structure the 10-slide deck around the cross-part traceability thread (see architecture.md §8) rather than one slide per part in isolation
- [ ] Draft slide titles as key messages, not labels (per guideline: state the finding, don't just say "Problem")
- [ ] Build the 1-slider explaining the Part 1 workflow (separate from the main 10, embedded inside the deck per instructions)
- [ ] Apply formatting constraints: no fellow name anywhere, 10 slides max including title, minimum font size per tool used (14 for Slides/PPT, 26 for Figma @1920×1080, 22 for Canva @1920×1080), colorblind-safe palette, readable text on any background color
- [ ] Hyperlink all supporting artifacts (workflow link, MVP link, survey/interview docs if referenced) — double check access permissions on every linked doc
- [ ] File naming per convention (e.g., "NL BlinkitCategoryAdoption" style), confirm file size under 40MB
- [ ] **Buffer**: Days 22–23 held as contingency before the Aug 4 deadline — do not schedule real work into this buffer

---

## 3. Master Timeline

```
Day 1        : Setup
Days 2–8     : Part 1 — Discovery engine build (ingestion -> filter -> extract -> cluster)
Day 9        : Part 1 — Validation + Eternal concall supplementary signal
Days 8–13    : Part 2 — User research (recruitment starts Day 8, overlapping Phase 1 tail)
Days 13–14   : Part 3 — Problem definition synthesis
Days 14–19   : Part 4 — MVP build + production deployment
Days 19–22   : Deck build + formatting compliance
Days 22–23   : Buffer
Deadline     : 4 Aug 2026, 3:59:00 PM IST
```

---

## 4. Deliverables Checklist (mapped to submission requirements)

| Deliverable | Phase | Notes |
|---|---|---|
| [Link] Discovery workflow, testable | Phase 1/2 | **LIVE 2026-07-23** → https://huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine — three-tab Gradio app (Live Extractor runs the real Two-Step Gated extraction on any pasted review; Bulk Run pushes up to 50 evaluator-supplied reviews through the full guardrail chain; Results Explorer shows the real funnel/themes/validation/concall). Source in `discovery/`. |
| 1-slider on workflow (inside deck) | Phase 6 | Summarizes Part 1 pipeline |
| 10-slide PDF deck | Phase 6 | Full narrative across all 4 parts |
| [Link] Deployed MVP/agent | Phase 5 | **LIVE 2026-07-23** → https://huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent — Category Nudge Agent on HF Gradio Space. Source in `mvp/`. |

---

## 5. Cross-Project Risks

| Risk | Mitigation |
|---|---|
| Interview recruitment slips | Start outreach Day 8, not after Phase 1 fully closes |
| Part 1 themes are too diffuse to pick one segment | Force-rank by evidence count + business relevance; pick top 1, keep a runner-up as backup |
| MVP scope creep (trying to build a "real" feature) | Explicitly scope to synthetic data + single nudge mechanic; a focused agent beats a half-built broader feature |
| Deck built last-minute, formatting violations | Build deck structure by Day 19, leaving 3 days purely for formatting/compliance/proofing |
| Concall data thin or unhelpful for business case | Fall back on category-mix commentary from any public Eternal investor material even if indirect; don't block Part 3 waiting for a perfect quote |

---

## 6. Definition of Done (whole project)

- [ ] All four parts produce a documented artifact (theme list, interview grid, problem statement, deployed MVP)
- [ ] At least one explicit place in the deck shows research confirming or contradicting the AI's findings
- [ ] MVP is live and reachable via URL at submission time
- [ ] Deck adheres to every formatting guideline (anonymity, slide count, font size, file size, naming, hyperlink access)
- [ ] Submission completed with buffer before 4 Aug, 3:59:00 PM IST
