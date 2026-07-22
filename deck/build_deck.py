"""Generate NL_Blinkit_CategoryAdoption.pptx from docs/deck_spec.md.

A starter deck to IMPORT into Google Slides (File -> Import slides). Carries the final
copy, speaker notes, a colorblind-safe palette, and >=14pt fonts (Google Slides minimum).
Polish visuals, add the live nudge screenshot + QR codes in Slides after import.

Run:  ./venv/bin/python deck/build_deck.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt

# ---- palette (colorblind-safe) ----
INK = RGBColor(0x1A, 0x1A, 0x1A)
SLATE = RGBColor(0x4A, 0x55, 0x68)
ACCENT = RGBColor(0x2B, 0x6C, 0xB0)   # blue
AMBER = RGBColor(0xB7, 0x79, 0x1F)    # attention
LIGHT = RGBColor(0xF2, 0xF4, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Arial"  # safe, maps cleanly into Google Slides
MIN = 14        # never go below this

# Masked short links (TinyURL) so no fellow name appears in the deck. They redirect to the
# real HF Spaces (huggingface.co/spaces/Abhishek292000/...), which HF gates from renaming
# without Pro — see docs/deck_spec.md compliance note.
DISCOVERY_URL = "https://tinyurl.com/2xz4eeaf"  # -> blinkit-discovery-engine
MVP_URL = "https://tinyurl.com/2bbqo8vs"        # -> blinkit-category-nudge-agent

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

SW, SH = prs.slide_width, prs.slide_height


def slide():
    return prs.slides.add_slide(BLANK)


def box(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    return tb, tf


def style(run, size, color=INK, bold=False, italic=False):
    run.font.size = Pt(size)
    run.font.name = FONT
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic


def band(s, x, y, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def title(s, text, color=INK):
    _, tf = box(s, 0.7, 0.5, 11.9, 1.6)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text
    style(r, 28, color, bold=True)


def bullets(s, items, x=0.7, y=2.3, w=11.9, h=4.2, size=18):
    _, tf = box(s, x, y, w, h)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(8)
        lvl = it.get("lvl", 0)
        p.level = lvl
        for seg in it["segs"]:
            r = p.add_run(); r.text = seg["t"]
            style(r, it.get("size", size), seg.get("c", INK),
                  bold=seg.get("b", False), italic=seg.get("i", False))
        if lvl == 0:
            # bullet dash prefix via leading text kept simple
            pass


def footer(s, current):
    parts = ["Part 1", "Part 2", "Part 3", "Part 4"]
    _, tf = box(s, 0.7, 7.0, 11.9, 0.4)
    p = tf.paragraphs[0]
    for i, pt in enumerate(parts):
        r = p.add_run(); r.text = pt
        style(r, 14, ACCENT if pt == current else SLATE, bold=(pt == current))
        if i < len(parts) - 1:
            sep = p.add_run(); sep.text = "  →  "
            style(sep, 14, SLATE)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def stat(s, x, y, value, label, color=ACCENT):
    _, tf = box(s, x, y, 3.4, 1.6)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = value
    style(r, 48, color, bold=True)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = label
    style(r2, 14, SLATE)


# ================= SLIDE 1 — Title =================
s = slide()
band(s, 0, 0, 13.333, 7.5, WHITE)
_, tf = box(s, 0.9, 2.3, 11.5, 2.2)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Why do Blinkit's most loyal users never widen their basket?"
style(r, 40, INK, bold=True)
_, tf2 = box(s, 0.9, 4.5, 11.5, 1.0)
p2 = tf2.paragraphs[0]
r2 = p2.add_run(); r2.text = "Turning a growth goal into evidence: discover → validate → define → build."
style(r2, 20, SLATE)
_, tf3 = box(s, 0.9, 6.4, 11.5, 0.6)
p3 = tf3.paragraphs[0]
r3 = p3.add_run(); r3.text = "Discovery engine  →  User research  →  Problem definition  →  Live AI MVP"
style(r3, 16, ACCENT, bold=True)
notes(s, "The Growth Team wants more monthly active customers buying from at least one NEW "
         "category. Instead of guessing why they don't, I built a pipeline that finds the reason "
         "in real user data and ends in a working product. No name on the deck per submission rules.")

# ================= SLIDE 2 — Goal & approach =================
s = slide()
title(s, "A growth metric, answered with evidence — not assumptions.")
band(s, 0.7, 2.1, 11.9, 0.9, LIGHT)
_, tf = box(s, 0.9, 2.25, 11.5, 0.7, anchor=MSO_ANCHOR.MIDDLE)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "The goal: increase the % of monthly active customers who buy from ≥1 new category each month."
style(r, 18, INK, bold=True)
bullets(s, [
    {"segs": [{"t": "The method — four parts, each built on the last:", "b": True}], "size": 18},
    {"segs": [{"t": "1.  AI discovery engine mines real reviews for the true barrier."}], "size": 18, "lvl": 1},
    {"segs": [{"t": "2.  User research tests that barrier with real people."}], "size": 18, "lvl": 1},
    {"segs": [{"t": "3.  A problem statement names the segment + root cause."}], "size": 18, "lvl": 1},
    {"segs": [{"t": "4.  A live AI MVP directly attacks that root cause."}], "size": 18, "lvl": 1},
    {"segs": [{"t": "Nothing is built in isolation — each part consumes the previous part's output.",
               "i": True, "c": SLATE}], "size": 16},
], y=3.3, h=3.3)
notes(s, "The key idea: nothing here is built in isolation. Each part consumes the previous part's "
         "output. This is the thread to follow for the rest of the deck.")

# ================= SLIDE 3 — Part 1 finding =================
s = slide()
title(s, "An AI engine read 15,820 reviews and found one dominant barrier: broken trust in product quality.")
bullets(s, [
    {"segs": [{"t": "Funnel: ", "b": True}, {"t": "15,820 raw → 4,740 filtered → 1,094 gate-passing extractions."}], "size": 18},
    {"segs": [{"t": "A ", "c": INK}, {"t": "Two-Step Gated Schema", "b": True},
              {"t": " first asks “is this about trying/avoiding a category at all?”, then extracts — rejecting generic refund/delivery/pricing noise."}], "size": 18},
    {"segs": [{"t": "Top theme: ", "b": True}, {"t": "“Poor Quality & Unreliable Products” — 770 of 1,094 (≈70%).", "b": True, "c": ACCENT},
              {"t": "  Next themes: 10%, 7%."}], "size": 18},
], y=2.2, h=2.8)
stat(s, 9.3, 4.9, "70%", "of category-avoidance\nevidence = one theme")
_, tf = box(s, 0.7, 5.4, 8.2, 1.2)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "▶ Test the extractor live:  "
style(r, 15, INK, bold=True)
r2 = p.add_run(); r2.text = DISCOVERY_URL
style(r2, 15, ACCENT)
p.runs[-1].hyperlink.address = DISCOVERY_URL
footer(s, "Part 1")
notes(s, "The gate is the core design decision — an earlier open-ended version just surfaced "
         "generic complaints. Evaluators can paste any review into the live link and watch the gate run.")

# ================= SLIDE 4 — Part 1 validation =================
s = slide()
title(s, "The finding holds up — validated by an LLM judge and echoed in Blinkit's own numbers.")
band(s, 0.7, 2.4, 5.7, 3.6, LIGHT)
band(s, 6.9, 2.4, 5.7, 3.6, LIGHT)
_, tf = box(s, 1.0, 2.7, 5.1, 3.0)
p = tf.paragraphs[0]; r = p.add_run(); r.text = "LLM-judge validation"; style(r, 20, ACCENT, bold=True)
p2 = tf.add_paragraph(); p2.space_before = Pt(6)
r2 = p2.add_run(); r2.text = "16 / 20 confirmed · 0 contradicted"; style(r2, 22, INK, bold=True)
p3 = tf.add_paragraph(); r3 = p3.add_run()
r3.text = "Against a held-out, theme-relevant sample — not random reviews."; style(r3, 16, SLATE)
_, tf2 = box(s, 7.2, 2.7, 5.1, 3.0)
q = tf2.paragraphs[0]; rq = q.add_run(); rq.text = "Company corroboration"; style(rq, 20, AMBER, bold=True)
q2 = tf2.add_paragraph(); q2.space_before = Pt(6)
rq2 = q2.add_run(); rq2.text = "Inventory losses ≈ 1.8% of NOV"; style(rq2, 22, INK, bold=True)
q3 = tf2.add_paragraph(); rq3 = q3.add_run()
rq3.text = "Eternal Q1FY27 letter — concentrated in perishables (expiry/damage), the same categories the reviews flagged."
style(rq3, 16, SLATE)
footer(s, "Part 1")
notes(s, "This matters because it shows the theme isn't just one model's opinion — an independent "
         "judge and the company's own P&L point the same way.")

# ================= SLIDE 5 — Part 2 confirm & challenge =================
s = slide()
title(s, "25 real users: the quality fear is real — but it's only half the story.")
band(s, 0.7, 2.3, 5.7, 4.0, LIGHT)
band(s, 6.9, 2.3, 5.7, 4.0, RGBColor(0xFB, 0xF2, 0xE1))
_, tf = box(s, 1.0, 2.5, 5.1, 3.6)
p = tf.paragraphs[0]; r = p.add_run(); r.text = "CONFIRMED"; style(r, 18, ACCENT, bold=True)
p2 = tf.add_paragraph(); p2.space_before = Pt(6)
r2 = p2.add_run(); r2.text = "Quality incidents spread beyond the affected category:"; style(r2, 16, INK)
p3 = tf.add_paragraph(); p3.space_before = Pt(6)
r3 = p3.add_run(); r3.text = "“I only order the essential items now if anything urgent.”"
style(r3, 17, INK, italic=True)
_, tf2 = box(s, 7.2, 2.5, 5.1, 3.6)
q = tf2.paragraphs[0]; rq = q.add_run(); rq.text = "CHALLENGED"; style(rq, 18, AMBER, bold=True)
for t in ["One user churned to a competitor (Zepto) rather than just avoiding a category.",
          "6 of 13 incident-havers changed nothing — a full refund often neutralizes the fear.",
          "6 of 14 “stuck” users had no bad incident at all — low intent, not distrust."]:
    pp = tf2.add_paragraph(); pp.space_before = Pt(6)
    rr = pp.add_run(); rr.text = "• " + t; style(rr, 16, INK)
footer(s, "Part 2")
notes(s, "This is the required confirm-and-contradict slide. Being honest here is the point — it "
         "directly shapes the scope of the MVP two slides later.")

# ================= SLIDE 6 — Part 3 problem =================
s = slide()
title(s, "Loyal, high-frequency buyers default to what's proven safe — because one bad experience removes the benefit of the doubt.")
bullets(s, [
    {"segs": [{"t": "Segment:  ", "b": True}, {"t": "repeat buyers who stick to the same categories — "},
              {"t": "56% of respondents", "b": True, "c": ACCENT}, {"t": "; heavy, daily/near-daily, mainstream across city tiers."}], "size": 18},
    {"segs": [{"t": "Root cause:  ", "b": True}, {"t": "an unresolved quality failure generalizes into category avoidance — for the "},
              {"t": "~50% of the segment that is trust-driven", "b": True, "c": AMBER}, {"t": " (not the low-intent half)."}], "size": 18},
    {"segs": [{"t": "Today's workarounds:  ", "b": True}, {"t": "retreat to “essentials only”; or switch platforms."}], "size": 18},
], y=2.6, h=3.4)
footer(s, "Part 3")
notes(s, "Note the honesty built into the root cause — we scope to the trust-driven half rather "
         "than claiming quality explains everyone.")

# ================= SLIDE 7 — Part 3 why it matters =================
s = slide()
title(s, "Users already told us the fix — and it aligns with Blinkit's own P&L.")
bullets(s, [
    {"segs": [{"t": "What users said would change their behavior (survey Q15, top two):", "b": True}], "size": 18},
    {"segs": [{"t": "A “no-questions-asked” refund/return guarantee — "}, {"t": "11 / 25", "b": True, "c": ACCENT}], "size": 18, "lvl": 1},
    {"segs": [{"t": "A visible quality/freshness signal — "}, {"t": "9 / 25", "b": True, "c": ACCENT}], "size": 18, "lvl": 1},
    {"segs": [{"t": "Business fit:  ", "b": True}, {"t": "assortment expansion is a stated Blinkit growth pillar (CEO, Q1FY27); cutting damage-driven distrust also supports the company's own 1.8%-of-NOV inventory-loss line."}], "size": 18},
], y=2.4, h=3.6)
footer(s, "Part 3")
notes(s, "The fix isn't invented — users ranked it themselves, and it happens to point the same "
         "direction as a real company cost line. That's the double justification.")

# ================= SLIDE 8 — Part 4 MVP =================
s = slide()
title(s, "An AI agent that earns the first try — leading with a guarantee, not a generic “try something new.”")
bullets(s, [
    {"segs": [{"t": "Matches a user's behavior to the friction theme, then generates a "},
              {"t": "per-user, reasoned nudge", "b": True}, {"t": " that leads with the "},
              {"t": "refund guarantee + quality/freshness signal", "b": True, "c": ACCENT}, {"t": " (the two ranked drivers)."}], "size": 18},
    {"segs": [{"t": "AI-native:  ", "b": True}, {"t": "the reasoning is generated per user and theme — not a fixed template."}], "size": 18},
    {"segs": [{"t": "Honest scope:  ", "b": True, "c": AMBER}, {"t": "targets the trust-driven ~50%; the low-intent half needs a different lever."}], "size": 18},
    {"segs": [{"t": "[ Add a screenshot of a live generated nudge here ]", "i": True, "c": SLATE}], "size": 15},
], y=2.3, h=3.2)
_, tf = box(s, 0.7, 5.7, 11.9, 0.8)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "▶ Try the live agent:  "; style(r, 15, INK, bold=True)
r2 = p.add_run(); r2.text = MVP_URL; style(r2, 15, ACCENT)
p.runs[-1].hyperlink.address = MVP_URL
footer(s, "Part 4")
notes(s, "Walk one example: a user with a past dairy issue → agent suggests a new category led by "
         "the guarantee. It's live — evaluators can generate their own.")

# ================= SLIDE 9 — Thread & honesty =================
s = slide()
title(s, "One line runs through all four parts — and we're clear about what it doesn't solve.")
band(s, 0.7, 2.6, 11.9, 1.5, LIGHT)
_, tf = box(s, 0.9, 2.8, 11.5, 1.1, anchor=MSO_ANCHOR.MIDDLE)
p = tf.paragraphs[0]
segs = [("Theme (770 / 70%)", ACCENT), ("  →  ", SLATE),
        ("confirmed & challenged by 25 users", INK), ("  →  ", SLATE),
        ("problem: trust-driven avoidance", INK), ("  →  ", SLATE),
        ("nudge: guarantee-led, per-user", ACCENT)]
for t, c in segs:
    r = p.add_run(); r.text = t; style(r, 17, c, bold=(c == ACCENT))
bullets(s, [
    {"segs": [{"t": "The boundary:  ", "b": True, "c": AMBER}, {"t": "this moves the trust-driven half. The low-intent half needs a different play (e.g. relevance-led discovery — a documented next step)."}], "size": 18},
], y=4.5, h=1.6)
footer(s, "Part 4")
notes(s, "This is the “product thinking” slide — one traceable line, plus an explicit statement "
         "of the limits. Evaluators reward the honesty.")

# ================= SLIDE 10 — Impact & links =================
s = slide()
title(s, "A testable engine and a live agent — the whole thread is reachable, not just described.")
band(s, 0.7, 2.3, 5.7, 1.7, LIGHT)
band(s, 6.9, 2.3, 5.7, 1.7, LIGHT)
_, tf = box(s, 1.0, 2.5, 5.1, 1.3, anchor=MSO_ANCHOR.MIDDLE)
p = tf.paragraphs[0]; r = p.add_run(); r.text = "Discovery workflow (test the extraction)"; style(r, 16, INK, bold=True)
p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = DISCOVERY_URL; style(r2, 14, ACCENT)
p2.runs[-1].hyperlink.address = DISCOVERY_URL
_, tf2 = box(s, 7.2, 2.5, 5.1, 1.3, anchor=MSO_ANCHOR.MIDDLE)
q = tf2.paragraphs[0]; rq = q.add_run(); rq.text = "Category Nudge Agent (generate a nudge)"; style(rq, 16, INK, bold=True)
q2 = tf2.add_paragraph(); rq2 = q2.add_run(); rq2.text = MVP_URL; style(rq2, 14, ACCENT)
q2.runs[-1].hyperlink.address = MVP_URL
bullets(s, [
    {"segs": [{"t": "The metric it moves:  ", "b": True}, {"t": "new-category trial rate in the nudged cohort — measurable as an A/B lift."}], "size": 18},
    {"segs": [{"t": "Next steps:  ", "b": True}, {"t": "pre-acceptance-inspection nudge; churn-save agent; move beyond synthetic data."}], "size": 18},
], y=4.4, h=1.8)
footer(s, "Part 4")
notes(s, "Close on reachability — two working links, a clear metric, and honest next steps. Leave the links on screen.")

# ================= APPENDIX — Workflow 1-slider =================
s = slide()
title(s, "Appendix · How the discovery engine works, end to end.", color=SLATE)
band(s, 0.7, 2.6, 11.9, 1.8, LIGHT)
_, tf = box(s, 0.9, 2.8, 11.5, 1.4, anchor=MSO_ANCHOR.MIDDLE)
p = tf.paragraphs[0]
r = p.add_run()
r.text = ("Ingest (Play Store · Google Maps · App Store · MouthShut · ConsumerComplaints)  →  "
          "TF-IDF prefilter  →  Two-Step Gated LLM extraction (Groq)  →  deterministic theme "
          "clustering  →  LLM-judge validation  →  earnings-call corroboration")
style(r, 17, INK, bold=True)
_, tf2 = box(s, 0.9, 4.8, 11.5, 0.8)
p2 = tf2.paragraphs[0]
r2 = p2.add_run(); r2.text = "Evidence counts are DB-backed row counts — never LLM-estimated."
style(r2, 16, AMBER, bold=True)
notes(s, "Required standalone workflow explainer; kept as the slide right after slide 10, clearly "
         "labelled Appendix so the main deck is a clean 10.")

out = Path(__file__).parent / "NL_Blinkit_CategoryAdoption.pptx"
prs.save(out)
print(f"Saved {out}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
