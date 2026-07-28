# Design Labs working prompt — editing the deck in place

Paste the fenced block below at the **start of any Design Labs session** where you intend to
change `Blinkit Category Nudge Case Study.dc.html`, then add your actual request underneath it.

It exists because the deck is graded against rules that are invisible from the canvas — a 612px
height budget on slide 10, a 19px type floor, and an invent-nothing rule that three previous
imports broke. Without the preamble, a reasonable-looking edit can silently fail one of them.

**Durable alternative:** most of this also belongs in the project's own `CLAUDE.md`, which Design
Labs reads automatically every session. That file is currently correct on the survey figures but
is missing the slide-10 budget and still tells you to verify with a check that does not catch
clipping (see §"Verification" below). Ask me to sync it and you can skip pasting this each time.

---

```
Before changing anything in "Blinkit Category Nudge Case Study.dc.html", load these constraints.
They are graded, and several are invisible from the canvas.

## Invent nothing
Every number, quote, theme name and label must already exist in the deck or in what I give you in
this message. Do NOT introduce conversion rates, A/B results, uplifts, p-values, live-usage
funnels, per-user confidence scores, real Blinkit pricing, or Eternal's "1.8% of NOV"
inventory-loss figure. If a panel seems to need a number I have not supplied, write the
qualitative claim instead or label it "proposed — not yet measured". Three earlier imports of this
deck shipped invented figures that had to be stripped by hand; this is the highest-risk failure.

## Hard output rules
- EXACTLY 10 slides. Title counts as one. No appendix slide. Never add or remove a section.
- The fellow's name appears nowhere in visible text. Slide 1's two cards stay label-only
  hyperlinks ("Open the live extractor →" / "Open the live agent →") with the URL only in href.
  Never render a raw URL as visible text. Slide 3 says the workflow is linked from the title slide.
- Minimum type 19px (14pt equivalent) on anything rendered — including chips, captions, table
  cells and footnotes. Decorative single-character glyphs count.
- Colour-blind safe: green #146634 / amber #7A6100 must always be paired with a word or glyph,
  never carrying meaning alone.
- Assertion-style slide titles (a full sentence stating the finding), with a small letterspaced
  uppercase eyebrow above each.
- Discovery-engine screenshots are cropped to remove the Hugging Face account pill. Keep them
  cropped; never swap in an uncropped capture.

## Visual system (do not drift)
Yellow #F8CD1B accent, ink #16130A, page #F4F5F3 (flat on every slide — the only gradient in the
deck is the soft yellow radial glow top-right of slide 1). White cards, 1px #E7E8E2, 20px radius.
Plus Jakarta Sans 400/600/800. Brand green #318616 for graphics only, never small text. Tinted
cards: confirmed/value #EDF5E9 + 1px #CFE3C6; chosen/highlight #FFF9DF + 1px #F8CD1B; neutral
white; limit/caution dark #16130A.

## Slide 10 has a hard height budget — read before touching it
Its two-column grid gets EXACTLY 612px and is the tightest thing in the deck. Adding anything
there costs real content elsewhere. Measured attempts:

  baseline                                              627px  (+15, was clipping)
  + one new line in each column                         723px  (+111)
  + a 5th guardrail as its own item, 2-col              723px  (+111)
  + a 5th guardrail, guardrails grid changed to 3-col   739px  (+127)  <- worse, narrower = more wrap
  + 5th guardrail with tighter ladder padding           699px  (+87)
  merged into the nudge-fatigue cell + ladder padding
  reduced 14px -> 10px  (CURRENT, shipped)              612px  (0)

The deck currently sits at exactly 612 with zero slack. Any addition to slide 10 must be paid for
by removing something. Do not add to it without telling me what you removed.

## Verification — the obvious check does NOT work
`section.scrollHeight` stays 1920x1080 even while an inner grid overflows and visibly clips
content behind the band below it. That is how a broken slide 10 passed review once already.

After ANY edit, run and report this:

  [...document.querySelectorAll('section[data-label] *')]
    .filter(e => e.scrollHeight - e.clientHeight > 20 && e.clientHeight > 0)
    .map(e => e.closest('section').getAttribute('data-screen-label')
              + ' +' + (e.scrollHeight - e.clientHeight))

Expected result: exactly one entry, "02 Why it matters +27". That is a pre-existing font-descender
artefact on the 58% numeral, not clipping. ANY other entry means you broke a slide — fix it before
telling me you are done.

Also confirm, every time:
- all 10 sections measure exactly 1920x1080
- no rendered text computes below 19px (ignore <style> and <script> nodes, which report 16px)
- no occurrence of "Abhishek" outside an href attribute
- no stale N=25 figures: 56%, 14 of 25, 13 of 25, 11/25, 9/25, 5/25, 6 of 13, 6 of 14, 8 of 14
```

---

## Current verified state — do not re-litigate these

As of the last sync, the deck passes every check above. Settled decisions:

| | |
|---|---|
| Survey figures | N=31, frozen 2026-07-28. 58% stuck (18/31) · 15/31 had a bad order · 7/7/1 behaviour split · 8 of 18 stuck with no incident · Q14 mean 3.0 (11 agree / 11 disagree / 9 neutral) |
| Q15 drivers | refund 13 · quality 10 · **inspect 7** · reviews 5 · offers 5 · nothing 4 · agent 3 · packaging 1 (write-in). Inspect is the **third** driver; item reviews are **fourth** — never label reviews as third |
| Slide 10 guardrails | five, including the order-frequency counter-metric merged into the nudge-fatigue cell |
| Category breadth | deliberately **not** on slide 10 — no room. It lives in `script.md` §5.1 as spoken material |
| Eternal corroboration | Q4 FY26 quotes only. The Q1 FY27 "1.8% of NOV" figure is hand-transcribed with no source doc in the repo and stays off the deck |

## Things this prompt cannot fix

The fellow's name still sits inside slide 1's two `href` values and in the `data-props` block, so
it surfaces in a PDF link annotation and on hover. No deck edit removes that — it needs the two
Hugging Face Spaces moved to an organization account, which requires HF Pro.
