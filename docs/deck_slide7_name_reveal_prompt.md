# Design Labs prompt — keep the agent unnamed on slides 1 & 7, reveal on slide 8

Decision: the agent's name (**BlinkIQ**) should first appear on **slide 8**, not before.
Slides 1 and 7 should refer to it only generically as "the Category Nudge Agent" so the
name lands as a reveal, not a repeat.

## What to change
- **Slide 1** (title slide), intro paragraph: currently names BlinkIQ inline — revert to
  the generic label only.
- **Slide 7** ("Chosen solution" panel): currently reads "BlinkIQ — the Category Nudge
  Agent" as the panel headline — revert to plain "The Category Nudge Agent," no name.
- **Slide 8**: unchanged — this is where BlinkIQ is introduced for the first time (both
  the section headline and the eyebrow reference it).

## What NOT to touch
- Slide 8's existing BlinkIQ references stay exactly as they are — that's the reveal.
- No other copy, layout, or data on slides 1 or 7 changes — this is a name removal only.

---

## Prompt to paste into Design Labs

```
Two changes, both removing the agent's name "BlinkIQ" from slides where it appears
before its intended reveal on slide 8:

1. Slide 1 (title slide), intro paragraph: it currently reads "...a deployed AI-native
   MVP — BlinkIQ, the Category Nudge Agent." Remove "BlinkIQ" and the comma that follows
   it, so it reads "...a deployed AI-native MVP — the Category Nudge Agent." Keep the
   bold styling on "the Category Nudge Agent" exactly as it was on "BlinkIQ."

2. Slide 7, "Chosen solution" panel headline: it currently reads "BlinkIQ — the Category
   Nudge Agent" (BlinkIQ large/bold, "— the Category Nudge Agent" smaller/muted on the
   same line). Remove "BlinkIQ —" entirely so the headline is just "The Category Nudge
   Agent" at the panel's large bold treatment (previously used for "BlinkIQ").

Do not change slide 8 — it already introduces BlinkIQ and should stay as is. Do not
change any other copy, layout, or data on slides 1 or 7.
```

## Separate, not part of this pass
Two other slide 7 issues were flagged earlier and are still open, tracked separately:
- The speaker notes field contains a leftover unexecuted edit instruction ("Change the
  header for this slide. also remove the Ranked survey drivers part from the bottom
  half.") that should be cleaned out of the notes text.
- There's empty space at the bottom of slide 7 from content that was previously removed;
  options for filling it (a real customer quote, a citation strip, a runner-up note) were
  proposed but not yet chosen.
