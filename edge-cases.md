# Edge Cases, Failure Modes, and Handling Strategies

This document provides a comprehensive catalog of corner cases and failure modes across all system layers defined in the `architecture.md` and `implementation-plan.md` for the Blinkit PM Fellowship Graduation Project.

---

## 1. Data Ingestion Layer (Part 1)
**Components:** Celery, Redis, `google-play-scraper`, `BeautifulSoup`, `Playwright`, JSON processing.

| Component / Sub-System | Failure Mode / Edge Case | Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Play/App Store Scraper** | API rate limits or IP bans triggered by high-frequency polling. | Loss of recent data; pipeline stalling. | Implement exponential backoff. Distribute Celery tasks across timeslots. Use proxy rotation if necessary. |
| **Web Scrapers (MouthShut, CC)** | DOM structure changes (HTML tags modified) breaking `BeautifulSoup` or `Playwright` selectors. | Scraper crashes or returns empty text fields, silently corrupting data. | Wrap extraction logic in `try-except` blocks. Add validation (e.g., minimum character length for a review) before committing to DB. Implement alerting on high failure rates. |
| **Deduplication Engine** | Identical reviews from the same user across different platforms, or slightly edited reviews resulting in different SHA-256 hashes. | Skewed theme clustering (over-counting evidence for a single user). | Use fuzzy matching (e.g., Levenshtein distance or trigram similarity) before insertion if hashes differ slightly. Enforce `ON CONFLICT DO NOTHING` on `source_id`. |
| **App Store JSON Ingest** | Malformed date strings (e.g., timezone parsing failures) in the JSON dump. | DB insertion failure due to invalid `created_at` timestamp. | Wrap `datetime.fromisoformat` in a `try-except`, stripping problematic timezones and defaulting to `datetime.utcnow()` if completely unparseable. |

## 2. Extraction & Clustering Layer (Part 1)
**Components:** TF-IDF Pre-filter, Gemini 1.5 Flash, PostgreSQL.

| Component / Sub-System | Failure Mode / Edge Case | Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **TF-IDF Pre-filter** | Over-filtering reviews containing valid niche problems just because they use rare vocabulary, or under-filtering spam. | Loss of crucial signal; LLM wasted on noise. | Maintain a dynamic threshold. Keep fallback heuristics (e.g., retaining all 1-star and 2-star reviews above 10 words regardless of TF-IDF score). |
| **LLM Extraction (Gemini)** | Rate limits (HTTP 429) or Quota Exhaustion from API. | Pipeline crash during extraction batching. | Implemented retry loop with 35-second `time.sleep()` for HTTP 429s. Limit batch sizes to 50 reviews per call. |
| **LLM Output Formatting** | Gemini responds with malformed JSON, markdown-wrapped JSON (`````json...`````), or missing required schema fields. | JSON decoding error (`json.loads` fails) or DB schema constraint violation. | Use `response_schema` in `GenerationConfig`. If using raw text, strip markdown block quotes. Use `.get('key', 'default')` safely during DB insertion. |
| **Theme Clustering** | "Monolithic Theme" edge case: LLM compresses all 100+ frictions into a single macro-theme (e.g., "Post-Purchase Friction") instead of 3-5 diverse themes. | No segment diversity for Part 2 research. | Adjust the clustering prompt to explicitly mandate mutually exclusive themes. Force rank by sub-categories (e.g., Delivery vs. App UX vs. Item Quality). |

## 3. User Research & Synthesis Layer (Part 2 & 3)
**Components:** Manual interviews, recruitment, problem framing.

| Component / Sub-System | Failure Mode / Edge Case | Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Participant Recruitment** | Scheduled users in the target segment no-show or cancel at the last minute. | Delays Phase 3 synthesis and Phase 4 build; missing deadline. | Over-recruit by 20-30%. Start outreach on Day 8 (before Phase 1 fully closes). Maintain a backup pool of generalized Blinkit users. |
| **Interview Validation** | Users completely contradict the AI-generated macro-themes (e.g., no one cares about "Personal Care Trust"). | Invalidates Part 1's AI engine. | This is a valid research outcome. Document the contradiction explicitly in the synthesis grid (as required by the prompt) and pivot the problem statement to the actual friction discovered during the interview. |
| **Eternal Concall Data** | Investor calls do not mention the specific category/friction identified by the AI (e.g., they only talk about quick commerce expansion, not refunds). | Weak business case for the final deck. | Use generalized statements about "category mix" or "customer retention" from the concalls to build the business case, connecting the dots logically rather than seeking a perfect direct quote. |

## 4. AI-Native MVP Layer (Part 4)
**Components:** FastAPI, Friction-Matching Layer, Gemini Agent Nudge, Synthetic Data.

| Component / Sub-System | Failure Mode / Edge Case | Impact | Handling Strategy & Mitigation |
| :--- | :--- | :--- | :--- |
| **Synthetic Profile Matcher** | A synthetic user's order history does not clearly map to any of the 3 validated macro-themes. | MVP cannot decide which friction nudge to apply. | Implement a "Fallback Theme" (e.g., generic discovery friction) or default to the highest-confidence macro-theme. |
| **Gemini Nudge Generation** | Agent generates hallucinated product categories or features (e.g., suggesting a Blinkit loyalty program that doesn't exist) to solve the friction. | Poor MVP UX; violates Blinkit's actual product constraints. | Strongly prompt the LLM to only suggest real categories. Provide a hardcoded list of valid categories in the prompt context. Enforce a strict schema for the nudge response. |
| **API Endpoint Latency** | The synchronous Gemini API call takes >5 seconds, causing the FastAPI endpoint to timeout or feel sluggish. | Bad demonstration experience for evaluators. | For the MVP, display a loading skeleton on the UI. In a real system, generate nudges asynchronously and cache them, rather than calculating them on-the-fly per request. |
| **Production Deployment** | Hosting platform (Render/Railway/HF Spaces) spins down the free tier instance due to inactivity before the evaluator reviews it. | Evaluator gets a 502/503 error; instant failure for MVP deliverable. | Provide clear instructions in the deck (e.g., "Allow 50 seconds for cold start"). Use a cron job (like `cron-job.org`) to ping the endpoint every 10 minutes to keep it awake during the review window (Aug 4 - Aug 10). |

---

## Conclusion
By anticipating these failure modes across the data, AI, research, and MVP layers, the system architecture ensures resilience. The most critical mitigations are **idempotency in the database**, **robust LLM retry/parsing logic**, and **preventing cold-start deployment failures** during evaluation.
