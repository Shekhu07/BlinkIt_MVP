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
    .setTitle('Section 1: About You & Your Shopping Habits')
    .setHelpText('A few quick background and usage questions.');

  form.addMultipleChoiceItem()
    .setTitle('1. Age range')
    .setChoiceValues(['Under 18', '18–24', '25–34', '35–44', '45+', 'Prefer not to say'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('2. Which Tier City do you live in?')
    .setChoiceValues(['Tier 1', 'Tier 2', 'Tier 3'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('3. What do you do for a living?')
    .setChoiceValues(['Working professional', 'Student', 'Business', 'Self Employed', 'Freelancer'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('4. How often do you currently order from Blinkit?')
    .setChoiceValues(['Daily', '2–3 times a week', 'Once a week', 'A few times a month', 'Rarely / Never'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('5. Which categories do you typically buy on Blinkit? (Select all that apply)')
    .setChoiceValues([
      'Groceries & Staples',
      'Fresh Fruits & Vegetables',
      'Snacks & Beverages',
      'Personal Care & Cosmetics',
      'Electronics & Appliances',
      'Household Essentials & Cleaning',
      'Baby Products',
      'Pet Supplies',
      'Paan Corner'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('6. In the last month, would you say you mostly stick to the same categories, or have you tried something new?')
    .setChoiceValues(['Mostly the same categories', 'Tried one or two new things', 'I regularly explore new categories'])
    .setRequired(true);

  // ---------------- Section 2 ----------------
  form.addPageBreakItem()
    .setTitle('Section 2: Recent Order Experience')
    .setHelpText('This section is about a specific recent order.');

  // Choices (and the branching) are wired up after Sections 3 & 4 exist below,
  // since Google Forms branching needs a reference to the target page.
  var q7 = form.addMultipleChoiceItem()
    .setTitle('7. In the last 3 months, has a Blinkit order arrived damaged, expired, wrong, missing an item, fake/duplicate, or otherwise not as expected?')
    .setRequired(true);

  // ---------------- Section 3 (only reached if Q7 = Yes) ----------------
  var section3 = form.addPageBreakItem()
    .setTitle('Section 3: Tell Us What Happened')
    .setHelpText('(Only shown if Q7 = Yes)');

  form.addMultipleChoiceItem()
    .setTitle('8. Which category was this order in?')
    .setChoiceValues([
      'Groceries & Staples',
      'Fresh Fruits & Vegetables',
      'Snacks & Beverages',
      'Personal Care & Cosmetics',
      'Electronics & Appliances',
      'Household Essentials & Cleaning',
      'Baby Products',
      'Pet Supplies',
      'Paan Corner'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('9. What went wrong with the order?')
    .setChoiceValues([
      'Item arrived damaged',
      'Item arrived expired',
      'Wrong item delivered',
      'Item(s) missing from order',
      'Fake / duplicate product'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('10. How did Blinkit\'s support team resolve this issue?')
    .setChoiceValues([
      'Full refund issued',
      'Replacement item sent',
      'Partial refund',
      'Complaint logged but not resolved',
      'No response / no action taken',
      'I did not contact support'
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('11. Has this changed how you shop on Blinkit since then? (e.g. categories you now avoid — including ones unrelated to what went wrong — or things you double-check before ordering)')
    .setRequired(true);

  // ---------------- Section 4 (everyone lands here) ----------------
  var section4 = form.addPageBreakItem()
    .setTitle('Section 4: Category Exploration')
    .setHelpText(
      'A couple of questions about categories you don\'t currently buy. This section deliberately ' +
      'does not mention quality, refunds, or trust.'
    );

  form.addCheckboxItem()
    .setTitle('12. Which category(ies) on Blinkit have you thought about trying but haven\'t bought yet? (Select all that apply)')
    .setChoiceValues([
      'Groceries & Staples',
      'Fresh Fruits & Vegetables',
      'Snacks & Beverages',
      'Personal Care & Cosmetics',
      'Electronics & Appliances',
      'Household Essentials & Cleaning',
      'Baby Products',
      'Pet Supplies',
      'Paan Corner',
      'None — I\'ve tried everything I\'m interested in'
    ])
    .showOtherOption(true)
    .setRequired(true);

  // ---------------- Section 5 ----------------
  form.addPageBreakItem()
    .setTitle('Section 5: A Few Quick Ratings')
    .setHelpText('Rate how much you agree with each statement.');

  form.addScaleItem()
    .setTitle('13. "If something goes wrong with my order, I trust Blinkit to resolve it quickly and fairly."')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('14. "A bad experience in one category makes me more hesitant to try other categories on Blinkit."')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('15. What would make you more confident trying a category you don\'t currently buy on Blinkit? (Pick up to 2)')
    .setChoiceValues([
      'A clear "no questions asked" return/refund guarantee',
      'Better visible quality/freshness guarantees (e.g. certified, verified brand tags)',
      'Seeing other buyers\' reviews/ratings for that specific item',
      'A human support agent instead of a chatbot for issues',
      'Option to inspect before accepting delivery',
      'Great offers/discounts/promos on first purchase in that category',
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
    .setTitle('16. Anything else about your Blinkit experience you\'d like to share?')
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('17. Would you be open to a quick 10–15 min follow-up call if we have more questions?')
    .setChoiceValues(['Yes', 'No'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('18. If yes, best way to reach you (phone/email) — optional, only used for this research')
    .setRequired(false);

  // ---------------- Wire up Section 2's branching gate (Q7) ----------------
  q7.setChoices([
    q7.createChoice('Yes', section3),
    q7.createChoice('No', section4)
  ]);
  // Section 3 falls through to Section 4 by default (next page in sequence),
  // matching "After this section: Continue to Section 4" in the spec.

  Logger.log('Edit this form: ' + form.getEditUrl());
  Logger.log('Live form link: ' + form.getPublishedUrl());
}
