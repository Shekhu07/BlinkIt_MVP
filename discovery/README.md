---
title: Blinkit Discovery Engine
emoji: 🔍
colorFrom: yellow
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# Blinkit Category-Adoption Discovery Engine (Part 1 — live workflow link)

The **testable discovery-workflow** deliverable for the NextLeap PM Fellowship project.
Part 1 mines ~15.8k public Blinkit reviews to find **why users don't explore new
categories**. This Space makes that engine interactive:

- **Live Extractor** — paste any review and watch the real **Two-Step Gated Schema** run:
  Step 1 gates on relevance to category-adoption behavior (rejecting refund/delivery/pricing
  noise), Step 2 extracts structured fields. Exact prompt from the batch pipeline
  (`analysis/extract_themes.py`), on Groq `llama-3.1-8b-instant`.
- **Results Explorer** — the real aggregate findings: pipeline funnel
  (15,820 → 4,740 → 1,094 gate-passing), ranked themes with deterministic DB-backed evidence
  counts (top: **Poor Quality and Unreliable Products, 770/1,094 ≈ 70%**), sample real
  evidence quotes, LLM-judge validation (16/20 confirmed), and Eternal earnings-call
  corroboration.

All results are **real pipeline output**, exported to `data/results.json` — no live database
is needed at runtime. (Mock `reddit` rows are excluded from the source display per project
data-integrity rules.)

## Design vs. data (important)

The visual design is imported from the **"Blinkit Discovery Engine redesign"** Claude Design
project. The design *chrome* (layout, brand palette, typography, components, interactions) is
reproduced faithfully — but every **number** comes from the real pipeline export
(`data/results.json`), never from the mockup, which carried placeholder values. Corrections made:

| Mockup value | Real value shipped |
|---|---|
| 15,800 raw reviews | **15,820** |
| 4,200 after filter | **4,740** |
| Themes: Packaging & Fulfillment Damage 142 / Unresolved Complaints 88 / Low Category Intent 66 / Competitor Switching 28 | **Convenience & Price Sensitivity 114 · Discovery Friction & Limited Options 78** (the real clustered themes) |
| 84% LLM-judge validation | **80% (16/20 confirmed, 0 contradicted)** |
| Behavior split: avoidance 61 / trial 22 / consideration 11 / switching 6 | **Real distribution** from `behavior_distribution` |
| Illustrative source-mix bars | **Real per-source counts** (mock `reddit` rows excluded) |
| Invented evidence quotes | **Real review rows** joined from the DB |

The mockup also simulated extraction with a client-side heuristic and canned results; the shipped
app performs a **real Groq call** per request. Keeping real vs. mock unambiguous is a hard project
requirement (see `CLAUDE.md`).

## Architecture

```
data/results.json  ─►  Results Explorer tab   (static, real aggregate findings)
pasted review      ─►  extractor.py  ─► Groq  ─►  Live Extractor tab   (real-time gated extraction)
```

## Run locally

```bash
pip install -r requirements.txt
export GROQ_API_KEY=...           # or a .env with GROQ_API_KEY
python app.py                     # http://127.0.0.1:7860
```

## Regenerate results.json (only if the pipeline is re-run)

```bash
docker-compose up -d              # from repo root; Postgres must hold the pipeline output
./venv/bin/python discovery/export_results.py
```

## Deploy to HuggingFace Spaces (free — Gradio SDK)

1. New Space → SDK **Gradio** → Blank. **CPU basic · Free** is ideal; **ZeroGPU** also works
   (`app.py` carries a no-op `@spaces.GPU` shim so it boots on ZeroGPU).
2. Push this `discovery/` directory's contents (or upload via the web UI). Make sure
   `data/results.json` is included.
3. Space **Settings → Variables and secrets** → add secret `GROQ_API_KEY`.
4. HF installs `requirements.txt` and runs `app.py` → stable public URL = the discovery link.
