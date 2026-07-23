"""Bulk review upload — runs an evaluator's own file through the SAME guardrails as
the real Part 1 pipeline, so the workflow can be tested end to end rather than only
read about in the Results Explorer.

Stages mirrored, in order, from the real pipeline:

  Stage 0  dedup           scrapers/ingest_master_json.py  (md5 of source+author+content[:100],
                                                            UNIQUE source_id in schema.sql)
  Stage 1  heuristic filter analysis/prefilter.py          (empty / <5 words / rating==5)
  Stage 2  gated extraction analysis/extract_themes.py     (Two-Step Gate, 15 per Groq call)
  Stage 3  combo grouping   analysis/cluster_themes.py     (deterministic category x behavior counts)

Every row that is dropped carries an explicit reason string naming the guardrail that
dropped it — that is the point of the feature: an evaluator should see the filtering
happen, not just the survivors.

Input is PASTED TEXT, not a file component, and that is deliberate: on the Gradio
version these Spaces run (4.44.1 / gradio_client 1.3.0), using gr.File or
gr.UploadButton as an *event input* crashes app startup — API-schema generation
raises "TypeError: argument of type 'bool' is not iterable" and the server never
binds. Verified locally; gr.File renders fine until it is wired to a .click().
Fixing it needs a Gradio 5.x bump, which is not worth the blast radius on a live
submission link. parse_reviews() therefore accepts CSV text, JSON text, or plain
newline-separated reviews — the same three shapes a file would have carried.

Deliberate differences from the real pipeline, and why:
  * MAX_ROWS cap (50). Both Spaces share one free-tier Groq key; an uncapped run
    could exhaust the quota and take down the Live Extractor and the MVP with it.
  * No Postgres. Production has no DB — everything here is in-memory and per-request.
  * Stage 3 stops at deterministic (category x behavior_type) counts and does NOT run
    the LLM theme-naming step. Naming macro-themes off <=50 rows would manufacture
    findings; the real themes come from 1,094 gate-passing extractions and are shown,
    unchanged, in the Results Explorer.

Nothing in here writes to data/results.json or to any pipeline artifact.
"""
import csv
import io
import json
import time
from collections import defaultdict

from extractor import GATE_SPEC, GROQ_MODEL, _client

MAX_ROWS = 50
BATCH_SIZE = 15          # same as analysis/extract_themes.py
MIN_WORDS = 5            # same as analysis/prefilter.py
DROP_RATING = 5          # same as analysis/prefilter.py

CONTENT_KEYS = ("content", "review", "review_text", "text", "body", "comment")
RATING_KEYS = ("rating", "stars", "star", "score")
SOURCE_KEYS = ("source", "platform", "site")
AUTHOR_KEYS = ("author", "user", "username", "name")

# Multi-review wording, composed from the SAME gate constant the single-review path
# uses. Mirrors the batch prompt in analysis/extract_themes.py.
BATCH_PROMPT = (
    "You are an AI extracting specific user behavior from reviews. "
    + GATE_SPEC +
    "Maintain the Review ID provided. "
    'Respond ONLY with a JSON object of the exact shape {"extractions": [{"review_id": int, '
    '"mentions_category_behavior": bool, "behavior_type": str, "category_mentioned": str, '
    '"underlying_reason": str, "sentiment": str, "confidence": float}, ...]}.'
)


class UploadError(Exception):
    """File-level problem — nothing was processed."""


def _pick(row, keys):
    lowered = {str(k).strip().lower(): v for k, v in row.items() if k is not None}
    for k in keys:
        if k in lowered and str(lowered[k]).strip() not in ("", "None"):
            return lowered[k]
    return None


def _coerce_rating(value):
    if value is None:
        return None
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None


def _detect(text):
    """json | csv | lines. Header-match for CSV, because review text is full of commas."""
    head = text.lstrip()
    if head[:1] in ("[", "{"):
        return "json"
    first = head.splitlines()[0].lower()
    if "," in first and any(k in [c.strip().strip('"') for c in first.split(",")]
                            for k in CONTENT_KEYS):
        return "csv"
    return "lines"


def parse_reviews(text):
    """Parse pasted CSV / JSON / newline-separated reviews. Raises UploadError."""
    if not text or not text.strip():
        raise UploadError("Nothing pasted — add some reviews first.")

    fmt = _detect(text)

    if fmt == "json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise UploadError(f"Not valid JSON — {e.msg} (line {e.lineno}).") from e
        if isinstance(data, dict):
            # tolerate {"reviews": [...]} style wrappers
            for key in ("reviews", "data", "rows", "items"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise UploadError(
                'JSON must be a list of review objects, or an object with a "reviews" list.')
        raw_rows = [r for r in data if isinstance(r, dict)]
        if not raw_rows and data:
            # a bare list of strings is a reasonable thing for someone to paste
            raw_rows = [{"content": r} for r in data if isinstance(r, str)]
    elif fmt == "csv":
        try:
            raw_rows = list(csv.DictReader(io.StringIO(text)))
        except csv.Error as e:
            raise UploadError(f"Could not parse the CSV: {e}") from e
    else:
        raw_rows = [{"content": ln} for ln in text.splitlines() if ln.strip()]

    if not raw_rows:
        raise UploadError("No review rows found.")

    rows = []
    for i, r in enumerate(raw_rows, start=1):
        content = _pick(r, CONTENT_KEYS)
        rows.append({
            "n": i,
            "content": "" if content is None else str(content).strip(),
            "rating": _coerce_rating(_pick(r, RATING_KEYS)),
            "source": str(_pick(r, SOURCE_KEYS) or "upload").strip()[:40],
            "author": str(_pick(r, AUTHOR_KEYS) or "user").strip()[:60],
        })

    if not any(r["content"] for r in rows):
        raise UploadError(
            "No review text found. Expected a column or key named one of: "
            + ", ".join(CONTENT_KEYS) + ".")

    if len(rows) > MAX_ROWS:
        raise UploadError(
            f"{len(rows):,} rows found — this demo is capped at {MAX_ROWS}. "
            "The cap protects a Groq free-tier quota shared with the MVP Space; "
            "trim the input and retry.")

    has_rating = any(r["rating"] is not None for r in rows)
    return rows, has_rating


def prefilter(rows):
    """Stage 0 + Stage 1. Returns (kept, dropped) — dropped rows carry a `reason`."""
    kept, dropped, seen = [], [], set()
    for r in rows:
        content = r["content"]

        if not content:
            dropped.append({**r, "stage": "Stage 1 · heuristic filter",
                            "reason": "Empty review text — no content to extract from."})
            continue

        # Stage 0 — same dedup key as scrapers/ingest_master_json.py
        key = f"{r['source']}_{r['author']}_{content[:100]}"
        if key in seen:
            dropped.append({**r, "stage": "Stage 0 · dedup",
                            "reason": "Duplicate of an earlier row (same source + author + "
                                      "opening 100 characters) — UNIQUE source_id would reject it."})
            continue
        seen.add(key)

        if len(content.split()) < MIN_WORDS:
            dropped.append({**r, "stage": "Stage 1 · heuristic filter",
                            "reason": f"Under {MIN_WORDS} words — too short to carry an "
                                      "extractable reason."})
            continue

        if r["rating"] == DROP_RATING:
            dropped.append({**r, "stage": "Stage 1 · heuristic filter",
                            "reason": f"{DROP_RATING}-star review — the corpus is deliberately "
                                      "biased toward friction, not praise."})
            continue

        kept.append(r)
    return kept, dropped


def _call_groq(client, chunk):
    batch_text = "Here are the reviews to analyze:\n\n"
    for r in chunk:
        batch_text += f"Review ID: {r['n']}\nContent: {r['content']}\n---\n"

    last_error = None
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "system", "content": BATCH_PROMPT},
                          {"role": "user", "content": batch_text}],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_completion_tokens=3500,
            )
            return json.loads(resp.choices[0].message.content).get("extractions", [])
        except json.JSONDecodeError as e:
            last_error = f"model returned malformed JSON ({e.msg})"
            time.sleep(2)
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "rate_limit" in msg.lower() or "429" in msg:
                last_error = "Groq rate limit reached"
                time.sleep(8)
            else:
                raise UploadError(f"Extraction call failed: {msg}") from e
    raise UploadError(f"Extraction failed after 3 attempts — {last_error}.")


def extract(kept, progress=None):
    """Stage 2 — the Two-Step Gate, batched 15 at a time exactly like the pipeline."""
    if not kept:
        return [], []
    client = _client()
    by_id = {r["n"]: r for r in kept}
    passed, rejected = [], []

    chunks = [kept[i:i + BATCH_SIZE] for i in range(0, len(kept), BATCH_SIZE)]
    for idx, chunk in enumerate(chunks, start=1):
        if progress is not None:
            progress((idx - 1) / len(chunks),
                     desc=f"Gated extraction — batch {idx}/{len(chunks)}")
        for data in _call_groq(client, chunk):
            row = by_id.get(data.get("review_id"))
            if row is None:
                continue          # model invented an ID; drop rather than misattribute
            # NB: "underlying_reason" is the model's output; "reason" is reserved
            # throughout this module for why a row was DROPPED. Keep them distinct.
            rec = {**row,
                   "behavior_type": (data.get("behavior_type") or "unknown"),
                   "category": (data.get("category_mentioned") or "unspecified"),
                   "underlying_reason": data.get("underlying_reason") or "",
                   "sentiment": data.get("sentiment") or "unknown",
                   "confidence": data.get("confidence")}
            if data.get("mentions_category_behavior"):
                passed.append(rec)
            else:
                rejected.append({**rec, "stage": "Stage 2 · relevance gate",
                                 "reason": "Gate rejected — general service complaint "
                                           "(refund / delivery / pricing / bug) with no explicit "
                                           "tie to trying or avoiding a category."})

    # A row the model silently omitted is not a pass — record it, don't lose it.
    accounted = {r["n"] for r in passed} | {r["n"] for r in rejected}
    for r in kept:
        if r["n"] not in accounted:
            rejected.append({**r, "stage": "Stage 2 · relevance gate",
                             "reason": "No verdict returned for this row (model omitted it) — "
                                       "counted as not-passing rather than assumed relevant.",
                             "behavior_type": "unknown", "category": "unspecified",
                             "underlying_reason": "", "sentiment": "unknown",
                             "confidence": None})
    return passed, rejected


def group(passed):
    """Stage 3 — deterministic (category x behavior_type) counts. No LLM, no naming."""
    combos = defaultdict(list)
    for e in passed:
        combos[(e["category"] or "unspecified", e["behavior_type"] or "unknown")].append(e)
    return sorted(
        ({"category": c, "behavior_type": b, "count": len(items)}
         for (c, b), items in combos.items()),
        key=lambda x: -x["count"])


def run(text, progress=None):
    """Full bulk run over pasted text. Raises UploadError for anything the user can fix."""
    rows, has_rating = parse_reviews(text)
    if progress is not None:
        progress(0.05, desc="Parsed input — applying heuristic filter")
    kept, dropped = prefilter(rows)
    passed, rejected = extract(kept, progress=progress)
    if progress is not None:
        progress(0.95, desc="Grouping gate-passing extractions")
    return {
        "total": len(rows),
        "has_rating": has_rating,
        "kept": kept,
        "dropped": dropped,
        "passed": passed,
        "rejected": rejected,
        "combos": group(passed),
        "model": GROQ_MODEL,
    }
