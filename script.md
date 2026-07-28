# Presentation Script & Evaluator Q&A Prep

### Blinkit — Cross-Category Adoption | NextLeap PM Fellowship Graduation Project

**Last updated:** 2026-07-28 · figures current at survey freeze N=31 and Part 1 export.

**How to use this:** §1–§3 are what you say. §4 is the number sheet to memorise. §5 is the
question bank, ordered roughly by how likely each is. §6 is the list of things that are
genuinely weak — read it twice, because a rehearsed honest answer beats an improvised
defensive one, and every weakness below is one an experienced evaluator will find.

---

## 1. The 60-second version

> Blinkit's growth team wants more monthly active customers buying from at least one new
> category each month. The obvious assumption is that this is a discovery problem — people
> don't know the other categories exist. I tested that assumption instead of accepting it.
>
> I built an AI engine over 15,820 public reviews that hard-gates on category-adoption
> relevance before it extracts anything. It found that the dominant barrier isn't awareness,
> it's trust: 70% of the category-behaviour signal is people who had a quality failure —
> damaged, expired, or fake — and responded by narrowing what they'd risk buying.
>
> I then ran a 31-person survey to test that. It confirmed the mechanism and challenged its
> reach: quality failures do generalise into whole-category avoidance, but only for about
> half the stuck segment. The other half simply don't want those categories.
>
> So the problem I scoped is deliberately narrower than the goal: for high-frequency buyers
> whose trust was broken, one bad order removes the benefit of the doubt they'd otherwise
> extend to an unfamiliar category. The MVP — the Category Nudge Agent, deployed and live —
> attacks exactly that, leading with the two things users themselves ranked highest: a
> no-questions-asked refund guarantee and a visible quality signal. And when the user isn't
> trust-blocked, the product says so on screen rather than pretending the fix applies.

**The one line to land:** _"The insight is that this is a trust problem wearing a discovery
problem's clothes — and I can show you the evidence for both halves of that sentence."_

---

## 2. The three-minute walkthrough (slide-by-slide spine)

Follow the traceability thread. At every slide you should be able to answer _"which part does
this come from, and what did the previous part tell us that led here?"_

| Slide | The beat                | The one sentence                                                                                                  |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1     | Title + two live links  | "Both the workflow and the MVP are live — you can test them while I talk."                                        |
| 2     | The goal, framed        | "58% of the people I surveyed say they stick to the same categories. They already see the other ones every week." |
| 3     | How the engine works    | "Five stages, and the third one is the whole design decision — it gates on relevance before it extracts."         |
| 4     | What the reviews said   | "One theme carries the segment: poor quality and unreliable products, 770 of 1,094."                              |
| 5     | What the survey said    | "It confirmed the mechanism and challenged how far it reaches — and I kept the challenge on the slide."           |
| 6     | The problem statement   | "Segment, root cause, workarounds, user value, business value — plus what this explicitly doesn't solve."         |
| 7     | Why this solution       | "Four options considered; the trust-led nudge wins because it answers the blocker users actually named."          |
| 8     | The MVP, running        | "Live Groq call per user. No invented numbers anywhere in the copy — that's enforced in the prompt."              |
| 9     | Architecture and limits | "Deterministic logic decides _what_ to nudge; the LLM only writes the words. Here's where it breaks."             |
| 10    | Measurement             | "Proposed, not measured — no experiment has been run, so there are no result numbers on this slide."              |

**Where to spend your time if you're cut short:** slides 3, 5 and 9. Slide 3 is the strongest
technical differentiator, slide 5 is the mandated confirm-and-challenge deliverable, and slide
9 is where you demonstrate the judgement to separate deterministic logic from generation.

---

## 3. The four parts, in the depth you'd need if asked to go deeper

### Part 1 — the discovery engine

**Corpus.** 15,820 deduplicated public reviews (SHA-256 dedup) in Postgres. Sources: Play
Store 8,058 · Google Maps 4,098 · **source not recorded 2,532** · App Store 530 · MouthShut
520 · ConsumerComplaints.in 76 · reddit 6 (mock/placeholder, labelled).

**Pipeline.** Ingest → heuristic prefilter (rule-based, no LLM; drops empty text, reviews under
five words, and 5-star reviews) → **Two-Step Gated extraction** (Groq `llama-3.1-8b-instant`) →
deterministic clustering → LLM-judge validation → earnings-call corroboration.

**The core design decision — the gate.** An earlier open-ended version of the extraction prompt
surfaced four macro-themes that were all general service complaints: broken refunds, quality
control, inflated pricing, delivery misconduct. None of them connected to category adoption.
The root cause was that the LLM was doing open-ended theme generation, so it clustered on
whatever was most _prevalent_ in the text — and service complaints dominate review corpora by
volume — rather than on what was _relevant to the question_.

So extraction was rewritten into two steps. Step 1 asks only: is this text about why someone
keeps buying the same category, why they haven't tried an unfamiliar one, how they discover
things, a specific moment of trying or rejecting a category, or trust about trying something
unfamiliar? Text primarily about refunds, support, delivery timing, pricing or app bugs —
**with no explicit tie to category trial or avoidance** — is rejected as
`mentions_category_behavior: false`. Only if it passes does Step 2 extract structured fields:
`behavior_type`, `category_mentioned`, `underlying_reason`, `sentiment`, `confidence`.

The prompt carries few-shot examples that distinguish real category signal from complaints that
merely _mention_ a category — a wrong-item refund complaint that happens to name "baby wipes"
is correctly rejected, because it says nothing about why the user chose or avoided that category.

**Funnel.** 15,820 → 4,740 after prefilter → **1,094 gate-passing extractions**. That is a steep
drop and it is the intended outcome, not data loss. It is also itself a finding: category-behaviour
signal is genuinely scarce in review data and mostly implicit, which says something about how
invisible this problem is to the users experiencing it.

**Result.** Top theme **"Poor Quality and Unreliable Products" — 770 of 1,094 (70%)**, stable
across repeated independent clustering runs. Next themes: Convenience and Price Sensitivity 114
(10%), Discovery Friction and Limited Options 78 (7%). Behaviour split: category_avoidance 77%,
repeat_purchase 11%, discovery_friction 9%, new_category_trial 2%, unknown 1%.

**Evidence counts are database row counts, never LLM estimates.** This is worth saying out loud —
it's the difference between a measured result and a model's impression of one.

**Validation.** An LLM judge re-checked a held-out, theme-relevant sample: 16/20 confirmed, 4
unclear, 0 contradicted.

### Part 2 — primary research

A Google Form questionnaire, **N=31, frozen 2026-07-28**. **No live interviews were conducted** —
see §6.1, this is the project's biggest deviation and you must lead with it rather than let it
be discovered.

**Confirmed** — quality failures generalise past the category they happened in:

- _"I have stopped exploring new categories on Blinkit. I only order the essential items now if
  anything urgent."_ (puja items arrived rotten/wrong-sized; complaint never resolved)
- _"yes I am skeptical of buying electronic products from Blinkit and other similar applications"_
- _"I avoid buying any fresh products dairy or perishables items from quick commerce apps."_
  (expired dairy — note this generalised to the _whole industry_, not just Blinkit)

**Challenged** — four ways, and all four stay in the deck:

1. The behaviour change is an even split, not a rule: of 15 with a bad order, 7 changed, 7 didn't,
   1 ambiguous. Resolution usually neutralises it — 11 of 15 got a full refund.
2. One respondent churned to a competitor entirely (_"I have started using Zepto more"_) rather
   than narrowing categories — a different and arguably worse failure than the one I'm solving.
3. 8 of the 18 "stuck" respondents had **no incident at all**. Their stagnation is low intent:
   _"Nothing in particular — I just don't need those categories."_
4. Asked the thesis directly (Q14: _"a bad experience in one category makes me more hesitant to
   try other categories"_), the rated answer is **mean 3.0 — 11 agree, 11 disagree, 9 neutral**.
   The polarisation is real and I show it.

**New sub-cause.** Packaging/fulfilment, distinct from product-source quality: fragile stationery
crushed because it was packed under heavier groceries. That respondent also _wrote in_ the fix
unprompted — "better and safer packaging guarantees for fragile items" — rather than picking any
offered option.

**What users said would unlock trial (Q15, pick up to 2, N=31):** refund guarantee 13 · visible
quality/freshness guarantee 10 · inspect before accepting delivery 7 · item reviews 5 · intro
offers 5 · nothing in particular 4 · human agent 3 · safer packaging 1 (write-in).

### Part 3 — the problem statement

All five required elements, on one slide:

- **Segment:** heavy, habitual repeat buyers with narrow baskets — 18/31 (58%), daily or near-daily,
  spanning Tier 1/2/3, students through professionals. Mainstream, not niche, which matters for
  opportunity size.
- **Root cause:** an unresolved or generically-handled quality failure removes the benefit of the
  doubt a user would otherwise extend to an unfamiliar category. Not laziness, not unawareness.
- **Workarounds:** retreat to essentials-only, or switch platforms. The first suppresses the metric
  silently; the second is active share loss.
- **User value:** they already want to consolidate into one app and can't risk it. 27 of 31 named a
  concrete change that would help.
- **Business value:** basket width is the growth lever Eternal itself has named. Restoring trust
  re-opens non-grocery categories among customers who already order frequently — no new acquisition.

**Corroboration.** Eternal Q4 FY26 earnings call (28 Apr 2026): an analyst frames growth as
depending on "growing the non-grocery assortment and going outside of the metro cities," and the
CFO describes growth as "a function of assortment expansion, geographical expansion as well as
more demand densification." **Honest caveat, stated on the slide:** the call does not discuss
product-quality or refund friction. The link to my cause is mine, not the company's.

**Scope limit, stated up front:** this addresses the trust-driven share of stagnation only —
roughly half. The low-intent half needs a different instrument and I don't claim otherwise.

### Part 4 — the Category Nudge Agent (live)

**Flow.** Synthetic user profile → **rule-based** friction match to a Part 1 theme (no LLM) →
**rule-based** adjacency ranker producing a candidate category list with integer weights (not model
confidence) → **LLM** generates the nudge copy and reasoning (Groq `llama-3.3-70b-versatile`,
JSON mode) → rendered nudge leading with the refund guarantee, then the quality/freshness signal.

**The architectural point:** deterministic logic decides _what_ to nudge; the LLM only writes the
words. That's what keeps it auditable — the same profile always matches the same theme and gets the
same candidate ranking, and the only variable part is the prose.

**Two integrity rules enforced in the system prompt:**

1. Never invent statistics — no ratings, buyer counts, percentages or success rates may appear in
   nudge copy. Verified live across all 8 profiles: zero digits in any social-proof line.
2. Never overclaim to low-intent users — with no incident on file, the agent leads with relevance
   instead of a guarantee, and the UI shows an amber "out of primary scope" banner saying the trust
   fix does not apply to this user.

**Where it breaks** (on the slide, deliberately): profiles are synthetic; a refund promise is only
credible if operations honour it, so the nudge inherits fulfilment risk it can't control; packaging
failures need a fulfilment change, not a message; and a customer who has already switched platforms
may never see the nudge.

**Deployment reality worth knowing if asked:** both apps are Gradio on HuggingFace free tier. The
Docker SDK was paywalled on this account and CPU-basic wasn't selectable, so both run on ZeroGPU —
which refuses to boot without a `@spaces.GPU` function. Each app registers a no-op warmup purely to
pass that check. Neither uses a GPU; all LLM work is remote on Groq.

---

## 4. Number sheet — memorise these

|                                       |                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------- |
| Raw reviews                           | **15,820** (deduped, SHA-256)                                                   |
| After prefilter                       | **4,740**                                                                       |
| Gate-passing extractions              | **1,094**                                                                       |
| Top theme                             | **"Poor Quality and Unreliable Products" — 770 / 1,094 = 70%**                  |
| Themes 2 and 3                        | Convenience & Price Sensitivity 114 (10%) · Discovery Friction 78 (7%)          |
| Behaviour split                       | avoidance 77% · repeat 11% · discovery friction 9% · new trial 2% · unknown 1%  |
| Top-theme categories (top five named) | groceries 431 · electronics 96 · snacks 79 · household 39 · personal care 27    |
| LLM-judge validation                  | **16/20 confirmed · 4 unclear · 0 contradicted**                                |
| Survey                                | **N=31**, frozen 2026-07-28                                                     |
| Stuck segment                         | **18/31 = 58%**                                                                 |
| Had an incident                       | **15/31 = 48%** (11 damaged · 2 expired · 1 fake · 1 other)                     |
| Resolution                            | 11 full refunds · 3 replacements · 1 unresolved                                 |
| Behaviour-change split                | **7 changed · 7 unchanged · 1 ambiguous**                                       |
| Stuck with no incident                | **8 of 18**                                                                     |
| Q14 (thesis, rated 1–5)               | **mean 3.0 — 11 agree · 11 disagree · 9 neutral**                               |
| Q13 (trust in resolution)             | mean 3.5                                                                        |
| Q15 top drivers                       | refund **13** · quality/freshness **10** · inspect **7** · reviews 5 · offers 5 |
| MVP                                   | 8 synthetic profiles · Groq `llama-3.3-70b-versatile`                           |
| Extraction model                      | Groq `llama-3.1-8b-instant`                                                     |

**If you forget a number, say so.** "I don't have that one in my head, it's in the export" is a
fine answer. Inventing a number in a project whose entire thesis is _don't invent numbers_ is the
single worst thing you could do in the room.

---

## 5. Question bank

### 5.1 The ones you will almost certainly get

**Q: Why Blinkit and not Zepto or Instamart?**
Largest public data footprint of the three, which matters when the whole of Part 1 depends on
scrapeable volume. Broadest category range, so the cross-category question is actually
interesting. And a listed parent (Eternal) with public earnings calls, which gave me a source of
company-stated strategy to corroborate against rather than only user complaints.

**Q: Walk me through how the discovery engine works.**
Use the five stages, then spend your time on the gate. The story of the failed ungated run is more
persuasive than the architecture diagram — it shows you validated your own tool before trusting it.

**Q: Why is your funnel so steep? You threw away 93% of the data.**
Two separate filters. The prefilter drops empty text, reviews under five words and 5-star reviews —
that's noise reduction. The gate then removes everything not tied to trying or avoiding a category,
which is most of a review corpus, because people write reviews about delivery and refunds. What
survives is deliberately small. The alternative is what I had first: 15,000 reviews clustered into
four generic complaint themes that told me nothing about category adoption. I'd rather have 1,094
relevant rows than 15,820 irrelevant ones. And the scarcity is itself informative — this problem is
largely invisible in the channels where users volunteer feedback.

**Q: Isn't "poor product quality" just a generic service complaint? How is that a category-adoption insight?**
This is the sharpest question in the set and it's the one the gate exists to answer. A generic
quality complaint _is_ rejected — a wrong-item refund complaint naming "baby wipes" doesn't pass.
What passes is text where the quality failure is explicitly tied to trial or avoidance behaviour.
That's why 77% of what survives is classified `category_avoidance`. And the survey verbatims show
the mechanism directly: "I have stopped exploring new categories," "I am skeptical of buying
electronic products," "I avoid buying any fresh products... from quick commerce apps." Those aren't
complaints about a bad order — they're descriptions of a narrowed consideration set.

**Q: You validated an LLM's output with another LLM. Isn't that circular?**
Partly, and I'd call it a weak validation rather than a strong one. Three things reduce the
circularity: the judge sees a held-out, theme-relevant sample rather than the extraction's own
working set; the evidence counts it validates are database row counts, not model estimates, so the
quantities can't drift; and the independent check that matters more is the survey, which is a
different instrument on a different population and confirmed the same mechanism. If I had more
runway I'd add a human-labelled gold set and report precision and recall on the gate specifically —
that's the honest gap.

**Q: What did your research challenge, not just confirm?**
Have four ready — the even split, the platform-churner, the low-intent half, and the Q14 rated
polarisation. Then make the point that matters: _the challenge is what set the MVP's scope._ If the
survey had only confirmed, I'd have built something that overclaims to half the segment.

**Q: Why a nudge and not a discount, better merchandising, or reviews?**
Slide 7's table. Discounts pay a customer to repeat the experience that broke their trust — it
doesn't change the expected outcome of the order, and every rival can copy it. Merchandising solves
awareness, and these buyers already see the categories weekly. Item reviews are table stakes and
rated 4th by users. The trust-led nudge is the only option that answers the top two blockers users
named themselves, and it's per-user rather than a surface everyone sees.

**Q: What's AI-native about this? Isn't it a wrapper?**
Two things. First, Part 1 isn't a wrapper — it's a gated extraction schema that solved a real
failure mode, and its output is the reason the problem statement says what it says. Second, in the
MVP the LLM's job is narrow and deliberate: deterministic rules decide which theme matched and
which categories are eligible; the model generates the reasoning and copy per user against that
user's specific friction. If I'd let the model choose the category too, I'd have a less auditable
product and I couldn't have fixed the category-collapse bug I found. Restraint about where the model
is allowed to decide _is_ the AI product thinking.

**Q: How would you measure success?**
Primary: % of monthly active customers purchasing from at least one new category that month,
measured against the nudged segment's own prior month rather than a headline average. Then three
tiers — outcome (did behaviour change), mechanism (nudge shown → opened → browsed → added, which
tells you which step leaks), and durability (repeat purchase in the new category the following
month, which distinguishes trust restored from trust merely tested).

**Q: What are your counter-metrics?**
Return and refund rate in nudged categories — nudging someone into a genuinely bad category is a
trust loss, not a win. Complaint rate among nudged users against their own baseline. Nudge fatigue:
dismissals and opt-outs, capped per user per month. And a copy audit — sampled nudges checked for
invented statistics, where any hit is a release blocker. That last one exists because the failure
mode of an LLM writing trust copy is fabricating the proof.

### 5.2 The ones aimed at your weak points

**Q: The brief asked for 5–6 user interviews. You did none.**
Answer this directly and without flinching — see §6.1 for the full framing. Do not let it be
discovered mid-conversation.

**Q: 31 responses from your own network isn't a representative sample.**
Correct, and I don't present it as one. It's a non-probability convenience sample, so I use it for
mechanism and language, not for prevalence. That's why the headline number in the deck comes from
1,094 review extractions rather than from the survey, and why the survey's job on slide 5 is to
confirm _and challenge_ rather than to size anything. Where I do quote survey proportions — 58%
stuck, the 7/7 split — I state the denominator every time so nobody reads them as population
estimates.

**Q: Your MVP runs on synthetic users. Doesn't that make it a demo?**
It makes it a working system on synthetic inputs, which is different from a mockup. Every nudge is
a live Groq call — evaluators can generate one right now and get something that has never existed
before. What's synthetic is the order history, because I don't have Blinkit's production data, and
the file says so in its metadata and on screen. The honest limit, which is on slide 9: nothing here
is matched against real behavioural history, so the friction match is untested against reality.

**Q: You said the top theme explains 70%, but half your survey respondents didn't change behaviour. Doesn't that undermine the whole thing?**
It bounds it, and I'd rather bound it myself than have you find it. The 70% is share of
category-behaviour _signal in reviews_ — of the people who wrote about category adoption, this is
what they wrote about. The survey measures something different: whether an incident changes
behaviour in a general population, and there it's an even split, corroborated by Q14 at mean 3.0.
Both are true. That's exactly why the problem statement scopes to the trust-driven half and the
product tells low-intent users the fix isn't theirs. If I'd claimed 70% of the _segment_ was
trust-blocked, that would have been an overclaim.

**Q: Where did 2,532 of your reviews come from?**
A master JSON dump where those rows carry no `source` field at all — about 16% of the corpus is
real scraped review text whose originating platform was never recorded. They're real, not mock, so
they stay in the corpus and the funnel, and the discovery app displays them as "source not recorded"
rather than inventing a platform name. I'd rather show an honest gap than a clean-looking fiction.

**Q: I see reddit in your sources. The brief asked for Reddit discussions.**
Live Reddit scraping was dropped — bot protection, and it wasn't worth the scoping cost. The six
reddit rows in the database come from a mock ingest script and are labelled as mock; they're
statistically irrelevant and I don't cite them. It's a real gap against the brief's source list,
and the honest trade was corpus depth on the sources that worked over thin coverage everywhere.

**Q: Has any of this been tested with real users? What's the impact?**
None. No experiment has been run and the MVP has never been shipped to real users, which is why
slide 10 carries a "plan only" banner and no result numbers appear anywhere in the deck. I'd rather
present a measurement design I can defend than a lift figure I made up.

**Q: What would you do differently with more time?**
Three, in priority order. Run the six live interviews I recruited and never called — the survey's
open-ended fields are a weaker instrument for the _why_ behind the even split. Build a
human-labelled gold set to measure the gate's precision and recall instead of relying on an LLM
judge. And test the pre-acceptance-inspection mechanic — it's the third-ranked driver at 7 of 31
and the highest-ranked thing this MVP deliberately doesn't do.

### 5.3 Depth probes if they're technical

**Q: Why Groq and Llama rather than GPT-4 or Claude?**
Cost and throughput at corpus scale. I started on Gemini 1.5 Flash and abandoned it — the free tier
capped at 20 requests a day, which makes a multi-thousand-review batch run impossible, and the model
was later removed from the API entirely. Groq's free tier could run the full 4,740 extractions.
`llama-3.1-8b-instant` for extraction, because the gate is a narrow classification task and a small
fast model is appropriate for it; `llama-3.3-70b-versatile` for the agent, because generating
per-user reasoning that stays inside six hard rules needs more capability.

**Q: How do you know the theme clustering is stable?**
It's deterministic by construction. Themes are clusters of real category × behaviour_type
combinations, and `evidence_count` is computed by counting database rows — never estimated by the
model. The 770 figure reproduced across repeated independent runs. That was a deliberate rewrite:
an earlier version let the LLM report counts, which is exactly how you end up with numbers nobody
can reproduce.

**Q: What's your hallucination mitigation in the MVP?**
Layered. The model never chooses the category — a deterministic ranker hands it a candidate list.
The system prompt bans invented statistics outright and I verified zero digits appear in any
social-proof line across all 8 profiles. Output is JSON-mode against a fixed schema. And there's a
copy audit in the counter-metrics, so at production scale sampled nudges get checked and a
fabricated figure is a release blocker rather than a bug report.

**Q: Tell me about a bug you found and fixed.**
The agent collapsed to suggesting "personal care" for 7 of 8 profiles — a single safe answer
regardless of who the user was, which would have made the personalisation claim false. Fixed with a
deterministic adjacency ranker plus an explicit prompt rule that the model must choose from the
provided ranked list and justify any deviation. Now 4 distinct categories across the profiles. It's
a good example of why the deterministic layer exists: the bug was only findable _because_ the
category choice was inspectable.

### 5.4 Curveballs

**Q: If Blinkit's ops can't honour the refund guarantee, your nudge makes things worse.**
Agreed, and it's on slide 9 as a stated failure mode. The nudge inherits fulfilment risk it can't
control — that's precisely why the return and refund rate in nudged categories is a counter-metric
and not a success metric. If nudged users start returning more, the honest read is that the guarantee
wrote a cheque the operation didn't cash, and the nudge should be paused, not scaled.

**Q: Why not just fix the quality problem instead of messaging around it?**
You should do both, and the quality fix is the more valuable one — Eternal's own CFO reports
inventory losses from expiry, damage and transit concentrated in perishables. But two things:
quality improvement is a multi-quarter operations programme, and even after it lands, the customers
who were already burned don't automatically find out. Trust doesn't recover on its own timetable;
someone has to tell them, at the moment they're deciding. That's the gap the nudge fills.

**Q: How does this scale beyond the ~50% you've scoped?**
It doesn't, by design, and that's the honest answer. The low-intent half needs a different
instrument — a relevance-led rather than trust-led play, which is one of my next bets. The mistake
would have been building one mechanism and claiming it moves everyone. Any evaluation of this needs
to report the two sub-segments separately or it'll read as a failure of the wrong thing.

**Q: What surprised you?**
That resolution neutralises the damage more often than I expected — 11 of 15 incidents got a full
refund, and roughly half of those users carried on as normal. My prior was that a bad order is
sticky. It isn't, if you fix it well. What's sticky is a bad order that goes _unresolved_ — the
respondent who stopped exploring entirely was the one whose complaint was never closed. That
changed how I think about the lever: it's less about preventing every failure and more about the
recovery being visibly guaranteed before the customer takes the risk.

---

## 6. Known weaknesses — rehearse these

### 6.1 Zero live interviews (the big one)

The brief asks for 5–6 user interviews. I ran none. **Lead with it; do not let it surface as a
discovery.**

> "I should flag the clearest gap myself. The brief asks for five to six live interviews and I
> ran zero. I substituted a 31-response survey with open-ended fields, which is a deliberate
> trade of depth for breadth against the deadline — it gave me four times the sample and the
> verbatims you see on slide 5, but it cost me the follow-up question. I know exactly what I
> lost: six respondents consented to calls I never made, and the most interesting finding in
> the whole project — the even split between people who changed behaviour and people who
> didn't — is precisely the thing a live conversation would have explained. That's the first
> thing I'd do with another week."

Do **not**: call the survey equivalent to interviews, imply the open-ended fields are as good as
a conversation, or blame time without naming what was lost.

### 6.2 The rest, in one place

| Weakness                             | The honest line                                                                                                                                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Convenience sample, N=31             | Used for mechanism and language, not prevalence. Denominators stated every time.                                                                                                        |
| LLM validating an LLM                | Weak validation. The real independent check is the survey. Gold set is the fix.                                                                                                         |
| Synthetic MVP profiles               | Working system, synthetic inputs. Labelled everywhere. Friction match untested against real history.                                                                                    |
| No experiment, no results            | Stated on slide 10. A measurement design I can defend beats a lift I invented.                                                                                                          |
| 16% of corpus has no recorded source | Real text, unknown platform. Shown as "source not recorded", never as a platform.                                                                                                       |
| Reddit dropped                       | Bot protection; 6 mock rows exist, are labelled, and are never cited. A real gap against the brief.                                                                                     |
| Q1FY27 "1.8% of NOV" figure          | Hand-transcribed, not reproducible from the repo — **deliberately omitted from the deck**. If asked about inventory losses, cite the Q4 FY26 quotes, which are reproducible end to end. |
| Q4 FY26 call doesn't mention quality | Said on the slide: the link to my cause is mine, not the company's.                                                                                                                     |

### 6.3 Two hard rules for the room

1. **Never invent a number.** The project's credibility rests on real-vs-invented being
   unambiguous. "I don't have that in my head" is always the correct fallback.
2. **Never describe mock or synthetic material as real.** The synthetic profiles, the six reddit
   rows, and the illustrative product in the phone mockup are all labelled in the artefacts —
   keep them labelled in your speech too.

---

## 7. Pre-submission checklist (deadline 4 Aug 2026, 3:59:00 PM IST)

- [ ] Deck contains no name — slides, footers, **file metadata**, speaker notes. Search for
      "Abhishek" and "huggingface.co" in the exported PDF; strip PDF Author/Creator on export.
- [ ] Exactly 10 slides including the title.
- [ ] Slide 6 shows all five required elements: segment · root cause · workarounds · user value ·
      business value.
- [ ] Smallest live text ≥ 14pt (check the annotations on slides 8–9).
- [ ] Both live links open from the exported PDF and both Spaces are awake.
- [ ] File < 40 MB, named in the "NL Blinkit…" convention.
- [ ] Every linked artefact is publicly accessible — test in a logged-out browser.
