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
- [ ] Reuse Celery + Redis config from existing news-tracker project
- [ ] Confirm Gemini 1.5 Flash API access via Google AI Studio for both Part 1 extraction and Part 4 agent reasoning
- [ ] Block out interview recruitment channels for Part 2 (personal network, online communities, paid panel if needed) — start early since scheduling 5–6 interviews takes lead time

### Phase 1 — Discovery Engine Build (Days 2–8)
*(Detailed sub-tasks in the Part 1–specific implementation plan; summarized here)*
- [x] Days 2–4: Ingestion — Play Store, App Store (JSON dump), MouthShut, ConsumerComplaints; dedup
- [x] Days 4–5: Pre-filtering (TF-IDF)
- [x] Days 5–7: LLM extraction (batched Gemini 1.5 Flash calls, structured JSON)
- [x] Days 7–8: Theme clustering + ranking
- [x] **Milestone**: by end of Day 8, have a ranked theme list with evidence — this determines your Part 2 segment choice, so don't let this slip

### Phase 2 — Validation + Supplementary Signal (Day 9, parallel)
- [x] Sample-validate top themes (human + optional LLM-judge cross-check), log agreement rate
- [x] Manually review last 2–3 Eternal earnings call transcripts, log corroborating/contradicting points against themes

### Phase 3 — User Research (Days 8–13, overlapping with late Phase 1/2)
- [x] Day 8–9: Finalize target segment based on Part 1 theme ranking; write interview guide (each Part 1 theme → open-ended probe, not leading question)
- [x] Days 9–11: Recruit and schedule 5–6 interviewees matching the segment *(mocked for prototype)*
- [x] Days 11–13: Conduct interviews, take notes/recordings (with consent) *(mocked for prototype)*
- [x] Day 13: Build the theme-confirmation grid (theme × confirmed/contradicted × supporting quote) — this is the direct input to Part 3
- [ ] **Risk flag**: interview scheduling is usually the slowest part of any research plan — start recruitment outreach as early as Day 8, don't wait for Phase 1 to fully close first

### Phase 4 — Problem Definition Synthesis (Days 13–14)
- [ ] Write the problem statement covering: target segment, root cause, existing workarounds, why it creates user value, why it makes business sense (pull in Eternal concall corroboration here)
- [ ] Explicitly document at least one place where interviews confirmed AND one place where they challenged the AI-surfaced themes — this is a specific deliverable requirement, don't skip it
- [ ] **Milestone**: by end of Day 14, problem statement is locked — this defines exactly what Part 4's MVP must address

### Phase 5 — AI-Native MVP Build (Days 14–19)
- [ ] Day 14–15: Build synthetic user profile dataset (5–10 profiles reflecting the Part 2 segment's real behavior patterns) — clearly label as synthetic
- [ ] Day 15–16: Build the friction-matching layer (maps a user profile to the closest Part 1/3 theme)
- [ ] Day 16–17: Build the Gemini agent layer — generates the nudge + reasoning, constrained to reference the matched friction theme (not generic copy)
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
