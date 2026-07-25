# Deck Build Spec — Blinkit Category Adoption
### Paste-ready copy for a 10-slide deck + appendix workflow slide

**How to use:** each slide below gives the exact **title** (a key message), the **body copy**
(final wording — paste as-is), **data callouts**, a **layout suggestion**, and **speaker notes**.
Build in your tool of choice; apply the compliance checklist at the end.

**Live links (embed as text + QR where noted):**
- Discovery workflow: `https://huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine`
- MVP (Category Nudge Agent): `https://huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent`

**Global visual system (keep consistent across all slides):**
- Colorblind-safe palette: ink `#1A1A1A`, slate `#4A5568`, one accent `#2B6CB0` (blue), a
  warning/attention `#B7791F` (amber). Avoid red/green as the only distinguisher.
- One sans-serif family. Title ≥ body ≥ minimum for the tool (see checklist). Generous whitespace.
- Footer on every slide: the traceability breadcrumb (e.g. `Part 1 → 2 → 3 → 4` with the current
  step emphasised). No fellow name anywhere.

---

## Slide 1 — Title
**Title:** Why do Blinkit's most loyal users never widen their basket?
**Subtitle:** Turning a growth goal into evidence: discover → validate → define → build.
**Body:** (none — keep it clean)
**Data callouts:** small footer strip showing the four stages as one arrow:
`Discovery engine → User research → Problem definition → Live AI MVP`
**Layout:** big title, subtitle beneath, the 4-stage arrow across the lower third.
**Speaker notes:** The Growth Team wants more monthly active customers buying from at least one
*new* category. Instead of guessing why they don't, I built a pipeline that finds the reason in
real user data and ends in a working product. No name on the deck per submission rules.

## Slide 2 — The goal & the approach
**Title:** A growth metric, answered with evidence — not assumptions.
**Body:**
- **The goal:** increase the % of monthly active customers who buy from ≥1 new category each month.
- **The method — four parts, each built on the last:**
  1. AI discovery engine mines real reviews for the true barrier.
  2. User research tests that barrier with real people.
  3. A problem statement names the segment + root cause.
  4. A live AI MVP directly attacks that root cause.
**Data callouts:** none; this is the map.
**Layout:** goal as a banner up top; the 4 numbered steps as a horizontal flow.
**Speaker notes:** The key idea — nothing here is built in isolation. Each part consumes the
previous part's output. This is the thread to follow for the rest of the deck.

## Slide 3 — Part 1: the discovery engine & its headline finding
**Title:** An AI engine read 15,820 reviews and found one dominant barrier: broken trust in product quality.
**Body:**
- Pipeline funnel: **15,820 raw reviews → 4,740 filtered → 1,094 gate-passing extractions.**
- A **Two-Step Gated Schema** first asks "is this about trying/avoiding a category at all?" —
  then extracts. It rejects generic refund/delivery/pricing noise.
- **Top theme: "Poor Quality & Unreliable Products" — 770 of 1,094 (≈70%).** Next themes: 10%, 7%.
**Data callouts:** big **70%** stat; the funnel as 3 shrinking blocks.
**Embed:** discovery workflow link + QR ("Test the extractor yourself").
**Layout:** funnel left, headline stat + theme name right, link/QR bottom-right.
**Speaker notes:** The gate is the core design decision — an earlier open-ended version just
surfaced generic complaints. Evaluators can paste any review into the live link and watch the
gate run.

## Slide 4 — Part 1: is the finding trustworthy?
**Title:** The finding holds up — validated by an LLM judge and aligned with Eternal's own growth narrative.
**Body:**
- **LLM-judge validation:** 16 / 20 confirmed, 4 unclear, 0 contradicted (held-out, theme-relevant sample).
- **Company corroboration:** Eternal's Q4 FY26 earnings call names **non-grocery assortment
  expansion** as a core growth dependency — the same widening this project is trying to unlock.
- **Honest gap:** the call does *not* directly discuss product-quality or refund friction. Say so;
  it's a real limit of the corroboration, not something to paper over.
**Data callouts:** `16/20 confirmed · 0 contradicted`.
**Layout:** two evidence cards side by side (AI validation | company commentary).
**Speaker notes:** This shows the theme isn't just one model's opinion — an independent judge
confirms it, and the company's own stated growth path depends on the behaviour we're trying to move.

> **Decision (2026-07-24): the "1.8% of NOV" inventory-loss figure is OMITTED from the deck.**
> It came from a hand-transcribed Q1FY27 shareholders'-letter excerpt with no source document in
> the repo; `analyze_concalls.py` was never re-run with it, so `company_disclosures` and
> `results.json` contain only the three Q4FY26 excerpts. The quote above is the corroboration
> that is actually reproducible from this repo and visible in the live discovery app.

## Slide 5 — Part 2: user research CONFIRMS *and* CHALLENGES the AI *(mandatory)*
**Title:** 25 real users: the quality fear is real — but it's only half the story.
**Body:**
- **Confirmed:** quality incidents spread beyond the affected category —
  *"I only order the essential items now if anything urgent."*
- **Challenged:**
  - One user **churned to a competitor (Zepto)** rather than just avoiding a category.
  - **6 of 13** incident-havers changed **nothing** — a full refund often neutralizes the fear.
  - **6 of 14** "stuck" users had **no bad incident at all** — low intent, not distrust.
**Data callouts:** a 2-column CONFIRMED / CHALLENGED split.
**Layout:** left column green-free "confirmed" (use blue accent), right column amber "challenged".
**Speaker notes:** This is the required confirm-and-contradict slide. Being honest here is the
point — it directly shapes the scope of the MVP two slides later.

## Slide 6 — Part 3: the problem statement
**Title:** Loyal, high-frequency buyers default to what's proven safe — because one bad experience removes the benefit of the doubt.
**Body:**
- **Segment:** repeat buyers who stick to the same categories — **56% of respondents**; heavy,
  daily/near-daily, mainstream across city tiers.
- **Root cause:** an unresolved quality failure generalizes into category avoidance — for the
  **~50%** of the segment that is trust-driven (not the low-intent half).
- **Today's workarounds:** retreat to "essentials only"; or switch platforms.
**Data callouts:** `56% stuck` · `~50% trust-driven`.
**Layout:** segment / root cause / workarounds as three stacked bands.
**Speaker notes:** Note the honesty built into the root cause — we scope to the trust-driven half
rather than claiming quality explains everyone.

## Slide 7 — Part 3: why solving it matters (user + business)
**Title:** Users already told us the fix — and it aligns with Blinkit's own P&L.
**Body:**
- **What users said would change their behavior (survey Q15, top two):**
  a "no-questions-asked" refund/return guarantee **(11/25)**, and a visible quality/freshness
  signal **(9/25)**.
- **Business fit:** Eternal's own Q4 FY26 call ties future growth to **non-grocery assortment
  expansion** — which only pays off if users actually try those categories. Removing the trust
  barrier is upstream of that growth path.
**Data callouts:** `11/25` and `9/25` as ranked bars.
**Layout:** user-value bars left; business-case note right.
**Speaker notes:** The fix isn't invented — users ranked it themselves, and it happens to point
the same direction as a real company cost line. That's the double justification.

## Slide 8 — Part 4: the MVP (Category Nudge Agent)
**Title:** An AI agent that earns the first try — leading with a guarantee, not a generic "try something new."
**Body:**
- Matches a user's behavior to the friction theme, then generates a **per-user, reasoned nudge**
  that leads with the **refund guarantee + quality/freshness signal** (the two ranked drivers).
- **AI-native:** the reasoning is generated per user and theme — not a fixed template.
- **Honest scope:** targets the trust-driven ~50%; the low-intent half needs a different lever.
**Data callouts:** one real screenshot of a generated nudge from the live app.
**Embed:** MVP link + QR ("Try the live agent").
**Layout:** left = how it works (3 steps); right = live nudge screenshot + link/QR.
**Speaker notes:** Walk one example: a user with a past dairy issue → agent suggests a new
category led by the guarantee. It's live — evaluators can generate their own.

## Slide 9 — The thread, and the honesty
**Title:** One line runs through all four parts — and we're clear about what it doesn't solve.
**Body:**
- **The thread:** Theme (770 / 70%) → confirmed *and* challenged by 25 users → problem
  (trust-driven category avoidance) → nudge (guarantee-led, per-user).
- **The boundary:** this moves the trust-driven half. The low-intent half needs a different play
  (e.g. relevance-led discovery — a documented next step).
**Data callouts:** the thread as a single 4-node chain across the slide.
**Layout:** horizontal chain graphic; honesty note beneath.
**Speaker notes:** This is the "product thinking" slide — one traceable line, plus an explicit
statement of the limits. Evaluators reward the honesty.

## Slide 10 — Impact & what's live
**Title:** A testable engine and a live agent — the whole thread is reachable, not just described.
**Body:**
- **Live now:** the discovery workflow (test the extraction) and the Category Nudge Agent
  (generate a nudge) — both public.
- **The metric it moves:** new-category trial rate in the nudged cohort — measurable as an A/B lift.
- **Next steps:** checkout cart-filler micro-trial for low-intent users (the segment this MVP doesn't target); pre-acceptance-inspection nudge; churn-save agent; move beyond synthetic data.
**Data callouts:** both links as prominent buttons + QRs.
**Layout:** two link cards up top; metric + next-steps beneath.
**Speaker notes:** Close on reachability — two working links, a clear metric, and honest next
steps. Leave the links on screen.

---

## Appendix (embedded, not counted in the 10) — Part 1 Workflow 1-slider
**Title:** How the discovery engine works, end to end.
**Body / diagram (left → right):**
`Ingest (Play Store · Google Maps · App Store · MouthShut · ConsumerComplaints)`
`→ TF-IDF prefilter → Two-Step Gated LLM extraction (Groq) → deterministic theme clustering`
`→ LLM-judge validation → earnings-call corroboration`
**Callout:** evidence counts are **DB-backed row counts, never LLM-estimated.**
**Layout:** single horizontal pipeline diagram, six labelled stages.
**Speaker notes:** This is the required standalone workflow explainer; keep it as the slide right
after slide 10, clearly labelled "Appendix / Workflow" so the main deck is a clean 10.

---

## Formatting-compliance checklist (verify before export)
- [ ] **≤10 slides** in the main narrative (title = slide 1). Workflow = labelled appendix.
- [ ] **No fellow name** anywhere — slides, footer, file metadata, notes.
- [ ] **Minimum font size** for your tool: **14** (Google Slides / PPT) · **26** (Figma @1920×1080)
      · **22** (Canva @1920×1080). Check the smallest text (footers, callouts, captions).
- [ ] **Colorblind-safe palette**; never use red-vs-green as the only signal. Text readable on any
      background used.
- [ ] **Both links public + working**, and clickable in the exported PDF.
- [ ] **File < 40 MB**; compress the nudge screenshot if needed.
- [ ] **File name** in the "NL Blinkit…" convention (e.g. `NL_Blinkit_CategoryAdoption.pdf`).
- [ ] Export to **PDF**; re-open and click both links to confirm they resolve.
