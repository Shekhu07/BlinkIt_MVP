# Design Labs prompt — slide 9: header, eyebrow, and runtime-flow copy sync

Target slide: **slide 9**, "Deterministic logic decides what to nudge..." (Architecture
and Limits). These changes have already been applied to the coded `.dc.html` file — this
prompt is for applying the same edits manually in Design Labs, plus two open items that
need your judgment before anything is changed there.

## Required changes (already decided)
1. **Header**: replace the current headline with **"Rules decide; the model only speaks."**
2. **Eyebrow**: drop the "Part 4 ·" prefix — it should read just **"ARCHITECTURE AND LIMITS"**
   (uppercase, same letterspacing/weight/colour as now).
3. **Runtime flow copy sync**: the three middle steps should read:
   - "Matches each user to their real friction pattern — no AI guessing"
   - "Ranks nearby categories with simple math, not a black box"
   - "Writes the actual message, live, per user"
   (These already match what's shown in this Design Labs render — this item is only
   relevant if you're re-syncing from the older coded copy; skip if your Design Labs
   version already has this wording.)

## Open items — needs your decision first, not yet in scope for this prompt
- **Icon vs. text-label chips on the runtime-flow steps.** The coded file uses text
  badges ("Rule-based" / "LLM"); this Design Labs render uses small icons instead. Pick
  one treatment as the source of truth before this gets touched again — tell me which,
  and I'll draft that as its own follow-up prompt.
- **Possible caption clipping**: the "Amber banner..." caption at the bottom-left of the
  screenshot panel looked like it might be running under the floating "9/10 · Reset"
  toolbar. Confirm in Present mode whether the full sentence renders cleanly before
  treating this as resolved.

---

## Prompt to paste into Design Labs

```
On slide 9 ("Deterministic logic decides what to nudge..."), make these changes:

1. Replace the h2 headline with: "Rules decide; the model only speaks." Keep the exact
   same font (Plus Jakarta Sans, 800 weight, 50px), max-width, and position — text swap
   only.

2. In the eyebrow line (currently "PART 4 · ARCHITECTURE AND LIMITS", small caps, gold
   colour, next to the Blinkit logo), remove "PART 4 ·" so it reads just "ARCHITECTURE
   AND LIMITS". Keep the same letterspacing, weight, size, and colour.

3. Confirm the "Runtime flow" panel's three middle steps read exactly:
   - "Matches each user to their real friction pattern — no AI guessing"
   - "Ranks nearby categories with simple math, not a black box"
   - "Writes the actual message, live, per user"
   If they already say this, no change needed here.

Do not change anything else on this slide — the "Why this nudge" screenshot panel, the
"Two integrity rules" box, the "Where it breaks" list, and any other slide stay as they
are. Do not touch the icon/text-chip styling on the runtime-flow steps — that's a
separate decision not yet made.
```
