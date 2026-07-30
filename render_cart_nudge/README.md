# Cart → Nudge flow (standalone Render deploy)

Spun out of the main Category Nudge Agent MVP (`mvp/`, deployed clone
`~/blinkit-category-nudge-agent`) because both HF accounts available for this project hit
their compute-Space limits (ZeroGPU quota on the original account; the second account was
gated to the Static SDK, likely pending phone verification). This app is deployed to
**Render** instead, as a separate free-tier Web Service.

## What it is

The single "Cart → Nudge flow" tab from the MVP: pick a synthetic user, add a checkout
cart-filler item (a low-cost item from a category they've never bought — deterministic,
no LLM), and the operator console immediately:
1. Shows a **no-LLM trust reassurance card** for the item just added (refund guarantee +
   verified-brand-seal — the same two top-ranked trust drivers from the survey, applied to
   the added item as static template copy, not invented per item).
2. Fires a **live Groq call** (`llama-3.3-70b-versatile`) that generates the next push
   nudge for a **different** never-bought category — the just-added category is excluded
   from the candidate list the LLM sees, so it can't repeat the same suggestion. This is
   the project's "a new category every month" thesis made concrete.

Real vs. synthetic, same rule as the rest of the project: user profiles are synthetic demo
data; the nudge copy and reasoning are generated live, not canned.

## Files

- `app.py` — trimmed Gradio app: only the Cart → Nudge flow tab (the other MVP tabs —
  Operator console, Auto-nudge queue, Checkout cart-filler, About & methodology — live
  only in the main MVP Space, not here).
- `agent.py`, `friction_matching.py`, `cart_filler.py`, `auto_targeting.py` — copied
  verbatim from the deployed MVP clone. `friction_matching.rank_suggestable_categories()`
  and `agent.generate_nudge()` both gained an `exclude_category` parameter to support the
  chained flow (also present in the main MVP clone — same code, not diverged).
- `data/friction_themes.json`, `data/synthetic_profiles.json` — same synthetic data as the
  main MVP.

## Running locally

```bash
pip install -r requirements.txt
GROQ_API_KEY=... python app.py   # http://127.0.0.1:7860, or $PORT if set
```

## Deploying on Render

1. New → Web Service, connect this GitHub repo, set **Root Directory** to
   `render_cart_nudge`.
2. Environment: Python 3. Build command: `pip install -r requirements.txt`. Start command:
   `python app.py`.
3. Add `GROQ_API_KEY` as an environment variable in the Render dashboard (a separate key
   from the one used by the two HF Spaces, to avoid shared per-key rate-limit contention
   across all three live surfaces).
4. Free tier spins down after ~15 min idle; the first request after that takes 30–60s to
   wake the service. Worth a one-line note wherever this link is shared.
