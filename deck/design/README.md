# Local copy of the Design Labs deck

Imported 2026-07-28 from the Claude Design project **"Blinkit presentation template"**
(`37db5789-c8b0-4ce1-9173-7f42675f92fb`) via the design MCP.

Main file: `Blinkit Category Nudge Case Study.dc.html` — 10 slides, 1920×1080, deck-stage runtime.

## `CLAUDE.md` here is a mirror — sync it by hand

`deck/design/CLAUDE.md` is the design project's instruction file. It serves two purposes: it
scopes the deck's rules for local work in this directory, and it is the paste source for the
Design Labs copy.

**It cannot be pushed over the MCP.** `write_files` rejects `CLAUDE.md` and `.claude/` as reserved
paths regardless of the finalized plan, because they carry instructions to the design agent — an
agent is not allowed to rewrite the instructions another agent reads. After editing this file,
open the project in Design Labs, open its `CLAUDE.md`, and paste the contents over. Everything
else in this directory syncs normally via `write_files`.

Drift here is silent and costly: the Design Labs copy is what constrains every future edit made in
the canvas, so if it lags, the agent will happily reintroduce a fixed defect.

## Run it locally

```bash
cd deck/design && python3 -m http.server 8770
# open http://localhost:8770/Blinkit%20Category%20Nudge%20Case%20Study.dc.html
```
It must be served over HTTP — the page fetches `support.js` / `deck-stage.js` / `image-slot.js`
relatively, so opening the file over `file://` will not boot the runtime.

## Verified after import (headless Chromium)

- 10 `<section>`s, each measuring **exactly 1920×1080** (the project's hard rule).
- No sub-19px (14pt) type anywhere.
- No fellow name and no raw URL in visible text — the two title-slide cards are label-only
  hyperlinks ("Open the live extractor →" / "Open the live agent →") whose `href`s carry the
  Hugging Face URLs. **Residual nit unchanged:** the name still lives inside the `href` and in
  the `data-props` block, so it is visible in a PDF link annotation / on hover. Only an HF
  organization transfer removes that.
- No stale N=25 figures; no forbidden figures (no "1.8% of NOV", no A/B results, no uplifts).
  The one "confidence score" hit is the negation "never a per-user confidence score" — intended.

## Three changes made after import (all pushed back to Design Labs)

1. Slide 2's `data-speaker-notes` still said **56%** (the N=25 figure) while the slide itself
   said 58%. Corrected to 58%.
2. Four glyph chips (`!`, `%`, `✓`) were set at **17px** ≈ 12.75pt, under the deck's own 19px /
   14pt floor. Raised to 19px; the chips are 34–40px so there is no layout impact.

3. Slide 10 gained the missing **order-frequency counter-metric**. It guards the failure mode that
   matters most for a push nudge into a habitual weekly reorder flow: the nudge degrades the core
   behaviour you already had. Folded into the existing nudge-fatigue cell rather than added as a
   fifth guardrail, because slide 10 had no vertical headroom (see below).

All three are pushed to the Design Labs project; local and remote match.

## Slide 10's height budget — read this before editing it

The two-column grid on slide 10 gets **exactly 612px** and is the tightest thing in the deck.
Measured intrinsic heights at import: col0 625px, col1 623px — i.e. it was already ~15px over and
clipping slightly. Anything added there costs real content elsewhere. Measured options:

| Attempt | Height needed | vs 612 budget |
|---|---|---|
| baseline at import | 627 | +15 (pre-existing clip) |
| category breadth + order frequency, as new lines | 723 | +111 |
| order frequency as a 5th guardrail, 2-col | 723 | +111 |
| order frequency as a 5th guardrail, 3-col grid | 739 | +127 |
| 5th guardrail + tighter ladder padding | 699 | +87 |
| **merged into nudge-fatigue cell + ladder padding 14->10px** | **612** | **0** |

The shipped version is the last row: it fits exactly and removes the pre-existing 15px clip.
`section.scrollHeight` stays 1920x1080 even when the grid overflows, so **that check alone is not
sufficient** — verify with a per-container `scrollHeight - clientHeight` sweep instead.

**Still not on slide 10:** category breadth per user per month, the companion to the primary
metric that catches the hollow win (adoption rises, breadth flat). There is no room for it; it
lives in `script.md` Section 5.1 as spoken material.

## Images — one is missing

`img/` holds 7 of the 8 required assets:

| Asset | Source |
|---|---|
| `mvp-02-phone-nudge.png`, `mvp-03-reasoning-ranked.png`, `mvp-04-out-of-scope.png`, `mvp-07-lockscreen.png` | copied from `deck/screenshots/` (identical files) |
| `disc-01-extractor-pass-crop.png`, `disc-02-extractor-reject-crop.png`, `disc-04-results-explorer-crop.png` | **regenerated locally** — see below |
| `blinkit-logo.png` | **regenerated locally** from the official press kit — see below |

### Why the three `disc-*-crop` files were regenerated
The MCP's `get_file` caps responses at 256 KiB and returned all three **truncated** (no IEND
chunk, ~197 KB of a larger file), so the originals could not be transferred intact. They were
instead regenerated from the uncropped captures in `deck/screenshots/` by removing the top
125px, which is the floating Hugging Face account pill that carries the fellow's name —
verified visually after cropping. Framing differs slightly from the Design Labs crops, but the
slots use `object-fit:cover; object-position:top`, so the rendered result is equivalent.

**Do not substitute the uncropped `deck/screenshots/disc-*.png` files** — they show
`Abhishek292000 / blinkit-discovery-engine` along the top edge.

### The logo
`img/blinkit-logo.png` (683x192 RGBA) was regenerated from the official Blinkit press kit
(`~/Downloads/press-kit_0.png`, the same source the Design Labs project cropped its copy from).
It could not be transferred over the MCP: files under the 256 KiB cap arrive inline in model
context rather than on disk, so writing it out would mean hand-transcribing ~14 KB of base64.

The extraction is an alpha un-matte, not a chroma key. The press kit is flat ink on flat yellow,
so for each pixel `C = a*F + (1-a)*B` with `B` = #F8CB46 sampled from the background and `F` the
nearer of the two ink colours (#1F1F1F / #318616); alpha solves directly as the projection of
`C-B` onto `F-B`. That keeps anti-aliased letter edges clean with no yellow fringe — verified by
compositing over the page (#F4F5F3), white and the dark panel (#16130A).

Two traps if this ever needs redoing: the press kit is mode `P` with transparency and has
**transparent rounded corners**, which will swallow the bounding box unless you mask on
`alpha > 250` first; and the bbox must be taken from confident ink (`alpha > 0.35`), not from
`alpha > 0`, or background noise widens it to the full frame.

Output is padded to the 683x192 aspect the deck's `width:212px` (slide 1) and `width:104px`
(slides 2-10) rules were built against, so no layout shifts.
