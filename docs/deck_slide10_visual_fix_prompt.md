# Design Labs prompt — slide 10: remove leftover text, make it visual not just informational

Target slide: **slide 10** (last slide), "Adoption is the metric; the guardrails are the veto."

The header swap and the dry-run wording fix from the previous pass both landed correctly.
Two things remain: a leftover text bug from the header swap, and the slide still reading
as pure information with no visual variety — the icon suggestion from last time was
skipped, and that's the main reason it still looks unfinished.

## Bug — required
There's a stray orphaned line reading **"trust guardrails"** in small, unstyled text
directly under the new headline. It's a leftover fragment of the old headline ("...with
trust guardrails") that didn't get removed when the header text was swapped. Delete it —
nothing should replace it; the eyebrow and headline are sufficient on their own.

## Make icons required, not optional, this time
Last prompt listed icons as optional and none were added. This is the single biggest
reason the slide reads as walls of text: every card is differentiated only by black-vs-
white background, nothing is actually visual. Add icons, consistent with the Stitch icon
set already used elsewhere in this deck:
- Primary Metric card → target/bullseye icon, sized prominently (this is the headline
  metric — it should have the most visual weight of anything on the slide)
- Guardrails card → shield/barrier icon
- "What we'd build next" section → roadmap/forward-arrow icon
- Small flask/test-tube badge next to "SYNTHETIC DRY-RUN"

## New — give the Measurement Ladder an actual visual form
It's called a "ladder" but is currently a plain 3-row data table — the most literal,
lowest-effort way to add real visual interest here is to make it look like what it's
named. Render the three tiers (Outcome / Mechanism / Durability) as an ascending
3-step staircase or ladder graphic running down the left edge of that box, with the
existing text content sitting beside each step instead of in table rows. Same content,
same three tiers, no new claims — just a visual form that matches its own name instead
of a spreadsheet-style table.

## What NOT to touch
- Don't change any number, statistic, or wording beyond removing the leftover text.
- Don't touch the header, eyebrow, or the already-fixed dry-run line.
- Don't add "category breadth per user per month" — still deliberately out of scope here.
- Icons should clarify, not decorate — no icon that doesn't correspond to an actual
  section already on the slide.

---

## Prompt to paste into Design Labs

```
On the final slide ("Adoption is the metric; the guardrails are the veto."), three fixes:

1. BUG: remove the stray leftover line reading "trust guardrails" that currently sits in
   small unstyled text directly under the headline. It's a leftover fragment from the old
   headline and nothing should replace it.

2. REQUIRED (previously optional, now required — it was skipped last time and this is
   why the slide still reads as pure text): add icons consistent with this deck's
   existing Stitch icon set:
   - Primary Metric card → a target/bullseye icon, given the most visual prominence on
     the slide since this is the headline metric
   - Guardrails card → a shield/barrier icon
   - "What we'd build next" section header → a roadmap/forward-arrow icon
   - A small flask/test-tube badge next to "SYNTHETIC DRY-RUN"

3. Convert the Measurement Ladder from a plain 3-row table into an actual ascending
   3-step staircase/ladder graphic running down the left edge of that card, with the
   existing Tier/What-we'd-watch/Reads-as content placed beside each step instead of in
   table rows. Keep the exact same three tiers and text content — this is a visual-form
   change only, matching the box's own name ("ladder") instead of looking like a
   spreadsheet.

Do not change any number, statistic, header, eyebrow, or the already-corrected
"SYNTHETIC DRY-RUN" wording. Do not add "category breadth per user per month." Icons must
correspond to sections already on the slide — no purely decorative additions.
```
