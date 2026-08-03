# Design Labs prompt — Slide 8 header rewrite

Target file: `deck/design/Blinkit Category Nudge Case Study.dc.html`
Target element: the `<h2>` on **slide 8** (`data-screen-label="08"`, `data-label="The MVP, running"`), currently:

> "Blink & Try It runs today: a shopper-facing nudge, its reasoning, and the push queue behind it"

---

## Prompt to paste into Design Labs

```
Rewrite ONLY the h2 headline on slide 8 ("The MVP, running") of the Blinkit Category Nudge
Case Study deck. Do not touch any other element on this slide or any other slide — same
position, same font (Plus Jakarta Sans 800), same size (48px), same max-width (1150px),
same line-height/letter-spacing.

Context this headline sits above: a live product teardown — a phone screenshot of the
shopper-facing nudge, the agent's reasoning panel, and the push-notification queue. The
agent is already named "Blink & Try It" earlier in the deck (slide 7), so this headline
is the first full introduction of it in action, not the first mention of the name.

Write 4 alternative headlines that:
- Open with punch, not a label — assertion-style, the way every other slide title in this
  deck reads (e.g. slide 2's "Blinkit's most loyal users almost never widen the basket").
- Still functionally describe what's on screen: a real, running nudge + why the agent
  chose it + the queue that sends it — evaluators should know what they're about to look
  at within one read.
- Are catchy without becoming a slogan — no exclamation marks, no invented stats or
  results (the deck rule: nothing beyond the sourced N=31 survey data and Blinkit's
  published Q1 FY27 metrics), no claims of performance or uplift since none were measured.
- Stay under ~95 characters so they don't wrap past 2 lines at 48px in a 1150px column.
- Keep "Blink & Try It" as the agent's name, verbatim — do not rename or restyle it.

Output the 4 options as plain text, ranked by your top pick, with a one-line rationale
each. Do not apply any option yet — I'll pick one and ask you to place it.
```

---

## Notes for whoever runs this
- This only asks for headline copy options — apply the chosen one as a direct text swap in the `<h2>` at deck/design line ~340, nothing else on the slide changes.
- Keep the eyebrow ("Part 4 · the MVP, deployed"), the "Open the live agent →" link, and the "Data disclosure" card untouched — the prompt scopes the edit to the h2 only on purpose.
