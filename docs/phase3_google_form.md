# Phase 3 Interview Questionnaire — Google Forms Build Sheet

**This is the canonical Phase 3 questionnaire** — built directly from the real Part 1 theme ("Poor Quality and Unreliable Products," 770/1,094 gate-passing extractions, spanning groceries/electronics/snacks/household/personal care). It supersedes the earlier drafts in `user_interview_survey.md` and `user_research_survey_phase3.md`, which were written before the real theme was confirmed.

Structured for direct copy-paste into Google Forms, including section breaks and branching logic. Question type labels (`[Short answer]`, `[Paragraph]`, etc.) match Google Forms' actual option names exactly.

**Design notes** (per `architecture.md` §4 guidance — don't lead the respondent):
- Open-ended questions come before rating/multiple-choice ones in every section, so friction surfaces unprompted before you show your hypothesis.
- The category-exploration question (Section 4, Q7) does **not** mention quality, trust, or refunds — it's deliberately blind, so a respondent naming that friction on their own is a real confirmation, not a leading answer.
- Branching (Section 2's gate question) uses Google Forms' native "go to section based on answer" — only works on Multiple Choice questions, which is why the gate is structured that way.

---

## Form Settings
- **Title**: Your Quick-Commerce Shopping Experience — A Short Research Survey
- **Description**: "This is an independent research project (not affiliated with Blinkit or any company) on how people shop across categories on quick-commerce apps. Takes about 8–10 minutes. Your answers are confidential and can be anonymized on request. There are no wrong answers — we're interested in your actual experience."
- **Collect email addresses**: Off (keep anonymous by default; contact info collected separately at the end, optional)
- **Shuffle question order**: Off
- Enable **"Go to section based on answer"** on the Section 2 gate question (see below)

---

## Section 1: About Your Shopping Habits
*Description: A few quick questions to understand your usage.*

**1. How often do you currently order from Blinkit?**
`[Multiple choice]`
- Daily
- 2–3 times a week
- Once a week
- A few times a month
- Rarely / Never

**2. Which categories do you typically buy on Blinkit? (Select all that apply)**
`[Checkboxes]`
- Groceries & Staples
- Fresh Fruits & Vegetables
- Snacks & Beverages
- Personal Care & Cosmetics
- Electronics & Appliances
- Household Essentials & Cleaning
- Baby Products
- Pet Supplies
- Other: ______

**3. In the last month, would you say you mostly stick to the same categories, or have you tried something new?**
`[Multiple choice]`
- Mostly the same categories
- Tried one or two new things
- I regularly explore new categories

---

## Section 2: Recent Order Experience
*Description: This section is about a specific recent order.*

**4. In the last 3 months, has a Blinkit order arrived damaged, expired, wrong, missing an item, fake/duplicate, or otherwise not as expected?**
`[Multiple choice]` — **branching question**
- Yes → *Go to Section 3*
- No → *Go to Section 4*

---

## Section 3: Tell Us What Happened
*(Only shown if Q4 = Yes)*

**5. What happened, exactly? Which category was it, and what went wrong?**
`[Paragraph]`

**6. What did you do next, and how did Blinkit's support/refund process handle it?**
`[Paragraph]`

**7. Did that experience change how you shop on Blinkit afterward — categories you now avoid, or things you double-check before ordering?**
`[Paragraph]`

*After this section: Continue to Section 4*

---

## Section 4: Category Exploration
*Description: A couple of questions about categories you don't currently buy.*
*(Shown to everyone — this section deliberately does not mention quality, refunds, or trust; if a respondent brings those up unprompted here, that's a genuine confirmation signal, not a leading answer.)*

**8. Is there a category on Blinkit you don't currently buy but have thought about trying? What's stopped you so far?**
`[Paragraph]`

**9. (If you answered Yes to Q4) Would that past experience make you hesitant to try a completely different, unrelated category on Blinkit? Why or why not?**
`[Paragraph]` — mark as optional, since Section 3 respondents only

---

## Section 5: A Few Quick Ratings
*Description: Rate how much you agree with each statement.*

**10. "If something goes wrong with my order, I trust Blinkit to resolve it quickly and fairly."**
`[Linear scale 1–5]` — 1: Strongly Disagree → 5: Strongly Agree

**11. "A bad experience in one category makes me more hesitant to try other categories on Blinkit."**
`[Linear scale 1–5]` — 1: Strongly Disagree → 5: Strongly Agree

**12. What would make you more confident trying a category you don't currently buy on Blinkit? (Pick up to 2)**
`[Checkboxes]`
- A clear "no questions asked" return/refund guarantee
- Better visible quality/freshness guarantees (e.g. certified, verified brand tags)
- Seeing other buyers' reviews/ratings for that specific item
- A human support agent instead of a chatbot for issues
- Option to inspect before accepting delivery
- Nothing in particular — I just don't need those categories
- Other: ______

---

## Section 6: Wrap-Up
*Description: Almost done — just a couple more things.*

**13. Anything else about your Blinkit experience you'd like to share?**
`[Paragraph]` — Optional

**14. Would you be open to a quick 10–15 min follow-up call if we have more questions?**
`[Multiple choice]`
- Yes
- No

**15. If yes, best way to reach you (phone/email) — optional, only used for this research**
`[Short answer]` — Optional

---

## After collecting responses
- Log every respondent (including screened-out ones) in `part2_research_tracker.md`'s Candidate Pipeline table.
- For anyone who answered Yes to Q4, their Section 3 + Section 4 answers are your primary raw material for the theme-confirmation grid (theme × confirmed/contradicted × supporting quote) — copy direct quotes, don't paraphrase, so Phase 4 can cite them.
- Watch Q8 specifically for **unprompted** mentions of quality/trust/refund language — that's the strongest form of confirmation since the question doesn't lead there. If most respondents name something else entirely (price, delivery speed, lack of need), that's a real contradiction worth documenting, not a result to discard.
