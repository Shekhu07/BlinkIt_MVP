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
