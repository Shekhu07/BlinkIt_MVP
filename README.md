# Blinkit — Cross-Category Adoption

NextLeap PM Fellowship graduation project. Blinkit's growth team wants more monthly active
customers buying from at least one new category each month. Instead of assuming this is a
discovery problem, the project builds an evidence chain across four parts to test that
assumption and ship a targeted fix.

**Full write-up and evaluator Q&A prep:** [`script.md`](script.md)
**Deck source:** [`deck/design/`](deck/design/) (see [`deck/design/README.md`](deck/design/README.md))

## Live demos

- **Discovery engine (Part 1):** https://huggingface.co/spaces/Cr7292000/blinkit-discovery-engine
- **Category Nudge Agent (Part 4 MVP):** https://huggingface.co/spaces/Cr7292000/blinkit-category-nudge-agent

## The four parts

| Part | What it is | Where |
| --- | --- | --- |
| 1. Discovery engine | AI pipeline that mines ~15.8k public Blinkit reviews with a two-step gated extraction schema to find the real barrier to category adoption | [`discovery/`](discovery/), [`analysis/`](analysis/) |
| 2. Survey | 31-response Phase 3 survey that confirms and complicates Part 1's top theme | [`docs/part2_research_tracker.md`](docs/part2_research_tracker.md), [`docs/phase3_google_form.md`](docs/phase3_google_form.md) |
| 3. Problem statement | The evidence-backed root cause and target segment, built from Parts 1 and 2 | [`docs/problem_statement.md`](docs/problem_statement.md) |
| 4. MVP — Category Nudge Agent ("Blink & Try It") | Groq-powered agent that generates a per-user, reasoned category nudge leading with the two research-ranked trust drivers | [`mvp/`](mvp/), standalone Render deploy at [`render_cart_nudge/`](render_cart_nudge/) |

## Repo layout

- `discovery/` — Part 1 engine as a deployed Gradio app (live extractor, bulk run, results explorer).
- `analysis/` — batch pipeline scripts (theme extraction, clustering, validation) that produced the real Part 1 numbers.
- `scrapers/` — ingestion scripts for the review corpus (MouthShut, Trustpilot, app-store reviews).
- `database/schema.sql` — Postgres schema backing the discovery engine.
- `mvp/` — Part 4 Category Nudge Agent, deployed on Hugging Face Spaces (Gradio/ZeroGPU).
- `render_cart_nudge/` — standalone Cart → Nudge flow, deployed separately to Render after HF compute quota was hit.
- `deck/` — deck design source (`deck/design/`) and product screenshots (`deck/screenshots/`).
- `docs/` — research tracker, problem statement, architecture notes, QA logs, and the Phase 3 survey build sheet.
- `data/` — review corpus exports consumed by the ingestion/analysis scripts.

## Running things

Each deployable component documents its own setup:

- Discovery engine: [`discovery/README.md`](discovery/README.md)
- MVP (Category Nudge Agent): [`mvp/README.md`](mvp/README.md)
- Cart → Nudge (Render deploy): [`render_cart_nudge/README.md`](render_cart_nudge/README.md)

Local Postgres/Redis for the discovery pipeline: `docker-compose up`. Copy `.env.example` to
`.env` and fill in `GROQ_API_KEY` (primary LLM across the project) plus DB/Redis config.

## Stack

Python, Gradio, FastAPI, Postgres, Redis/Celery, Groq (`llama-3.1-8b-instant` for extraction,
`llama-3.3-70b-versatile` for the nudge agent).
