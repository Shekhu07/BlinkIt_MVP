/**
 * Builds the Phase 3 Google Form from docs/phase3_google_form.md.
 *
 * How to run:
 * 1. Go to https://script.google.com -> New project.
 * 2. Delete the placeholder code and paste this whole file in.
 * 3. Click Run (▶) with buildPhase3Form selected. Authorize when prompted
 *    (it needs permission to create Forms in your Google account).
 * 4. Open View > Logs (or Executions) to get the edit URL and live form URL.
 *
 * This creates a brand-new Form each time it's run — re-running it will
 * create a duplicate, not update the previous one.
 */
function buildPhase3Form() {
  var form = FormApp.create('Your Quick-Commerce Shopping Experience — A Short Research Survey');
  form.setDescription(
    'This is an independent research project (not affiliated with Blinkit or any company) on how ' +
    'people shop across categories on quick-commerce apps. Takes about 8–10 minutes. Your answers ' +
    'are confidential and can be anonymized on request. There are no wrong answers — we\'re ' +
    'interested in your actual experience.'
  );
  form.setCollectEmail(false);
  form.setShuffleQuestions(false);

  // ---------------- Section 1 ----------------
  form.addPageBreakItem()
    .setTitle('Section 1: About Your Shopping Habits')
    .setHelpText('A few quick questions to understand your usage.');

  form.addMultipleChoiceItem()
    .setTitle('1. How often do you currently order from Blinkit?')
    .setChoiceValues(['Daily', '2–3 times a week', 'Once a week', 'A few times a month', 'Rarely / Never'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('2. Which categories do you typically buy on Blinkit? (Select all that apply)')
    .setChoiceValues([
      'Groceries & Staples',
      'Fresh Fruits & Vegetables',
      'Snacks & Beverages',
      'Personal Care & Cosmetics',
      'Electronics & Appliances',
      'Household Essentials & Cleaning',
      'Baby Products',
      'Pet Supplies'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('3. In the last month, would you say you mostly stick to the same categories, or have you tried something new?')
    .setChoiceValues(['Mostly the same categories', 'Tried one or two new things', 'I regularly explore new categories'])
    .setRequired(true);

  // ---------------- Section 2 ----------------
  form.addPageBreakItem()
    .setTitle('Section 2: Recent Order Experience')
    .setHelpText('This section is about a specific recent order.');

  // Choices (and the branching) are wired up after Sections 3 & 4 exist below,
  // since Google Forms branching needs a reference to the target page.
  var q4 = form.addMultipleChoiceItem()
    .setTitle('4. In the last 3 months, has a Blinkit order arrived damaged, expired, wrong, missing an item, fake/duplicate, or otherwise not as expected?')
    .setRequired(true);

  // ---------------- Section 3 (only reached if Q4 = Yes) ----------------
  var section3 = form.addPageBreakItem()
    .setTitle('Section 3: Tell Us What Happened')
    .setHelpText('(Only shown if Q4 = Yes)');

  form.addParagraphTextItem()
    .setTitle('5. What happened, exactly? Which category was it, and what went wrong?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('6. What did you do next, and how did Blinkit\'s support/refund process handle it?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('7. Did that experience change how you shop on Blinkit afterward — categories you now avoid, or things you double-check before ordering?')
    .setRequired(true);

  // ---------------- Section 4 (everyone lands here) ----------------
  var section4 = form.addPageBreakItem()
    .setTitle('Section 4: Category Exploration')
    .setHelpText(
      'A couple of questions about categories you don\'t currently buy. This section deliberately ' +
      'does not mention quality, refunds, or trust.'
    );

  form.addParagraphTextItem()
    .setTitle('8. Is there a category on Blinkit you don\'t currently buy but have thought about trying? What\'s stopped you so far?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('9. (If you answered Yes to Q4) Would that past experience make you hesitant to try a completely different, unrelated category on Blinkit? Why or why not?')
    .setRequired(false);

  // ---------------- Section 5 ----------------
  form.addPageBreakItem()
    .setTitle('Section 5: A Few Quick Ratings')
    .setHelpText('Rate how much you agree with each statement.');

  form.addScaleItem()
    .setTitle('10. "If something goes wrong with my order, I trust Blinkit to resolve it quickly and fairly."')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('11. "A bad experience in one category makes me more hesitant to try other categories on Blinkit."')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('12. What would make you more confident trying a category you don\'t currently buy on Blinkit? (Pick up to 2)')
    .setChoiceValues([
      'A clear "no questions asked" return/refund guarantee',
      'Better visible quality/freshness guarantees (e.g. certified, verified brand tags)',
      'Seeing other buyers\' reviews/ratings for that specific item',
      'A human support agent instead of a chatbot for issues',
      'Option to inspect before accepting delivery',
      'Nothing in particular — I just don\'t need those categories'
    ])
    .showOtherOption(true)
    .setValidation(FormApp.createCheckboxValidation().requireSelectAtMost(2).build())
    .setRequired(true);

  // ---------------- Section 6 ----------------
  form.addPageBreakItem()
    .setTitle('Section 6: Wrap-Up')
    .setHelpText('Almost done — just a couple more things.');

  form.addParagraphTextItem()
    .setTitle('13. Anything else about your Blinkit experience you\'d like to share?')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('14. Would you be open to a quick 10–15 min follow-up call if we have more questions?')
    .setChoiceValues(['Yes', 'No'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('15. If yes, best way to reach you (phone/email) — optional, only used for this research')
    .setRequired(false);

  // ---------------- Wire up Section 2's branching gate (Q4) ----------------
  q4.setChoices([
    q4.createChoice('Yes', section3),
    q4.createChoice('No', section4)
  ]);
  // Section 3 falls through to Section 4 by default (next page in sequence),
  // matching "After this section: Continue to Section 4" in the spec.

  Logger.log('Edit this form: ' + form.getEditUrl());
  Logger.log('Live form link: ' + form.getPublishedUrl());
}
