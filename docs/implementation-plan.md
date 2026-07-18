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
- [x] Confirm Blinkit's current Play Store package ID (App Store dropped due to strict bot protection)
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

### Phase 3 — User Research (Days 8–13, overlapping with late Phase 1/2)
- [x] Day 8–9: Finalize target segment based on Part 1 theme ranking; write interview guide (each Part 1 theme → open-ended probe, not leading question) — **redone 2026-07-18 against the real Part 1 theme** ("Poor Quality and Unreliable Products," 770 evidence) after the original extraction turned out to be running on incomplete/mock data; see `part2_research_tracker.md` and `interview_recruitment_kit.md`
- [ ] Days 9–11: Recruit and schedule 5–6 interviewees matching the segment — **not started for real; `mock_interview_notes.md` was a prototype placeholder, not actual recruitment.** Use `interview_recruitment_kit.md` outreach templates.
- [ ] Days 11–13: Conduct interviews, take notes/recordings (with consent) — **not started**
- [ ] Day 13: Build the theme-confirmation grid (theme × confirmed/contradicted × supporting quote) — **not started; depends on real interviews above**
- [ ] **Risk flag**: interview scheduling is usually the slowest part of any research plan — start recruitment outreach immediately, this is now the critical path blocking Phase 4

### Phase 4 — Problem Definition Synthesis (Days 13–14)
- [ ] Write the problem statement covering: target segment, root cause, existing workarounds, why it creates user value, why it makes business sense (pull in Eternal concall corroboration here)
- [ ] Explicitly document at least one place where interviews confirmed AND one place where they challenged the AI-surfaced themes — this is a specific deliverable requirement, don't skip it
- [ ] **Milestone**: by end of Day 14, problem statement is locked — this defines exactly what Part 4's MVP must address

### Phase 5 — AI-Native MVP Build (Days 14–19)
- [ ] Day 14–15: Build synthetic user profile dataset (5–10 profiles reflecting the Part 2 segment's real behavior patterns) — clearly label as synthetic
- [ ] Day 15–16: Build the friction-matching layer (maps a user profile to the closest Part 1/3 theme)
- [ ] Day 16–17: Build the Groq agent layer (switched from Gemini — see Phase 0) — generates the nudge + reasoning, constrained to reference the matched friction theme (not generic copy)
- [ ] Day 17–18: Build the delivery layer (FastAPI endpoint + minimal front end)
- [ ] Day 18–19: Deploy to production (reuse ArthaAI's HuggingFace Spaces pattern or equivalent), test end-to-end live
- [ ] **Milestone**: by end of Day 19, MVP is live at a stable URL

### Phase 6 — Deck Build (Days 19–22)
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
| [Link] Discovery workflow, testable | Phase 1/2 | Deployed query endpoint or demo UI |
| 1-slider on workflow (inside deck) | Phase 6 | Summarizes Part 1 pipeline |
| 10-slide PDF deck | Phase 6 | Full narrative across all 4 parts |
| [Link] Deployed MVP/agent | Phase 5 | Must be live in production, not just code |

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
