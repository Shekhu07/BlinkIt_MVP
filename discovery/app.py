"""Discovery-Workflow demo — the second required live link (Part 1 AI engine).

Three tabs:
  1. Live Extractor    — paste any review, watch the REAL Two-Step Gated extraction run
                         (live Groq call, not a canned/heuristic response).
  2. Bulk Run           — upload up to 50 of your own reviews and push them through the
                         SAME guardrails (dedup -> heuristic filter -> gate -> grouping);
                         every dropped row is reported with the guardrail that dropped it.
                         Results are the evaluator's own run and never touch the real
                         Part 1 numbers.
  3. Results Explorer   — the REAL aggregate findings, rendered from data/results.json.

Visual design imported from the "Blinkit Discovery Engine redesign" Claude Design project.
Design chrome is reproduced faithfully; all NUMBERS are taken from the real pipeline export,
never from the mockup's placeholder values (see README "Design vs. data" note).

Deployed on HuggingFace Gradio SDK (free). Local run:
    python app.py     -> http://127.0.0.1:7860
"""
import html
import json
import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

import batch as batchmod
from batch import MAX_ROWS, UploadError
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
SOURCE_MIX = [s for s in RESULTS["source_mix"] if s["source"] != "reddit"]

# Display labels only — counts are never altered. `unknown_master` is the catch-all bucket in
# ingest_master_json.py for rows in MASTER_Blinkit_Reviews.json that carry no `source` field at
# all (2,532 rows). Showing the raw internal key implied a named platform; "source not recorded"
# is what it actually is. These rows are real scraped reviews with unrecorded provenance — not
# mock — so they stay in the corpus and in the funnel rather than being hidden.
SOURCE_LABELS = {"unknown_master": "source not recorded"}

EXAMPLES = [
    "it's selling expired products through the app so I stopped ordering fruits here",
    "Delivery was 10 minutes late and the delivery guy was rude",
    "I never buy electronics from here, too scared it'll arrive damaged",
    "I only order the same groceries every week, never tried anything else",
]

INK, YELLOW, BG = "#141414", "#f8cb46", "#f6f6f4"

# Fonts must be injected into <head> — Gradio ignores @import inside the css= param.
HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
"""

# Theme + embed bootstrap.
#
# The previous version unconditionally ran location.replace() to append ?__theme=light.
# Inside HuggingFace's Space page that is a navigation *within the iframe*, and HF sizes
# that iframe with iframe-resizer while setting scrolling="no" and overflow:hidden — so a
# reload can leave the parent holding a stale height, and because the iframe cannot scroll,
# whatever falls past that height is unreachable rather than merely below the fold. That is
# the "page won't scroll / data looks incomplete" symptom, and it needs no redirect to be
# fixed: the CSS above already pins the light surface with !important, verified to hold even
# when the container carries Gradio's .dark class.
#
# So redirect only when we are the top-level document (the direct *.hf.space URL, where it
# is harmless), and inside an iframe instead keep prodding iframe-resizer to re-measure:
# after webfonts swap (text metrics change, so height changes), after tab switches (DOM
# mutations), and on a short settle schedule for the initial paint.
BOOT_JS = """
function(){
  var inIframe = false;
  try { inIframe = window.self !== window.top; } catch (e) { inIframe = true; }
  if (!inIframe) {
    var u = new URL(window.location);
    if (u.searchParams.get('__theme') !== 'light') {
      u.searchParams.set('__theme', 'light');
      window.location.replace(u.href);
      return;
    }
  }
  var nudge = function () {
    try {
      if (window.parentIFrame && typeof window.parentIFrame.size === 'function') {
        window.parentIFrame.size();
      } else {
        window.dispatchEvent(new Event('resize'));
      }
    } catch (e) {}
  };
  [0, 350, 900, 1800, 3500, 6000].forEach(function (ms) { setTimeout(nudge, ms); });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { nudge(); setTimeout(nudge, 250); });
  }
  window.addEventListener('load', function () { setTimeout(nudge, 200); });
  var timer = null;
  var mo = new MutationObserver(function () {
    clearTimeout(timer);
    timer = setTimeout(nudge, 200);
  });
  mo.observe(document.body, { childList: true, subtree: true });
}
"""

CSS = """
:root{color-scheme:light}
html,body,.gradio-container,.dark .gradio-container{background:#f6f6f4 !important}
/* THEME-PROOFING — must stay ABOVE the class rules below.
   Every element defaults to our ink, so nothing can inherit Gradio's theme colour
   (that is what made headings invisible). Deliberately NOT !important: our own
   class rules below and inline styles (e.g. white text on the dark cards) still
   win normally. This holds even if the force-light redirect is blocked in HF's
   iframe, so the design no longer depends on it. */
.gradio-container *,.dark .gradio-container *{color:#141414}
body,.gradio-container,.gradio-container *,button,input,textarea{
  font-family:'Plus Jakarta Sans',system-ui,-apple-system,sans-serif !important}
.gradio-container{max-width:1100px !important;margin:0 auto !important;padding:0 !important;
  color:#141414 !important;box-shadow:0 0 0 1px #ececec}
.gradio-container .prose,.gradio-container p,.gradio-container span,.gradio-container div{color:inherit}
footer,.footer,.show-api,.built-with,.settings{display:none !important}

/* strip Gradio chrome so our own cards are the only surfaces */
.block,.form,.gr-box,.gr-group,.panel,.gr-panel,.styler,.wrap.svelte-1parkyl{
  background:transparent !important;border:none !important;box-shadow:none !important;padding:0 !important}
.gradio-container .gap{gap:0 !important}
.dc-body .block{margin:0 !important}

/* header */
.dc-head{background:#f8cb46 !important;padding:22px 40px !important;align-items:center !important;
  border:none !important;border-radius:0 !important;flex-wrap:wrap;gap:16px !important;margin:0 !important}
.dc-head .block{background:transparent !important}
.dc-logo.dc-logo.dc-logo{width:46px;height:46px;border-radius:13px;background:#141414;display:flex;
  align-items:center;justify-content:center;font-size:25px;flex:none;color:#f8cb46}
.dc-brand{display:flex;align-items:center;gap:16px}
.dc-title.dc-title.dc-title{font-weight:800;font-size:23px;letter-spacing:-.02em;line-height:1;color:#141414}
.dc-title span{font-weight:600;opacity:.72}
.dc-sub.dc-sub.dc-sub{font-size:13px;font-weight:600;color:#5a4b06;margin-top:5px}

/* pill tabs inside the header */
.dc-tabs{background:rgba(20,20,20,.10);padding:5px !important;border-radius:12px !important;
  gap:8px !important;flex:none !important;min-width:0 !important;width:auto !important}
.dc-tabs{justify-content:flex-end !important;flex-wrap:nowrap !important}
.dc-tabs button{border:none !important;box-shadow:none !important;font-size:13.5px !important;
  padding:9px 18px !important;border-radius:9px !important;min-width:0 !important;
  white-space:nowrap !important;width:auto !important;flex:none !important}
.dc-tabs button.secondary{background:transparent !important;color:#4a3d05 !important;font-weight:600 !important}
.dc-tabs button.primary{background:#141414 !important;color:#f8cb46 !important;font-weight:700 !important}

.dc-body{padding:34px 40px 64px !important}
.dc-eyebrow.dc-eyebrow.dc-eyebrow{font-size:12px;font-weight:800;letter-spacing:.12em;color:#4f440d}
.dc-h2.dc-h2.dc-h2{font-weight:700;font-size:20px;letter-spacing:-.01em;color:#141414}
.dc-lede{font-size:14px;color:#4a4a4a !important;max-width:640px;line-height:1.5;margin:8px 0 4px}
.dc-lede code{font-family:'JetBrains Mono',monospace !important;font-size:12px;background:#efeee9;
  padding:2px 6px;border-radius:5px}
.dc-card{background:#fff !important;border-radius:18px !important;border:1px solid #ececec !important;
  padding:22px !important;box-shadow:0 2px 12px rgba(0,0,0,.04) !important}
.dc-card>*{background:transparent !important}
.dc-label.dc-label.dc-label{font-size:12px;font-weight:700;color:#6b6b6b;margin-bottom:9px;letter-spacing:.02em}
@keyframes fadeup{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.dc-anim{animation:fadeup .3s ease}

/* inputs */
#rev textarea{background:#faf9f6 !important;border:1px solid #eee !important;border-radius:12px !important;
  padding:14px 16px !important;font-size:14px !important;line-height:1.5 !important;color:#333 !important;
  min-height:96px;box-shadow:none !important}
#rev textarea::placeholder{color:#b3b3b3 !important}
#go{background:#f8cb46 !important;color:#141414 !important;font-weight:800 !important;font-size:14px !important;
  padding:11px 28px !important;border:none !important;border-radius:12px !important;box-shadow:none !important;
  margin:14px 0 0 auto !important;width:auto !important;min-width:0 !important;flex:none !important;
  align-self:flex-end !important;display:block !important}
.ex-btn{border:1px solid #eee !important;border-radius:10px !important;padding:10px 13px !important;
  font-size:13px !important;color:#444 !important;background:#fcfcfa !important;text-align:left !important;
  font-weight:500 !important;line-height:1.4 !important;box-shadow:none !important;width:100% !important;
  justify-content:flex-start !important;display:block !important;margin-bottom:8px !important;
  white-space:normal !important;height:auto !important;min-height:0 !important}
.ex-btn:hover{border-color:#f8cb46 !important;background:#fffdf3 !important}

/* bulk run */
#bulk textarea{background:#faf9f6 !important;border:1px solid #eee !important;border-radius:12px !important;
  padding:14px 16px !important;font-family:'JetBrains Mono',monospace !important;font-size:12px !important;
  line-height:1.55 !important;color:#333 !important;min-height:240px;box-shadow:none !important}
#bulk textarea::placeholder{color:#b3b3b3 !important}
#gobulk{background:#f8cb46 !important;color:#141414 !important;font-weight:800 !important;
  font-size:14px !important;padding:11px 28px !important;border:none !important;border-radius:12px !important;
  box-shadow:none !important;margin:14px 0 0 !important;width:auto !important;min-width:0 !important;
  flex:none !important}
#sample{background:#fcfcfa !important;border:1px solid #eee !important;border-radius:12px !important;
  color:#444 !important;font-weight:600 !important;font-size:13px !important;padding:11px 18px !important;
  box-shadow:none !important;margin:14px 0 0 10px !important;width:auto !important;min-width:0 !important;
  flex:none !important}
#sample:hover{border-color:#f8cb46 !important;background:#fffdf3 !important}
.dc-rows{display:flex;flex-direction:column;gap:8px;max-height:420px;overflow-y:auto;padding-right:4px}
.dc-row{border:1px solid #ececec;border-radius:12px;padding:12px 14px;background:#fff}
.dc-row.drop{background:#fdf7f7;border-color:#eedada}
.dc-quote.dc-quote.dc-quote{font-size:12.5px;color:#3d3d3d;line-height:1.45}
.dc-why.dc-why.dc-why{font-size:11.5px;color:#8a5a5a;margin-top:6px;line-height:1.45}
.dc-stage.dc-stage.dc-stage{font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:600;color:#a63c3c;
  letter-spacing:.02em}

/* loading state — Gradio's default spinner is hidden by our chrome reset */
.dc-body .generating,.dc-body .progress-text{background:transparent !important;color:#756512 !important;
  font-size:12px !important;font-weight:700 !important;letter-spacing:.06em}

/* responsive — the design is a fixed 1100px canvas; collapse gracefully below it */
@media (max-width:900px){
  .dc-head{padding:18px 20px !important}
  .dc-body{padding:24px 20px 10px !important}
  .dc-title{font-size:20px}
  .dc-sub{font-size:12px}
  .dc-grid3{grid-template-columns:1fr !important}
  .dc-funnel{flex-direction:column !important}
  .dc-funnel .dc-arrow{transform:rotate(90deg);align-self:center}
  .dc-cols{flex-direction:column !important}
}
@media (max-width:620px){
  .dc-head{flex-direction:column;align-items:flex-start !important}
  .dc-tabs{width:100% !important;justify-content:flex-start !important}
}
"""


def esc(t):
    return html.escape(str(t) if t is not None else "")


# ---------------- Tab 1: Live Extractor ----------------
EMPTY_HTML = """
<div style="border:1.5px dashed #e0e0e0;border-radius:18px;padding:40px 24px;text-align:center;color:#6f6f6f">
  <div style="font-size:34px;color:#a87c0c">⚡</div>
  <div style="font-size:13.5px;margin-top:10px;line-height:1.5;color:#6f6f6f">Enter a review and hit Extract to watch the<br>Two-Step Gated Schema run.</div>
</div>"""


def _err(msg):
    return (f'<div class="dc-anim" style="border:1.5px solid #d8b4b4;background:#fdf5f5;border-radius:16px;'
            f'padding:20px 22px;color:#a63c3c;font-size:13.5px"><b>Error:</b> {esc(msg)}</div>')


def run_extract(review_text):
    if not review_text or not review_text.strip():
        return EMPTY_HTML
    if "GROQ_API_KEY" not in os.environ:
        return _err("GROQ_API_KEY is not configured on the server (add it in Settings → Secrets).")
    try:
        r = extract_one(review_text)   # REAL Groq call — not a canned response
    except Exception as e:  # noqa: BLE001
        return _err(e)

    if not r.get("mentions_category_behavior"):
        return """
<div class="dc-anim" style="border:1.5px solid #d8b4b4;background:#fdf5f5;border-radius:16px;padding:20px 22px">
  <div style="display:flex;align-items:center;gap:9px">
    <span style="width:24px;height:24px;border-radius:50%;background:#c85a5a;color:#fff;display:flex;
      align-items:center;justify-content:center;font-size:13px;font-weight:800">⛔</span>
    <span style="font-weight:800;font-size:14px;color:#a63c3c">GATE REJECTED</span></div>
  <div style="font-size:13.5px;color:#7a4a4a;margin-top:11px;line-height:1.55">General service complaint, not
    category behavior. The Two-Step Gated Schema drops this before clustering — exactly how the pipeline filters
    out refund / delivery / pricing noise that isn't tied to trying or avoiding a category.</div>
</div>"""

    chips = [("#141414", "#f8cb46", r.get("behavior_type")),
             ("#fdf3d0", "#7a6410", r.get("category_mentioned")),
             ("#fde8e8", "#b23c3c", r.get("sentiment")),
             ("#e7f5ee", "#0c7d3c", f"{r.get('confidence')} confidence")]
    chip_html = "".join(
        f'<span style="background:{bg};color:{fg};font-size:12px;font-weight:700;padding:6px 12px;'
        f'border-radius:20px">{esc(v)}</span>' for bg, fg, v in chips if v not in (None, ""))

    return f"""
<div class="dc-anim" style="display:flex;flex-direction:column;gap:14px">
  <div style="border:1.5px solid #12a150;background:#f2fbf5;border-radius:16px;padding:18px 20px">
    <div style="display:flex;align-items:center;gap:9px">
      <span style="width:24px;height:24px;border-radius:50%;background:#12a150;color:#fff;display:flex;
        align-items:center;justify-content:center;font-size:13px;font-weight:800">✓</span>
      <span style="font-weight:800;font-size:14px;color:#0c7d3c">STEP 1 · GATE PASSED</span></div>
    <div style="font-size:13px;color:#3a5a45;margin-top:9px;line-height:1.5">Mentions category-adoption behavior
      — kept for theme clustering.</div>
  </div>
  <div style="border:1px solid #ececec;background:#fff;border-radius:16px;padding:18px 20px;
    box-shadow:0 2px 12px rgba(0,0,0,.04)">
    <div style="font-weight:800;font-size:13px;color:#6b6b6b;letter-spacing:.02em;margin-bottom:12px">
      STEP 2 · STRUCTURED FIELDS</div>
    <div style="display:flex;flex-wrap:wrap;gap:7px">{chip_html}</div>
    <div style="font-size:13px;color:#555;margin-top:13px;line-height:1.5"><b>Underlying reason:</b>
      {esc(r.get('underlying_reason'))}</div>
    <div style="font-size:11px;color:#6f6f6f;margin-top:12px;font-family:'JetBrains Mono',monospace">
      model · {esc(r.get('_model'))}</div>
  </div>
</div>"""


# ---------------- Tab 2: Bulk Run (the EVALUATOR's own data) ----------------
BULK_PLACEHOLDER = (
    "Paste up to 50 reviews, one per line — e.g.\n\n"
    "I stopped buying fruits here after a rotten batch arrived\n"
    "Delivery was late and the rider was rude\n"
    "Never tried their pet range, no ratings on the items")

# Deliberately mixed: contains a duplicate, two sub-5-word rows, a 5-star row and two
# pure service complaints, so every guardrail visibly fires on one click.
SAMPLE_BULK = """content,rating,source,author
"it's selling expired products through the app so I stopped ordering fruits here",1,playstore,anon1
"Delivery was 10 minutes late and the delivery guy was rude",2,playstore,anon2
"I never buy electronics from here, too scared it'll arrive damaged",2,maps,anon3
"good",5,playstore,anon4
"nice app",4,playstore,anon5
"Absolutely love this app, everything arrives on time and fresh always",5,playstore,anon6
"it's selling expired products through the app so I stopped ordering fruits here",1,playstore,anon1
"I only order the same groceries every week, never tried anything else on the app",3,maps,anon7
"Refund has not been processed for 15 days now, customer care is useless",1,mouthshut,anon8
"After the dairy I ordered arrived spoilt I stopped buying any perishables from quick commerce",1,mouthshut,anon9
"Wanted to try their pet food range but reviews on the items are missing so I skipped it",3,maps,anon10
"""

BULK_EMPTY = f"""
<div style="border:1.5px dashed #e0e0e0;border-radius:18px;padding:40px 24px;text-align:center;color:#6f6f6f">
  <div style="font-size:34px;color:#a87c0c">📄</div>
  <div style="font-size:13.5px;margin-top:10px;line-height:1.5;color:#6f6f6f">Paste up to {MAX_ROWS} reviews to run
    them through<br>dedup → heuristic filter → gate → grouping.</div>
</div>"""


def _step_card(n, label, value, sub, dark=False):
    bg, bd = ("#141414", "#141414") if dark else ("#fff", "#ececec")
    num = YELLOW if dark else INK
    lab = "#cfcfcf" if dark else "#6b6b6b"
    return (f'<div style="flex:1;min-width:120px;background:{bg};border:1px solid {bd};border-radius:16px;'
            f'padding:15px 17px">'
            f'<div style="font-size:10.5px;font-weight:700;letter-spacing:.1em;color:#8a8a8a">{esc(n)}</div>'
            f'<div style="font-size:26px;font-weight:800;letter-spacing:-.02em;color:{num};margin-top:5px">{value:,}</div>'
            f'<div style="font-size:12px;color:{lab};font-weight:600;margin-top:2px">{esc(label)}</div>'
            f'<div style="font-size:11px;color:#8a8a8a;margin-top:5px;line-height:1.4">{esc(sub)}</div></div>')


def _row_card(r, dropped):
    body = esc((r["content"] or "")[:220] + ("…" if len(r["content"] or "") > 220 else ""))
    if dropped:
        return (f'<div class="dc-row drop"><div class="dc-stage">{esc(r["stage"])}</div>'
                f'<div class="dc-quote" style="margin-top:5px">“{body}”</div>'
                f'<div class="dc-why">{esc(r["reason"])}</div></div>')
    chips = "".join(
        f'<span style="background:{bg};color:{fg};font-size:11px;font-weight:700;padding:4px 9px;'
        f'border-radius:20px">{esc(v)}</span>'
        for bg, fg, v in (("#141414", YELLOW, r.get("behavior_type")),
                          ("#fdf3d0", "#7a6410", r.get("category")),
                          ("#fde8e8", "#b23c3c", r.get("sentiment")))
        if v not in (None, ""))
    reason = esc(r.get("underlying_reason") or "")
    return (f'<div class="dc-row"><div class="dc-quote">“{body}”</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:9px">{chips}</div>'
            + (f'<div style="font-size:11.5px;color:#5a6b5f;margin-top:7px;line-height:1.45">'
               f'<b>Reason:</b> {reason}</div>' if reason else "") + "</div>")


def run_bulk(text, progress=gr.Progress()):
    if not text or not text.strip():
        return BULK_EMPTY
    if "GROQ_API_KEY" not in os.environ:
        return _err("GROQ_API_KEY is not configured on the server (add it in Settings → Secrets).")
    try:
        res = batchmod.run(text, progress=progress)
    except UploadError as e:
        return _err(e)
    except Exception as e:  # noqa: BLE001
        return _err(f"Unexpected failure: {e}")

    total, n_drop = res["total"], len(res["dropped"])
    n_kept, n_pass, n_rej = len(res["kept"]), len(res["passed"]), len(res["rejected"])

    funnel = "".join((
        _step_card("PASTED", "rows submitted", total, f"cap {MAX_ROWS}"),
        _step_card("STAGE 0–1", "after guardrails", n_kept,
                   f"{n_drop} dropped by dedup / heuristic filter"),
        _step_card("STAGE 2", "gate-passing", n_pass,
                   f"{n_rej} rejected by the relevance gate", dark=True)))

    rate = f"{round(100 * n_pass / n_kept)}%" if n_kept else "—"
    combo_rows = "".join(
        f'<div style="display:flex;justify-content:space-between;font-size:12.5px;padding:7px 0;'
        f'border-bottom:1px solid #f2f2f2"><span style="color:#3d3d3d">{esc(c["category"])} · '
        f'{esc(c["behavior_type"])}</span><span style="font-weight:700;color:#141414">{c["count"]}</span></div>'
        for c in res["combos"]) or '<div style="font-size:12.5px;color:#6f6f6f">No rows passed the gate.</div>'

    dropped_html = "".join(_row_card(r, True) for r in res["dropped"] + res["rejected"]) or \
        '<div style="font-size:12.5px;color:#6f6f6f">Nothing was dropped — every row cleared all guardrails.</div>'
    kept_html = "".join(_row_card(r, False) for r in res["passed"]) or \
        '<div style="font-size:12.5px;color:#6f6f6f">No rows passed the gate.</div>'

    rating_note = "" if res["has_rating"] else (
        '<div style="font-size:11.5px;color:#8a6a2a;background:#fdf6dd;border:1px solid #f0e2a8;'
        'border-radius:10px;padding:9px 12px;margin-bottom:14px">No <code>rating</code> column found — '
        "the 5-star drop rule could not be applied to this input. All other guardrails ran.</div>")

    return f"""
<div class="dc-anim">
  <div style="background:#fdf6dd;border:1px solid #f0e2a8;border-radius:12px;padding:10px 14px;
    font-size:11.5px;color:#756512;font-weight:600;margin-bottom:16px">YOUR RUN — scoped to the reviews you
    just pasted. It does not modify the real Part 1 corpus or the numbers in Results Explorer.</div>
  {rating_note}
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:8px">{funnel}</div>
  <div style="font-size:11.5px;color:#6f6f6f;margin:10px 0 20px">Gate pass rate on your input:
    <b style="color:#141414">{rate}</b> · the full 15,820-review corpus ran at ~23% ·
    model <span style="font-family:'JetBrains Mono',monospace">{esc(res['model'])}</span></div>

  <div class="dc-cols" style="display:flex;gap:14px;align-items:flex-start">
    <div style="flex:1;min-width:0;background:#fff;border:1px solid #ececec;border-radius:18px;padding:20px 22px">
      <div style="font-weight:800;font-size:13.5px;color:#141414;margin-bottom:4px">Dropped ({n_drop + n_rej})</div>
      <div style="font-size:11.5px;color:#6f6f6f;margin-bottom:13px">Each row names the guardrail that removed it.</div>
      <div class="dc-rows">{dropped_html}</div></div>
    <div style="flex:1;min-width:0;background:#fff;border:1px solid #ececec;border-radius:18px;padding:20px 22px">
      <div style="font-weight:800;font-size:13.5px;color:#141414;margin-bottom:4px">Gate-passing ({n_pass})</div>
      <div style="font-size:11.5px;color:#6f6f6f;margin-bottom:13px">Structured fields from Step 2.</div>
      <div class="dc-rows">{kept_html}</div></div>
  </div>

  <div style="background:#fff;border:1px solid #ececec;border-radius:18px;padding:20px 22px;margin-top:14px">
    <div style="font-weight:800;font-size:13.5px;color:#141414;margin-bottom:4px">Category × behavior grouping</div>
    <div style="font-size:11.5px;color:#6f6f6f;margin-bottom:10px">Deterministic row counts, same as
      <code>cluster_themes.py</code>. Theme <i>naming</i> is deliberately not run on a sample this small —
      naming macro-themes off ≤{MAX_ROWS} rows would manufacture findings.</div>
    {combo_rows}</div>
</div>"""


# ---------------- Tab 3: Results Explorer (REAL numbers) ----------------
def results_html():
    f = RESULTS["funnel"]
    themes = RESULTS["themes"]
    v = RESULTS["validation"]
    conf = v["breakdown"].get("confirmed", 0)
    contra = v["breakdown"].get("contradicted", 0)
    pct = round(100 * conf / v["total"]) if v["total"] else 0
    dash = 251
    offset = round(dash * (1 - pct / 100))

    # funnel widths relative to raw
    w_filt = round(100 * f["filtered_reviews"] / f["raw_reviews"])
    w_gate = round(100 * f["gate_pass"] / f["raw_reviews"])

    theme_rows = []
    top_share = themes[0]["evidence_share"] if themes else 1
    for i, t in enumerate(themes):
        share = round(100 * t["evidence_share"])
        fill = YELLOW if i == 0 else ("#efd582" if i == 1 else "#e9d9a0")
        name = (f'<b style="color:#141414">{esc(t["theme_name"])}</b>' if i == 0
                else f'<span style="color:#3d3d3d">{esc(t["theme_name"])}</span>')
        weight = "700" if i == 0 else "600"
        color = "#141414" if i == 0 else "#666"
        theme_rows.append(f"""
      <div><div style="display:flex;justify-content:space-between;font-size:13.5px;margin-bottom:6px">
        {name}<span style="font-weight:{weight};color:{color}">{share}% · {t['evidence_count']:,}</span></div>
        <div style="height:15px;border-radius:8px;background:#f3f3f3;overflow:hidden">
        <div style="height:100%;width:{share}%;background:{fill};border-radius:8px"></div></div></div>""")

    mx = max(s["n"] for s in SOURCE_MIX)
    shades = ["#141414", "#4a4a4a", "#6a6a6a", "#6b6b6b", "#a0a0a0", "#6f6f6f"]
    src_rows = "".join(f"""
        <div style="display:flex;align-items:center;gap:10px"><span style="width:132px;color:#666">{esc(SOURCE_LABELS.get(s['source'], s['source']))}</span>
        <div style="flex:1;height:11px;background:#f3f3f3;border-radius:6px;overflow:hidden">
        <div style="height:100%;width:{round(100*s['n']/mx)}%;background:{shades[min(i,5)]};border-radius:6px"></div></div>
        <span style="width:52px;text-align:right;color:#6b6b6b;font-size:11.5px">{s['n']:,}</span></div>"""
        for i, s in enumerate(SOURCE_MIX))

    beh = RESULTS["behavior_distribution"]
    tot_b = sum(b["n"] for b in beh) or 1
    bshades = [YELLOW, "#efd582", "#e2ce80", "#d8c273", "#cbb96a"]
    bar = "".join(f'<div style="width:{100*b["n"]/tot_b:.1f}%;background:{bshades[min(i,4)]}"></div>'
                  for i, b in enumerate(beh))
    legend = "".join(
        f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:{bshades[min(i,4)]};border:1px solid rgba(0,0,0,.22);vertical-align:middle"></span> {esc(b["behavior_type"])} — '
        f'{round(100*b["n"]/tot_b)}%</span>' for i, b in enumerate(beh))

    top = themes[0]
    seen, uniq = set(), []
    for e in top["sample_evidence"]:
        key = e["review"].strip().lower()[:40]
        if key not in seen:
            seen.add(key); uniq.append(e)
    ev = "".join(f"""
        <div style="border-left:3px solid {YELLOW};padding:2px 0 2px 14px">
          <div style="font-family:'Newsreader',serif;font-size:16px;font-style:italic;color:#2a251b;line-height:1.5">
            “{esc(e['review'].strip())}”</div>
          <div style="font-size:11.5px;color:#6f6f6f;margin-top:4px">{esc(e['source'])} · {esc(e['category'])} · {esc(e['behavior_type'])}</div>
        </div>""" for e in uniq[:3])

    # Only a row the judge actually scored as corroborating may be labelled as such.
    # Every shipped row is signal_type "unrelated" — the Q4FY26 call speaks to assortment
    # expansion, never to product-quality or refund friction. Labelling it "CORROBORATED"
    # would claim support the pipeline explicitly did not find (see problem_statement.md §5).
    _corroborating = [x for x in RESULTS["company_disclosures"]
                      if (x.get("signal_type") or "").lower() == "corroborates"]
    d = _corroborating[0] if _corroborating else (
        RESULTS["company_disclosures"][0] if RESULTS["company_disclosures"] else None)
    corro = ""
    if d:
        if _corroborating:
            _label = f"CORROBORATED BY EARNINGS CALL — {esc(d['source_document'].replace('_',' '))}"
            _caveat = ""
        else:
            _label = f"EARNINGS-CALL CONTEXT — {esc(d['source_document'].replace('_',' '))}"
            _caveat = ("""
      <div style="font-size:12px;line-height:1.45;color:#6b6144;margin-top:10px">
        Growth-narrative context, not scored as corroboration: the call ties growth to
        non-grocery assortment expansion but does not discuss product-quality or refund
        friction. The link to this project's cause is ours, not the company's.</div>""")
        corro = f"""
    <div style="background:#fdf6dd;border:1px solid #f0e2a8;border-radius:18px;padding:20px 22px">
      <div style="font-size:11px;font-weight:700;letter-spacing:.12em;color:#756512;margin-bottom:9px">
        {_label}</div>
      <div style="font-family:'Newsreader',serif;font-size:17px;line-height:1.5;color:#3a3320">
        “{esc(d['content_snippet'].strip())}”</div>{_caveat}
    </div>"""

    return f"""
<div>
  <div style="display:flex;align-items:center;gap:11px;margin-bottom:6px">
    <span class="dc-eyebrow">THE FINDINGS</span>
    <span class="dc-h2">What {f['raw_reviews']:,} reviews actually said</span></div>
  <div class="dc-lede" style="margin-bottom:24px">Aggregate output of the full pipeline run — deterministic,
    DB-backed evidence counts. Not synthetic.</div>

  <div class="dc-funnel" style="display:flex;gap:14px;align-items:stretch;margin-bottom:16px">
    <div style="flex:1;background:#fff;border:1px solid #ececec;border-radius:16px;padding:18px 20px">
      <div style="font-size:30px;font-weight:800;letter-spacing:-.02em;color:#141414">{f['raw_reviews']:,}</div>
      <div style="font-size:12.5px;color:#6b6b6b;font-weight:600;margin-top:3px">raw reviews scraped</div>
      <div style="height:9px;border-radius:5px;background:{YELLOW};margin-top:14px"></div></div>
    <div class="dc-arrow" style="display:flex;align-items:center;color:#7d7d7d;font-size:22px">→</div>
    <div style="flex:1;background:#fff;border:1px solid #ececec;border-radius:16px;padding:18px 20px">
      <div style="font-size:30px;font-weight:800;letter-spacing:-.02em;color:#141414">{f['filtered_reviews']:,}</div>
      <div style="font-size:12.5px;color:#6b6b6b;font-weight:600;margin-top:3px">after heuristic filter</div>
      <div style="height:9px;border-radius:5px;background:#f2d979;margin-top:14px;width:{w_filt}%"></div></div>
    <div class="dc-arrow" style="display:flex;align-items:center;color:#7d7d7d;font-size:22px">→</div>
    <div style="flex:1;background:#141414;border-radius:16px;padding:18px 20px;color:#fff">
      <div style="font-size:30px;font-weight:800;letter-spacing:-.02em;color:{YELLOW}">{f['gate_pass']:,}</div>
      <div style="font-size:12.5px;color:#cfcfcf;font-weight:600;margin-top:3px">gate-passing extractions</div>
      <div style="height:9px;border-radius:5px;background:{YELLOW};margin-top:14px;width:{max(w_gate,6)}%"></div></div>
  </div>

  <div style="background:#fff;border:1px solid #ececec;border-radius:18px;padding:22px 24px;margin-bottom:16px">
    <div style="font-weight:800;font-size:15px;margin-bottom:18px;color:#141414">Ranked themes
      <span style="font-weight:600;color:#6f6f6f;font-size:12.5px">· share of gate-passing extractions</span></div>
    <div style="display:flex;flex-direction:column;gap:15px">{''.join(theme_rows)}</div>
    <div style="font-size:11.5px;color:#6f6f6f;margin-top:16px">All counts are DB row-counts from the pipeline
      export — never LLM-estimated.</div>
  </div>

  <div class="dc-grid3" style="display:grid;grid-template-columns:1.3fr 1fr .75fr;gap:14px;margin-bottom:16px">
    <div style="background:#fff;border:1px solid #ececec;border-radius:18px;padding:20px 22px">
      <div style="font-weight:800;font-size:13.5px;margin-bottom:14px;color:#141414">Source mix</div>
      <div style="display:flex;flex-direction:column;gap:10px;font-size:12.5px">{src_rows}</div>
      <div style="font-size:11px;color:#6f6f6f;margin-top:13px;line-height:1.45">“Source not
        recorded” = real scraped reviews whose originating platform was not captured in the
        source dump. Kept in the corpus and the funnel rather than dropped.</div></div>
    <div style="background:#fff;border:1px solid #ececec;border-radius:18px;padding:20px 22px">
      <div style="font-weight:800;font-size:13.5px;margin-bottom:14px;color:#141414">Behavior type</div>
      <div style="display:flex;height:14px;border-radius:7px;overflow:hidden">{bar}</div>
      <div style="display:flex;flex-direction:column;gap:6px;margin-top:12px;font-size:12px;color:#666">{legend}</div></div>
    <div style="background:#141414;border-radius:18px;padding:20px;color:#fff;display:flex;flex-direction:column;
      align-items:center;justify-content:center">
      <svg width="100" height="100" viewBox="0 0 96 96"><circle cx="48" cy="48" r="40" fill="none" stroke="#333" stroke-width="12"/>
      <circle cx="48" cy="48" r="40" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round"
        stroke-dasharray="{dash}" stroke-dashoffset="{offset}" transform="rotate(-90 48 48)"/></svg>
      <div style="font-size:27px;font-weight:800;margin-top:-64px;color:{YELLOW}">{pct}%</div>
      <div style="font-size:11px;color:#cfcfcf;margin-top:44px;text-align:center;font-weight:600">
        LLM-judge validation<br>{conf}/{v['total']} confirmed · {contra} contradicted</div></div>
  </div>

  <div style="background:#fff;border:1px solid #ececec;border-radius:18px;padding:22px 24px;margin-bottom:16px">
    <div style="font-weight:800;font-size:13.5px;margin-bottom:14px;color:#141414">Sample evidence — {esc(top['theme_name'])}</div>
    <div style="display:flex;flex-direction:column;gap:12px">{ev}</div></div>
  {corro}
</div>"""


BRAND = f"""
<div class="dc-brand">
  <div class="dc-logo">⚡</div>
  <div><div class="dc-title">blinkit <span>discovery engine</span></div>
  <div class="dc-sub">Why users don't explore new categories — mined from
    {RESULTS['funnel']['raw_reviews']:,} public reviews</div></div>
</div>"""

FOOTER = """
<div style="padding:18px 40px 26px;border-top:1px solid #ececec;font-size:11.5px;color:#6f6f6f;
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
  <span>Blinkit Category-Adoption Discovery Engine · Part 1</span>
  <span style="font-family:'JetBrains Mono',monospace">Two-Step Gated Schema · Groq llama-3.1-8b-instant</span>
</div>"""


with gr.Blocks(title="Blinkit Discovery Engine", css=CSS, head=HEAD,
               js=BOOT_JS, theme=gr.themes.Base()) as demo:
    # Font <link> repeated in-body: Gradio's head= does not always reach the served
    # page on Spaces, and browsers honour stylesheet links in the body too.
    gr.HTML(HEAD)
    # ---- header: brand + pill tabs, all inside the yellow bar ----
    with gr.Row(elem_classes="dc-head"):
        gr.HTML(BRAND)
        with gr.Row(elem_classes="dc-tabs"):
            t_ex = gr.Button("Live Extractor", variant="primary", size="sm")
            t_bulk = gr.Button("Bulk Run", variant="secondary", size="sm")
            t_res = gr.Button("Results Explorer", variant="secondary", size="sm")

    # ---- panel 1: live extractor ----
    with gr.Column(elem_classes="dc-body", visible=True) as panel_ex:
        gr.HTML(
            '<div style="display:flex;align-items:center;gap:11px;margin-bottom:8px">'
            '<span class="dc-eyebrow">STEP DEMO</span>'
            '<span class="dc-h2">Two-Step Gated extraction, live</span></div>'
            '<div class="dc-lede" style="margin-bottom:18px">Paste a review. Step 1 gates it on whether '
            "it's about category-adoption behavior at all; Step 2 extracts structured fields. Exact prompt "
            'from the batch pipeline, on Groq <code>llama-3.1-8b-instant</code>.</div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, elem_classes="dc-card"):
                gr.HTML('<div class="dc-label">REVIEW TEXT</div>')
                inp = gr.Textbox(
                    elem_id="rev", show_label=False, lines=4, container=False,
                    placeholder="e.g. I stopped buying fruits here after getting a rotten batch")
                btn = gr.Button("Extract →", elem_id="go", variant="primary")
                gr.HTML('<div style="font-size:11px;font-weight:700;color:#6f6f6f;letter-spacing:.08em;'
                        'margin:26px 0 10px;clear:both">TRY AN EXAMPLE</div>')
                ex_btns = [gr.Button(e, elem_classes="ex-btn", size="sm") for e in EXAMPLES]
            with gr.Column(scale=1):
                out = gr.HTML(EMPTY_HTML)

    # ---- panel 2: bulk run ----
    with gr.Column(elem_classes="dc-body", visible=False) as panel_bulk:
        gr.HTML(
            '<div style="display:flex;align-items:center;gap:11px;margin-bottom:8px">'
            '<span class="dc-eyebrow">RUN IT YOURSELF</span>'
            '<span class="dc-h2">Push your own reviews through the pipeline</span></div>'
            f'<div class="dc-lede" style="margin-bottom:18px">Paste up to {MAX_ROWS} reviews — one per line, '
            'or as CSV / JSON. They run through the same guardrails as the real corpus — '
            'dedup, the heuristic filter, then the Two-Step Gate — and every row that gets dropped comes back '
            'labelled with the guardrail that dropped it.</div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, elem_classes="dc-card"):
                gr.HTML('<div class="dc-label">REVIEWS — ONE PER LINE, OR PASTE CSV / JSON</div>')
                bulk_inp = gr.Textbox(
                    elem_id="bulk", show_label=False, lines=12, container=False,
                    placeholder=BULK_PLACEHOLDER)
                with gr.Row():
                    bulk_btn = gr.Button("Run pipeline →", elem_id="gobulk", variant="primary")
                    sample_btn = gr.Button("Load sample", elem_id="sample", size="sm")
                gr.HTML(
                    '<div style="font-size:11.5px;color:#6f6f6f;line-height:1.55;margin-top:18px">'
                    '<b style="color:#141414">Accepted shapes.</b> Plain reviews one per line; or CSV with a '
                    '<code>content</code> header (also <code>review</code> / <code>text</code>); or a JSON '
                    'list. Optional <code>rating</code>, <code>source</code>, <code>author</code> columns — '
                    'without <code>rating</code> the 5-star drop rule cannot run.<br><br>'
                    f'<b style="color:#141414">Why the {MAX_ROWS}-row cap.</b> This Space and the MVP share one '
                    'free-tier Groq key; an uncapped run could exhaust it and take both demos offline.</div>')
            with gr.Column(scale=1):
                bulk_out = gr.HTML(BULK_EMPTY)

    # ---- panel 3: results explorer ----
    with gr.Column(elem_classes="dc-body", visible=False) as panel_res:
        gr.HTML(results_html())

    gr.HTML(FOOTER)

    # ---- wiring ----
    btn.click(run_extract, inputs=inp, outputs=out)
    inp.submit(run_extract, inputs=inp, outputs=out)
    for b, text in zip(ex_btns, EXAMPLES):
        b.click(lambda t=text: t, outputs=inp).then(run_extract, inputs=inp, outputs=out)

    bulk_btn.click(run_bulk, inputs=bulk_inp, outputs=bulk_out)
    sample_btn.click(lambda: SAMPLE_BULK, outputs=bulk_inp)

    def _show(which):
        panels = [gr.update(visible=which == k) for k in ("ex", "bulk", "res")]
        tabs = [gr.update(variant="primary" if which == k else "secondary")
                for k in ("ex", "bulk", "res")]
        return panels + tabs

    _tabs_out = [panel_ex, panel_bulk, panel_res, t_ex, t_bulk, t_res]
    t_ex.click(lambda: _show("ex"), outputs=_tabs_out)
    t_bulk.click(lambda: _show("bulk"), outputs=_tabs_out)
    t_res.click(lambda: _show("res"), outputs=_tabs_out)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
