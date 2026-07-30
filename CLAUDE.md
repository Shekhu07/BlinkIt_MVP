# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A NextLeap PM Fellowship graduation project (deadline: 4 Aug 2026, 3:59 PM IST — strict) built around Blinkit's category-adoption growth goal. Part 1 is an AI discovery engine over ~15.8k scraped Blinkit reviews, Parts 2–3 are user research and problem framing, Part 4 is the deployed "Category Nudge Agent" MVP. The full brief is in `Blinkit PRD.pdf`.

All four parts are complete. **Two Gradio apps are deployed live on HuggingFace Spaces** (both free tier, both required submission links):
- `discovery/` — the Part 1 workflow demo (Live Extractor runs the real gated extraction on any pasted review; Results Explorer renders the real findings from `discovery/data/results.json`).
- `mvp/` — the Category Nudge Agent (operator console + phone mockup; live Groq nudge generation).

The Phase 6 deck is built and submission-ready: `deck/design/Blinkit Category Nudge Case Study.dc.html`
is the authoritative 10-slide source (see its own `deck/design/CLAUDE.md` for the graded hard
rules), exported to `deck/NL Blinkit Category Adoption.pdf` and rebuilt as an editable
`deck/NL_Blinkit_CategoryAdoption.pptx` via `deck/build_deck.py`. `docs/deck_spec.md` and
`docs/deck_outline.md` are earlier planning drafts (different title, N=25 survey, 11-slide
structure with an appendix) superseded by the HTML deck — don't treat them as current.

**The PDF is generated from the HTML, not from `build_deck.py`** — editing the builder never
changes the PDF. `build_deck.py` produces only the editable PPTX mirror, and it renders onto a
**20 × 11.25in canvas (`SCALE = 1.5`), which is deliberate, not a mistake**: that is exactly
1920×1080 at 96 DPI, so HTML px × 0.75 = pt and the design's 19px floor lands at 14.25pt. Authoring
at the usual 13.333 × 7.5in puts the dense panels at 9–13.5pt, under the PRD's 14pt floor; clamping
those sizes up instead of rescaling flattens ~90% of runs to one size and destroys the type
hierarchy. All geometry must go through the `IN()` helper so the scale stays consistent.

**Source of truth for project state and design decisions is `docs/`**, especially:
- `docs/implementation-plan.md` — phase-by-phase status with checkboxes (what's real vs. not started)
- `docs/architecture.md` — pipeline design, the Two-Step Gated Schema rationale, LLM choices, and §6.4 the UI design system + Gradio hardening rules
- `docs/problem_statement.md` — the locked Part 3 problem statement; §6 scopes what the MVP may claim
- `docs/phase3_google_form.md` — the canonical Phase 3 questionnaire (supersedes the other two survey drafts in docs/)
- `docs/mvp_qa_log.md` — running Q&A/decision log for Part 4

Read the relevant doc before changing pipeline behavior — several scripts were rewritten after real-run failures, and the docs record why.

## Running things

No build step or linter in this repo, and **no tests here** — everything is direct Python script
invocation using the checked-in venv. (The only test suite in the project lives in the deployed MVP
clone, not in `mvp/` — see the divergence warning below.)

```bash
# Infra (Postgres 15 + Redis; schema auto-applied from database/schema.sql on first boot)
docker-compose up -d

# Always use the venv's python
./venv/bin/python analysis/prefilter.py

# Run either deployed app locally (Gradio, http://localhost:7860)
./venv/bin/python mvp/app.py
./venv/bin/python discovery/app.py

# Rebuild the editable PPTX from deck/build_deck.py (the PDF comes from the HTML, not this)
./venv/bin/python deck/build_deck.py

# The MVP's tests exist ONLY in the deployed clone (pytest is in that clone's
# requirements-dev.txt; it is in none of this repo's requirements files):
cd ~/blinkit-category-nudge-agent
/Users/abhishekspillai/Blinkit_PRD/venv/bin/pip install -r requirements-dev.txt
/Users/abhishekspillai/Blinkit_PRD/venv/bin/python -m pytest tests/ -q
/Users/abhishekspillai/Blinkit_PRD/venv/bin/python -m pytest tests/test_cart_filler.py::test_name -q   # single test
```

Pipeline order (each stage reads the previous stage's DB table):

1. `scrapers/ingest_master_json.py` (and other `scrapers/ingest_*.py`) → `raw_reviews`
2. `analysis/prefilter.py` → `filtered_reviews` (heuristic: drops short/5-star reviews)
3. `analysis/extract_themes.py` → `extractions` (batched Groq LLM calls). `fast_extract.py` is the
   abandoned pre-Groq (Gemini) prototype this replaced — it now fails on import since
   `google-generativeai` was removed; don't use it or "fix" its import.
4. `analysis/cluster_themes.py` → `themes` + `theme_evidence`
5. `analysis/validate_themes.py` → LLM-judge validation against a theme-relevant held-out sample
6. `analysis/analyze_concalls.py` → Eternal earnings-call corroboration

Requires `.env` (copy from `.env.example`): `GROQ_API_KEY` and `DATABASE_URL` are the ones that matter. Celery/Redis config exists (`celery_config.py`) but the pipeline does **not** run through Celery — scripts are invoked directly.

## Architecture and constraints that aren't obvious from any single file

- **LLM provider is Groq, not Gemini.** Gemini was abandoned (free tier: 20 req/day; model deprecated). All extraction/clustering/validation uses Groq `llama-3.1-8b-instant`; `llama-3.3-70b-versatile` is reserved for the Part 4 agent. Don't reintroduce Gemini. **`google-generativeai` was removed from `requirements.txt` and the venv (2026-07-29, ~150MB of orphaned dependencies)** — `GEMINI_API_KEY` remains in `.env.example` as a documented dead setting, and `analysis/fast_extract.py` (the never-adopted Gemini extraction variant) will now fail on import if run; it was already effectively dead per the note above, so this wasn't a functional loss.
- **The Two-Step Gated Schema is the core design decision.** Extraction first hard-gates each review on relevance to *category-adoption behavior* (`mentions_category_behavior`), rejecting general service complaints (refunds, delivery, pricing) unless explicitly tied to category trial/avoidance. An earlier open-ended version surfaced only generic complaint themes and was scrapped. Any prompt change must preserve the gate and its few-shot examples.
- **Theme evidence counts must stay deterministic and DB-backed.** `evidence_count` is computed by counting rows, never LLM-estimated. The headline result — "Poor Quality and Unreliable Products", 770/1,094 gate-passing extractions (~70%) — is cited across the docs; anything that changes these numbers needs the docs updated to match.
- **Scripts define their own SQLAlchemy models inline** (each script redeclares the table classes it needs) rather than sharing a models module; the authoritative schema is `database/schema.sql`.
- **Mock artifacts are deliberately labeled.** `analysis/mock_themes.py`, `scrapers/ingest_reddit_mock.py`, and `docs/mock_interview_notes.md` are prototypes/placeholders — never present their output as real findings. The project history includes a mock-data incident that had to be unwound; keeping real vs. mock unambiguous is a hard requirement. This extends to **imported UI designs**: both Claude Design mockups shipped with invented figures (fabricated funnel counts, invented theme names, fake confidence scores, invented pricing) and the discovery mock simulated extraction client-side. Implement the design *chrome*, never its numbers or canned output — wire every figure to the real export and every generation to a live Groq call. Substitutions are tabulated in `discovery/README.md` and `mvp/README.md`.
- **`mvp/data/synthetic_profiles.json` is synthetic and says so.** Its `_meta.SYNTHETIC` flag, the display-fields note, and the app's "Synthetic demo data" pill must all stay. The behavioural fields (order_frequency, top_categories, recent_incident, stated_barrier) are what the matcher and agent actually use; the display fields (name, tenure, locality…) exist only for the UI.
- **The MVP must not overclaim.** `docs/problem_statement.md` §6 scopes it to the ~50% of stagnation that is quality/trust-driven. The agent's system prompt rule 4 and the UI's "out of primary scope" banner both enforce this for low-intent users — don't soften either.
- **Scope decisions already made:** live Reddit scraping was dropped (bot protection / scoping) — the only "reddit" rows in `raw_reviews` come from `scrapers/ingest_reddit_mock.py` and are mock/placeholder, never real. Live re-scraping of the App Store was also dropped, but real historical App Store data (530 rows: 500 from `data/blinkit_reviews.json` + 30 from the master JSON dump) was already ingested and is real, not mock — don't describe App Store as unanalyzed. Real sources in `raw_reviews`, summing to the full 15,820: Play Store (8,058), Google Maps (4,098), **`unknown_master` (2,532)**, App Store (530), MouthShut (520), ConsumerComplaints.in (76), reddit (6, mock), via `data/MASTER_Blinkit_Reviews.json` and `data/blinkit_reviews.json`. **`unknown_master` is the catch-all in `ingest_master_json.py` for the 2,551 rows in the master dump that carry no `source` field at all** — 16% of the corpus is real scraped review text whose originating platform was never recorded. These are real, not mock, so they stay in the corpus and the funnel; the discovery app displays them as "source not recorded" rather than as a platform name. Don't quote the first five sources as if they were the whole corpus — they account for only 13,282 of 15,820.

## The two deployed apps (`discovery/` and `mvp/`)

- **Both are Gradio on HuggingFace Spaces, free tier.** The Docker SDK is paywalled on this account and CPU-basic hardware was not selectable, so both run on **ZeroGPU** — which refuses to boot unless a `@spaces.GPU` function exists. Each app registers a no-op `_zerogpu_warmup` purely to pass that check; neither uses a GPU (all LLM work is remote on Groq). Don't remove it.
- **`GROQ_API_KEY` is a Space secret**, never committed. `mvp/.env` and `discovery/.env` are gitignored.
- **Redeploy** by syncing into the corresponding clone (`~/blinkit-discovery-engine`, `~/blinkit-category-nudge-agent`) and pushing; HF rebuilds automatically. **Never copy a folder's contents wholesale without diffing first** — see the divergence warning below.
- **⚠️ `mvp/` in this repo is NOT what is deployed.** `~/blinkit-category-nudge-agent` has diverged and is *ahead* on code: it holds a **pytest suite (`tests/`, 51 passing) and GitHub Actions CI (`.github/workflows/tests.yml`)**, `friction_matching.primary_suggested_category()`, parallel nudge generation via `ThreadPoolExecutor`, conditional refund/freshness lines, and newer `agent.py` / `cart_filler.py` / `README.md` — none of which exist in `mvp/`. A blind `cp mvp/* ~/blinkit-category-nudge-agent/` destroys all of it. Always `diff -rq mvp ~/blinkit-category-nudge-agent -x .git -x .env -x __pycache__` first and port only the specific hunks you intend to change. (`discovery/` and its clone are in sync — only that clone's `.gitattributes` differs — so it is safe to copy.)
- **The clone can also be *behind* on data, in the same breath as being ahead on code.** On 2026-07-29 the deployed agent was still serving stale **N=25** survey figures in six places, including its user-facing methodology tab, long after the survey was frozen at N=31 — precisely the numbers `deck/design/CLAUDE.md` says must never reappear. When touching either app, check both directions, and grep the clone for stale figures (`11/25`, `9/25`, `14/25`, `56%`, `N=25`).
- **`discovery/data/results.json` is a build artifact** produced by `discovery/export_results.py` from Postgres. The deployed app reads it statically — no DB in production. Re-run the export only if the pipeline is re-run, and update the docs to match the new numbers.
- **Gradio is deliberately UNPINNED and the CSS is written to survive that.** Custom `css=` selectors repeat their class (`.nb-dark.nb-dark.nb-dark .h`) because Gradio 4 auto-prefixes custom CSS and Gradio 6 does not — without the boost, colour rules lose to `.prose *` and dark-panel text renders `#27272A` on `#16130A` (1.25:1, invisible). Don't "simplify" those selectors, and don't pin Gradio to fix it: that took both Spaces offline twice (`HfFolder` ImportError, then a launch ValueError). See `docs/architecture.md` §6.4.
- **UI design system and Gradio hardening rules are in `docs/architecture.md` §6.4.** Four regressions were hit repeatedly and are easy to reintroduce: Gradio ignores `@import` in `css=` (emit font `<link>` in-body); never rely on colour inheritance (declare a base `.gradio-container *{color:<ink>}` rule above the class rules, not `!important`); don't depend on the force-light `js=` redirect (HF's iframe can block it); and strip Gradio's block/group chrome so custom cards are the only surfaces. Verify UI changes by rendering headlessly (Playwright is installed) rather than by eye.

## Deliverable constraints (from the PRD, enforced at submission)

The final deck must not contain the fellow's name anywhere, max 10 slides, min font 14 (Slides/PPT), <40MB, file named like "NL Blinkit…", all linked artifacts publicly accessible. The workflow and the MVP must both be reachable via live links at submission time.
