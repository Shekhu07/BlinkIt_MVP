# Part 2: Real Interview Recruitment Kit

Replaces the mocked recruitment/interview flow in `mock_interview_notes.md`. Segment confirmed 2026-07-18 from the real Two-Step Gated extraction (4,740/4,740 filtered reviews processed via Groq) + clustering run — see `part2_research_tracker.md` for the full theme ranking.

---

## 1. Screening criteria
**Real top theme: "Poor Quality and Unreliable Products"** — 770 of 1,094 gate-passing extractions (70%), spanning groceries, electronics, snacks/beverages, household essentials, and personal care roughly proportional to category volume. NOT limited to high-value purchases.

- Has purchased from Blinkit at least 3 times in the last month (repeat user).
- Has received a damaged, expired, wrong, fake/duplicate, or used-instead-of-new item on Blinkit — in ANY category, not just electronics or expensive items — OR had a refund/support request that went unresolved or poorly handled.
- Bonus (not required): has since avoided re-buying that category, or hesitated to try a new category because of the experience — this is the specific link to category-adoption behavior the research is trying to confirm or challenge.

## 2. Recruitment channels & outreach templates

### Personal network / WhatsApp / alumni groups
> Hey! I'm doing a research project on quick-commerce shopping habits (Blinkit/Zepto/Instamart). Looking for 15–20 min for a quick chat about how you shop for groceries vs. other stuff on these apps — no pitch, no survey link, just a conversation. Would you be up for a quick call this week? Happy to work around your schedule.

### Reddit / online communities (r/delhi, r/bangalore, r/IndianStreetBets-adjacent shopping threads, etc.)
> Hi all — doing independent research (not affiliated with any quick-commerce company) on how people decide what to buy vs. not buy on apps like Blinkit/Zepto/Instamart. Looking to chat with 4–5 people for ~15 min about your shopping habits — happy to do it over a call or even async over DM if that's easier. Not selling anything, just trying to understand real usage patterns for a project. DM if interested!

### Screening message (once someone responds)
> Thanks for reaching out! Quick check before we schedule — roughly how many times a month do you order on Blinkit, and has an order ever arrived damaged, expired, wrong, or fake — or had a refund request that didn't go smoothly?

## 3. Interview logistics
- Target: 5–6 completed interviews, over-recruit by ~30% (aim to schedule 7–8) per `edge-cases.md` mitigation for no-shows.
- 15–20 min each, over call or video, recorded only with explicit verbal consent at the start.
- Keep questions open-ended first (let friction surface unprompted), screening/rating questions last — per `architecture.md` §4 guidance: don't ask "do you distrust X," ask what happened and let them name it.
- Log every candidate — including screened-out and no-shows — in `part2_research_tracker.md`'s Candidate Pipeline table, not just completed ones (keeps the recruitment funnel honest for the deck if asked).

## 4. Consent line (read verbatim at start of call)
> "This is for a research project on shopping habits on quick-commerce apps — not affiliated with Blinkit or any company. I'd like to record this conversation just for my own notes, is that okay? Nothing you say will be shared outside this project, and I can anonymize your name if you'd prefer."

## 5. After each interview
- Write up raw notes within 24 hours (memory fades fast — don't batch this at the end).
- Tag each answer against the theme hypotheses as `confirmed | contradicted | partial | unrelated` — this feeds directly into the theme-confirmation grid for Phase 4.
- Explicitly flag anything the interviewee said that the AI-surfaced theme did NOT predict — this is the "challenged" half of the required deliverable, and it's the easiest thing to lose if you only take notes matching your hypotheses.
