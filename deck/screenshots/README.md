# Deck screenshots — captured from the LIVE HuggingFace Spaces

Captured 2026-07-24 at 2× device scale (retina-crisp for slides). Every image is a real
screenshot of the deployed apps, with **live Groq generations** — no mockups, no canned copy.

- Discovery engine: https://huggingface.co/spaces/Abhishek292000/blinkit-discovery-engine
- Category Nudge Agent: https://huggingface.co/spaces/Abhishek292000/blinkit-category-nudge-agent

Total ~7 MB, well inside the PRD's 40 MB deck limit.

## Which shot goes on which slide

Slide numbers refer to `docs/deck_design_prompt.md`.

### Slide 3 — the AI discovery engine, how it works
| File | Shows |
|---|---|
| `disc-01-extractor-pass.png` | Live Extractor, **gate PASSED** — a category-avoidance review is kept and structured (behaviour type, category, sentiment). Best single image of the Two-Step Gate working. |
| `disc-02-extractor-reject.png` | Live Extractor, **gate REJECTED** — a pure delivery complaint is dropped. Pair with the one above: this is the design decision that makes the engine work. |
| `disc-03-bulk-run.png` | Bulk Run — an evaluator's own 11 reviews pushed through the full guardrail chain (11 → 7 → 5), every dropped row labelled with the guardrail that dropped it. Use if you want to show the workflow is *testable*, not just described. |

### Slide 4 — what 15,820 reviews said
| File | Shows |
|---|---|
| `disc-04-results-explorer.png` | The real funnel (15,820 → 4,740 → 1,094), ranked themes with evidence counts, source mix, behaviour split, and the 80% LLM-judge validation dial. This is the evidence slide in one image. |

### Slide 8 — the MVP, running
| File | Shows |
|---|---|
| `mvp-01-console-full.png` | Full operator console after a live generation — profile, matched friction theme, agent reasoning, phone preview, measurement plan. The "hero" MVP shot. |
| `mvp-02-phone-nudge.png` | **Phone crop.** The nudge as the shopper sees it: refund guarantee, freshness signal, numbers-free social proof, "Illustrative demo item". Best for a callout-annotated layout. |
| `mvp-03-reasoning-ranked.png` | **Dark reasoning card crop.** Why-this-user / why-this-category / the ranked candidate panel with real adjacency weights / trust drivers / model name. Shows the agent is auditable. |
| `mvp-07-lockscreen.png` | **Lock-screen crop.** 5 live-generated push payloads across 4 distinct categories — proof the agent doesn't collapse onto one suggestion. |
| `mvp-05-auto-queue.png` | Auto-nudge queue: deterministic eligibility gate, funnel (8 → 5 → 5), in-queue vs held-back with per-user reasons. |
| `mvp-06-queue-sent.png` | Same tab after running the batch (queue + lock screen together). |
| `mvp-08-cart-filler.png` | Checkout cart-filler: threshold band, filler carousel, selection logic, adjacency-ranked candidate pool. |

### Slide 9 — how it works + where it breaks (the honesty slide)
| File | Shows |
|---|---|
| `mvp-04-out-of-scope.png` | **The most valuable image in the set.** A low-intent user with no incident: the header reads "out of primary scope" and the banner states the agent does *not* claim the trust fix applies. This is the scope limit visible *in the product*, not just asserted on a slide. |
| `mvp-04b-out-of-scope-full.png` | Full-page version of the same state. |
| `mvp-00-console-before.png` | Pre-generation state — the deterministic layer (theme match + candidate ranking) has already resolved before any LLM runs. Useful to show what is rules-based vs. what is the model. |

## Suggested minimum set
If you only place four images, use: `disc-04-results-explorer` (evidence),
`mvp-02-phone-nudge` (the product), `mvp-07-lockscreen` (it scales + stays diverse),
`mvp-04-out-of-scope` (intellectual honesty). Those four carry the whole story.

## Note for the deck
These are screenshots of synthetic-profile demo data — the apps label this in-product
("Synthetic demo data" pill, "Illustrative demo item"). Keep those labels visible when you
crop; they are part of why the work reads as honest.
