# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A NextLeap PM Fellowship graduation project (deadline: 4 Aug 2026, 3:59 PM IST — strict) built around Blinkit's category-adoption growth goal. It is a data/research pipeline plus documentation, not a deployable app (yet): Part 1 is an AI discovery engine over ~15.8k scraped Blinkit reviews, Parts 2–3 are user research and problem framing, Part 4 will be a deployed "Category Nudge Agent" MVP. The full brief is in `Blinkit PRD.pdf`.

**Source of truth for project state and design decisions is `docs/`**, especially:
- `docs/implementation-plan.md` — phase-by-phase status with checkboxes (what's real vs. not started)
- `docs/architecture.md` — pipeline design, the Two-Step Gated Schema rationale, LLM choices
- `docs/phase3_google_form.md` — the canonical Phase 3 questionnaire (supersedes the other two survey drafts in docs/)

Read the relevant doc before changing pipeline behavior — several scripts were rewritten after real-run failures, and the docs record why.

## Running things

No build, tests, or linter. Everything is direct Python script invocation using the checked-in venv:

```bash
# Infra (Postgres 15 + Redis; schema auto-applied from database/schema.sql on first boot)
docker-compose up -d

# Always use the venv's python
./venv/bin/python analysis/prefilter.py
```

Pipeline order (each stage reads the previous stage's DB table):

1. `scrapers/ingest_master_json.py` (and other `scrapers/ingest_*.py`) → `raw_reviews`
2. `analysis/prefilter.py` → `filtered_reviews` (heuristic: drops short/5-star reviews)
3. `analysis/extract_themes.py` → `extractions` (batched Groq LLM calls; `fast_extract.py` is the batched/faster variant)
4. `analysis/cluster_themes.py` → `themes` + `theme_evidence`
5. `analysis/validate_themes.py` → LLM-judge validation against a theme-relevant held-out sample
6. `analysis/analyze_concalls.py` → Eternal earnings-call corroboration

Requires `.env` (copy from `.env.example`): `GROQ_API_KEY` and `DATABASE_URL` are the ones that matter. Celery/Redis config exists (`celery_config.py`) but the pipeline does **not** run through Celery — scripts are invoked directly.

## Architecture and constraints that aren't obvious from any single file

- **LLM provider is Groq, not Gemini.** `google-generativeai` is still in requirements and `GEMINI_API_KEY` in `.env.example`, but Gemini was abandoned (free tier: 20 req/day; model deprecated). All extraction/clustering/validation uses Groq `llama-3.1-8b-instant`; `llama-3.3-70b-versatile` is reserved for the Part 4 agent. Don't reintroduce Gemini.
- **The Two-Step Gated Schema is the core design decision.** Extraction first hard-gates each review on relevance to *category-adoption behavior* (`mentions_category_behavior`), rejecting general service complaints (refunds, delivery, pricing) unless explicitly tied to category trial/avoidance. An earlier open-ended version surfaced only generic complaint themes and was scrapped. Any prompt change must preserve the gate and its few-shot examples.
- **Theme evidence counts must stay deterministic and DB-backed.** `evidence_count` is computed by counting rows, never LLM-estimated. The headline result — "Poor Quality and Unreliable Products", 770/1,094 gate-passing extractions (~70%) — is cited across the docs; anything that changes these numbers needs the docs updated to match.
- **Scripts define their own SQLAlchemy models inline** (each script redeclares the table classes it needs) rather than sharing a models module; the authoritative schema is `database/schema.sql`.
- **Mock artifacts are deliberately labeled.** `analysis/mock_themes.py`, `scrapers/ingest_reddit_mock.py`, and `docs/mock_interview_notes.md` are prototypes/placeholders — never present their output as real findings. The project history includes a mock-data incident that had to be unwound; keeping real vs. mock unambiguous is a hard requirement.
- **Scope decisions already made:** App Store and Reddit ingestion were dropped (bot protection / scoping); sources are Play Store, Google Maps, MouthShut, ConsumerComplaints via `data/MASTER_Blinkit_Reviews.json`.

## Deliverable constraints (from the PRD, enforced at submission)

The final deck must not contain the fellow's name anywhere, max 10 slides, min font 14 (Slides/PPT), <40MB, file named like "NL Blinkit…", all linked artifacts publicly accessible. The workflow and the MVP must both be reachable via live links at submission time.
