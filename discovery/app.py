"""Discovery-Workflow demo — the second required live link (Part 1 AI engine).

Two tabs:
  1. Live Extractor    — paste any review, watch the real Two-Step Gated extraction run.
  2. Results Explorer   — the real aggregate findings (funnel, themes, evidence, validation,
                          earnings-call corroboration), from discovery/data/results.json.

Deployed on HuggingFace Gradio SDK (free), same pattern as the MVP. Local run:
    python app.py     -> http://127.0.0.1:7860
"""
import json
import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from extractor import extract_one

load_dotenv()

# --- ZeroGPU compatibility (see mvp/app.py for the full rationale) ---------
try:
    import spaces

    GPU = spaces.GPU
except ImportError:
    def GPU(*args, **kwargs):
        if args and callable(args[0]):
            return args[0]
        return lambda fn: fn


@GPU(duration=1)
def _zerogpu_warmup():
    return "ok"
# ---------------------------------------------------------------------------

RESULTS = json.load(open(Path(__file__).parent / "data" / "results.json"))

# Reddit rows are mock/placeholder (see CLAUDE.md) — never shown as real data.
_SOURCE_MIX = [s for s in RESULTS["source_mix"] if s["source"] != "reddit"]

EXAMPLES = [
    "it's selling expired products through the app so I stopped ordering fruits here",
    "Delivery was 10 minutes late and the delivery guy was rude",
    "I never buy electronics from here, too scared it'll arrive damaged",
    "I only order the same groceries every week, never tried anything else",
]


# ---------------- Tab 1: Live Extractor ----------------
def run_extract(review_text):
    if not review_text or not review_text.strip():
        return "_Enter a review above and click Extract._"
    if "GROQ_API_KEY" not in os.environ:
        return "**Error:** `GROQ_API_KEY` is not configured on the server (add it in Settings → Secrets)."
    try:
        r = extract_one(review_text)
    except Exception as e:  # noqa: BLE001
        return f"**Error:** {e}"

    passed = r.get("mentions_category_behavior")
    gate = ("### ✅ Gate PASSED — relevant to category-adoption behavior"
            if passed else
            "### ⛔ Gate REJECTED — general service complaint, not category behavior")
    if not passed:
        return (gate + "\n\nThe Two-Step Gated Schema drops this before theme clustering — "
                "exactly how the pipeline filters out refund/delivery/pricing noise that isn't "
                "tied to trying or avoiding a category.")
    return f"""{gate}

| Field | Value |
|---|---|
| **behavior_type** | `{r.get('behavior_type')}` |
| **category** | `{r.get('category_mentioned')}` |
| **sentiment** | `{r.get('sentiment')}` |
| **confidence** | `{r.get('confidence')}` |
| **underlying_reason** | {r.get('underlying_reason')} |
| **model** | `{r.get('_model')}` |
"""


# ---------------- Tab 2: Results Explorer ----------------
def _results_markdown():
    f = RESULTS["funnel"]
    md = [
        "## The real discovery-engine output",
        "*Aggregate results from the full pipeline run — real data, not synthetic.*\n",
        "### Pipeline funnel",
        f"**{f['raw_reviews']:,}** raw reviews → **{f['filtered_reviews']:,}** filtered "
        f"→ **{f['gate_pass']:,}** gate-passing extractions "
        f"(~{round(100*f['gate_pass']/f['filtered_reviews'])}% of filtered)\n",
        "**Sources:** " + ", ".join(f"{s['source']} ({s['n']:,})" for s in _SOURCE_MIX) + "\n",
        "### Ranked themes (deterministic, DB-backed evidence counts)",
        "| Theme | Segment | Evidence | Share of gate-pass |",
        "|---|---|---:|---:|",
    ]
    for t in RESULTS["themes"]:
        md.append(f"| **{t['theme_name']}** | {t['user_segment']} | "
                  f"{t['evidence_count']:,} | {round(100*t['evidence_share'])}% |")

    top = RESULTS["themes"][0]
    md.append(f"\n### Sample real evidence — {top['theme_name']}")
    for ev in top["sample_evidence"]:
        md.append(f"> \"{ev['review'].strip()}\"  \n"
                  f"— *{ev['source']}, category: {ev['category']}, {ev['behavior_type']}*")

    v = RESULTS["validation"]
    conf = v["breakdown"].get("confirmed", 0)
    md.append(f"\n### LLM-judge validation (held-out theme-relevant sample)")
    md.append(f"**{conf}/{v['total']} confirmed**, "
              f"{v['breakdown'].get('unclear', 0)} unclear, "
              f"{v['breakdown'].get('contradicted', 0)} contradicted.")

    md.append("\n### Earnings-call corroboration (Eternal, Blinkit's parent)")
    for d in RESULTS["company_disclosures"]:
        md.append(f"> \"{d['content_snippet'].strip()}\"  \n— *{d['source_document']}*")

    return "\n".join(md)


with gr.Blocks(title="Blinkit Discovery Engine") as demo:
    gr.Markdown(
        "# 🔍 Blinkit Category-Adoption Discovery Engine\n"
        "Part 1 of the fellowship project — an AI engine that mines ~15.8k public Blinkit "
        "reviews to find **why users don't explore new categories**. Try the core extraction "
        "step live, or explore the real aggregate findings."
    )
    with gr.Tab("Live Extractor"):
        gr.Markdown(
            "Paste any review. The **Two-Step Gated Schema** first decides if it's about "
            "category-adoption behavior at all (Step 1 gate), then extracts structured fields "
            "(Step 2). This is the exact prompt from the batch pipeline, on Groq "
            "`llama-3.1-8b-instant`."
        )
        inp = gr.Textbox(label="Review text", lines=3, placeholder="e.g. I stopped buying fruits here after getting a rotten batch")
        btn = gr.Button("Extract", variant="primary")
        gr.Examples(EXAMPLES, inputs=inp)
        out = gr.Markdown()
        btn.click(run_extract, inputs=inp, outputs=out)
    with gr.Tab("Results Explorer"):
        gr.Markdown(_results_markdown())


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
