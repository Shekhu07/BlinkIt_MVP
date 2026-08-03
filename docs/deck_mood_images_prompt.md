# Design Labs prompt: mood imagery for the deck

5 AI-illustration mood images were added to `deck/design/img/` to give the deck
an illustrative style shift on 5 of its 10 slides. Placement plan and risks
were worked out via brainstorming before drafting this prompt; images are
used as-is (no re-generation to match brand), and Design Labs is expected to
frame them like the deck's existing screenshots (1px #E7E8E2 border, 14px
radius, shadow) rather than let them go full-bleed or reskin the palette.

Filename → image:
- `img/5l5k5qipEBWBOlqwbi2Gt.png` — "From Reviews to Insights" funnel infographic
- `img/ImJ8MvyrLf8DFIGo7wDNS.png` — man reading reviews on phone, kitchen
- `img/K3IxluDXz3Vxs_eAll-Sb.png` — "Shop with Confidence" refund/quality shield
- `img/MSP32PKwJEu1inRgjgB06.png` — family unpacking groceries
- `img/qpOds-FcDInIdeVSfjxA7.jpg` — woman holding phone with Blinkit app (fake/garbled UI text on screen — known risk, accepted)

## Prompt to paste into Design Labs

```
Add illustrative mood imagery to 5 of the 10 slides in
`deck/design/Blinkit Category Nudge Case Study.dc.html`. These are stock-style
AI illustrations (not screenshots, not brand-accurate UI) — use them as
supporting visual accents, not as literal product captures.

Read `deck/design/CLAUDE.md` first and do not violate any hard rule in it:
exactly 10 slides, min 19px rendered type everywhere, no layout may overflow
(verify with the scrollHeight/scrollWidth sweep script in that file after
every change), and preserve the existing screenshot framing convention
(1px #E7E8E2 border, 14px border-radius, box-shadow 0 8px 24px rgba(0,0,0,.10),
object-fit:cover, no browser chrome/device mockups, no recoloring).

Place each image as a small-to-medium framed thumbnail INSIDE the slide's
existing grid/card structure — do not add new columns or rows, do not shrink
type below 19px, and do not remove any required content (segment/root
cause/workarounds/value framing on slide 6 must all survive). If a slide has
no room without cutting something, trim only the least-load-bearing line and
say what you cut.

Placements (images already live in deck/design/img/):

1. Slide 1 ("Title", data-screen-label="01") — img/qpOds-FcDInIdeVSfjxA7.jpg
   (woman holding phone with Blinkit app). Tuck it into the existing
   2-column stat-card row (currently `grid-template-columns:1.02fr 0.98fr`)
   as a small third element or corner inset inside one of the two existing
   cards — do not restructure the whole grid. Crop or size it so no on-screen
   app text is legible past thumbnail size — the fake UI text on that phone
   screen is not real Blinkit copy.

2. Slide 2 ("Why it matters", data-screen-label="02") — img/ImJ8MvyrLf8DFIGo7wDNS.png
   (man reading reviews on phone, kitchen). Place inside or beside the "This
   is a trust problem, not an awareness problem" white card as a small framed
   thumbnail, illustrating a customer weighing reviews before buying.

3. Slide 4 ("Review findings", data-screen-label="04") — img/5l5k5qipEBWBOlqwbi2Gt.png
   (the "From Reviews to Insights" funnel infographic). Place as a small
   accent thumbnail next to insight card #2 ("The steep funnel is the gate
   working, not data loss") — this card already states the 15,820 → 4,740 →
   1,094 numbers in text, so the image should reinforce it, not duplicate
   slide 3's own funnel hero band. Keep it small enough that it reads as a
   supporting visual, not a second data source.

4. Slide 6 ("Problem framing", data-screen-label="06") — img/MSP32PKwJEu1inRgjgB06.png
   (family unpacking groceries). Place as a small framed thumbnail supporting
   the user-value framing element, without displacing any of the five
   required framing elements (segment, root cause, workarounds, user value,
   business value, scope limit).

5. Slide 7 ("Why trust, not discount", data-screen-label="07") —
   img/K3IxluDXz3Vxs_eAll-Sb.png ("Shop with Confidence" refund/quality
   shield). Place inside or beside the dark "Chosen solution" panel (right
   column) as a small framed thumbnail — this slide has the least spare
   room, so keep the image small and do not let the panel's text wrap or
   get cut.

After placing all 5, re-run the deck's own overflow-check script from
CLAUDE.md across all 10 sections and confirm: exactly one expected overflow
entry (`02 Why it matters +27`, the existing font-descender artifact), all
10 sections still measure 1920x1080, and no rendered text computes below
19px. Report any slide that fails this before calling the work done.
```

## Open risk to check after Design Labs runs

The slide 1 image (`qpOds-FcDInIdeVSfjxA7.jpg`) has legible garbled fake UI
text on its phone screen. User explicitly chose to accept this risk rather
than crop/drop the image. Verify after rendering that Design Labs kept it
small/cropped enough that the fake text isn't a distraction.
