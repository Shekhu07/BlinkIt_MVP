"""Live single-review extractor — the Two-Step Gated Schema from the real Part 1
pipeline (analysis/extract_themes.py), adapted to run on one pasted review so an
evaluator can watch the discovery engine's core step work in real time.

Same model as the batch pipeline: Groq llama-3.1-8b-instant. Same gate + schema.
Do not change the gate or its wording without updating analysis/extract_themes.py
and the docs — the gate is the core design decision (see CLAUDE.md).

GATE_SPEC below is the single source of the gate wording for this app: batch.py
composes its own multi-review prompt from the same constant, so the single-review
and bulk paths can never drift apart.
"""
import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"

# Verbatim Step-1 gate + Step-2 schema from analysis/extract_themes.py. Shared by the
# single-review path (below) and the bulk path (batch.py) so there is exactly one copy
# of the gate wording in this app.
GATE_SPEC = (
    "Step 1 - Relevance Gate: Check if the text relates to: why a user keeps buying the same category, "
    "why a user has not tried an unfamiliar category, how users discover new products/categories, "
    "a specific moment of considering/trying/rejecting a category, trust or risk about trying something unfamiliar, "
    "or habitual/repeat-purchase patterns. If it is primarily about refunds, support, delivery timing/conduct, "
    "pricing, payments, or general app bugs with no explicit tie to category trial/avoidance, set mentions_category_behavior to false.\n"
    "Step 2 - Extraction: If mentions_category_behavior is true, fill in behavior_type (repeat_purchase | category_avoidance | discovery_friction | new_category_trial), "
    "category_mentioned (groceries | personal_care | pet_supplies | baby_products | electronics | household_essentials | snacks_beverages | other | unspecified), "
    "underlying_reason (one sentence, paraphrased), and sentiment (frustration | neutral_observation | satisfaction | curiosity). "
    "If mentions_category_behavior is false, leave other fields blank or default. "
)

# Single-review wording (the pipeline batches 15 at a time; here we send exactly one).
SYSTEM_PROMPT = (
    "You are an AI extracting specific user behavior from a single review. "
    + GATE_SPEC +
    'Respond ONLY with a JSON object of the exact shape {"mentions_category_behavior": bool, '
    '"behavior_type": str, "category_mentioned": str, "underlying_reason": str, '
    '"sentiment": str, "confidence": float}.'
)


def _client():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not configured")
    return Groq(api_key=key)


def extract_one(review_text, client=None):
    """Run the gated extraction on one review. Returns the parsed dict, plus _model."""
    client = client or _client()
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,
        response_format={"type": "json_object"},
        max_completion_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review to analyze:\n{review_text}"},
        ],
    )
    out = json.loads(resp.choices[0].message.content)
    out["_model"] = GROQ_MODEL
    return out


if __name__ == "__main__":
    samples = [
        "it's selling expired products through the app so I stopped ordering fruits here",
        "Delivery was 10 minutes late and the guy was rude",  # should fail the gate
        "I never buy electronics from here, too scared it'll arrive damaged",
    ]
    c = _client()
    for s in samples:
        r = extract_one(s, client=c)
        print(f"> {s}\n  gate={r.get('mentions_category_behavior')} "
              f"behavior={r.get('behavior_type')} cat={r.get('category_mentioned')}\n")
