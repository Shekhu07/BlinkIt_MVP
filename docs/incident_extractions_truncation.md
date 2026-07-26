# Incident audit — loss of the 4,740 `extractions` rows (1,094 gate-passing)

**Audited:** 2026-07-26 · **Incident:** 2026-07-24 11:57:27 UTC (17:27:27 IST)
**Status:** cause established · **data RESTORED and verified 2026-07-26** (§6.1) · sandbox hazard §8.1 still open

---

## 1. Finding in one line

A manual `TRUNCATE extractions CASCADE` was executed against the **production** database
(`blinkit_postgres`, port 5432) instead of the sandbox, seven seconds before the same operation was
correctly executed against the sandbox. It emptied `extractions` (4,740 rows, of which 1,094
gate-passing) and, via the foreign key, `theme_evidence`.

**Yes — this is directly related to the `Blinkit_experiment` work.** The sandbox was purpose-built
that morning so prompt re-runs would *not* touch the real 1,094 / 770 results. The clearing step
that workflow requires was aimed at the wrong database.

---

## 2. Timeline (UTC; IST = +5:30)

| Time (2026-07-24) | Event | Evidence |
|---|---|---|
| 11:47:29 | Sandbox planning begins; prod row-count sanity check | session `4e925d24` transcript |
| 11:48:34 | `pg_dump` of the live DB taken → `db_seed.sql`; code rsynced to `~/Blinkit_experiment`; sandbox `.env` set to port **5433** | transcript + file mtime 11:48 |
| 11:48:58 | Sandbox `docker-compose.yml` written — separate container names, ports 5433/6380, separate volume | file contents |
| 11:49:11 | Sandbox stack started, dump restored into it | transcript |
| 11:49:28 | **Isolation verified** — row counts compared 5433 vs 5432, marker row written to sandbox only | transcript |
| 11:50:16 | `SANDBOX_README.md` written, documenting the clear-and-re-run workflow | file contents |
| 11:50:28 | Final check: sandbox scripts resolve to `5433 ✓ (isolated)` | transcript |
| ~11:55:27 | Sandbox seed restore finishes writing | sandbox `raw_reviews`/`themes` mtimes |
| **11:57:27.541** | **TRUNCATE hits PRODUCTION** — `extractions` + `theme_evidence` emptied | prod relfilenode mtimes |
| 11:57:34.434 | Same operation runs against the **sandbox** — 7 seconds later | sandbox `theme_evidence` mtime |
| 12:02:17 | Production Postgres shut down cleanly; not started again until 2026-07-26 | Postgres log |
| 2026-07-26 09:41 | Sandbox re-extraction populates its own `extractions` (3,938 rows / 212 gate-passing) | sandbox `extractions` mtime |
| 2026-07-26 10:03 | Production Postgres started for this audit | Postgres log |

---

## 3. How the mechanism was established

**It was a `TRUNCATE`, not a `DELETE`.** `pg_stat_user_tables` shows `extractions` with 5,260 rows
inserted and only **312** deleted, yet 0 live. A `DELETE` of ~4,950 rows would have incremented
`n_tup_del` accordingly. `TRUNCATE` swaps in a fresh, empty relfilenode without counting tuples.
The sequence `extractions_id_seq` still reads 5,260, so it ran **without** `RESTART IDENTITY`.

**It was one atomic statement.** Six data files were created inside a ~2 ms window at
11:57:27.541–.543, and they map to exactly:

| relfilenode | object |
|---|---|
| 16651 | `extractions` (heap, 0 bytes) |
| 16653 | `extractions_pkey` |
| 16652 / 16654 | `pg_toast_16414` + index |
| 16649 | `theme_evidence` (heap, 0 bytes) |
| 16650 | `theme_evidence_pkey` |

**`theme_evidence` fell to CASCADE, not to a separate command.** It is the FK child of `extractions`
(`theme_evidence_extraction_id_fkey`), so truncating the parent with `CASCADE` necessarily takes it.

**It was not the committed pipeline.** The only `TRUNCATE` in either repo is
[`analysis/cluster_themes.py:137`](../analysis/cluster_themes.py#L137), which targets
`themes, theme_evidence` — the wrong FK direction to reach `extractions` (truncating a child never
touches its parent). Decisively, that script *also* truncates `themes`, and the `themes` data file
has not been modified since 2026-07-18 10:50. `cluster_themes.py` did not run on 07-24.

**It was not the documented sandbox command either.** `SANDBOX_README.md` line 43 reads
`TRUNCATE extractions, themes, theme_evidence, validation_samples CASCADE;` — four tables. On
production, `themes` (3 rows) and `validation_samples` (20 rows) are **intact**. So what ran was
narrower: effectively `TRUNCATE extractions CASCADE`.

**It was not run by Claude.** Zero session events exist across all transcripts between 11:52 and
12:02. The last Claude action was the isolation check at 11:50:28. The statement was issued
manually in a terminal (`~/.zsh_history` has no match, so it was a shell whose history was not
persisted — e.g. an IDE terminal).

---

## 4. Why the safeguards did not catch it

The sandbox isolation was genuinely well built — separate container names, separate ports, separate
volume, detached git origin, and a verified write test. Every one of those guards the **sandbox
scripts**. None of them constrains an ad-hoc `docker exec` typed by hand, because that addresses the
container **by name** and bypasses `.env`, the port mapping, and SQLAlchemy entirely.

Two contributing factors:

1. **Near-identical invocations.** `docker exec blinkit_postgres …` and
   `docker exec blinkit_exp_postgres …` differ by four characters, and both databases are named
   `blinkit_discovery` with the same user and password. Nothing in the prompt or output distinguishes
   them once you are inside `psql`.
2. **The README's own step 2 is a destructive command presented for copy-paste**, with the safety
   resting entirely on the reader not altering the container name.

---

## 5. Impact

| Asset | Status |
|---|---|
| `extractions` (4,740 rows / 1,094 gate-passing) | **Lost from the DB** — recoverable, see §6 |
| `theme_evidence` (75 sample links) | **Lost from the DB** — recoverable, see §6 |
| `raw_reviews` (15,820) · `filtered_reviews` (4,740) | Intact |
| `themes` (770 / 114 / 78) · `validation_samples` (20) · `company_disclosures` (3) | Intact |
| `discovery/data/results.json` | **Unaffected** — exported 2026-07-23 01:40 IST, ~40 h before the incident |
| Both live HF Spaces | **Unaffected** — they read the static `results.json`, no DB in production |
| Deck, docs, published 1,094 / 770 headline | **Unaffected and still valid** |

The published numbers were computed from real rows before the incident and remain correct. The loss
was of the *row-level detail* — the per-review gate decision, category, behaviour type and reason —
i.e. the ability to read the 1,094 individual extractions.

Note on a related point: `evidence_count` remains sound. `cluster_themes.py` sets it to a real count
of matched extractions; the `theme_evidence` table only ever stored up to 25 round-robin samples per
theme ([`cluster_themes.py:164`](../analysis/cluster_themes.py#L164)), so its 75 rows were never the
full 962.

---

## 6. Recovery

**The data is fully recoverable.** The `pg_dump` taken at 11:48 UTC to seed the sandbox — nine
minutes *before* the truncation — survived in the session scratchpad and has been copied out of
`/private/tmp` (which macOS purges) to:

```
~/blinkit_db_backups/db_dump_2026-07-24T1148Z_pre_truncation.sql
sha256 f5b984f50dd4c3ea3962ef0490b9ed650f6ffb929d15a434c081ebcd84764efc   (4,261,310 bytes)
```

Verified contents — it reproduces the published figures exactly:

| Table | Rows in dump |
|---|---|
| `extractions` | **4,740** (of which **1,094** gate-passing) |
| `raw_reviews` / `filtered_reviews` | 15,820 / 4,740 |
| `themes` / `theme_evidence` / `validation_samples` / `company_disclosures` | 3 / 75 / 20 / 3 |

Behaviour split of the 1,094: `category_avoidance` 842, `repeat_purchase` 124,
`discovery_friction` 101, `new_category_trial` 19 — matching `results.json`. Top categories:
groceries 563, unspecified 136, electronics 117 — also matching.

This means a restore rebuilds the original 1,094 **without** re-running the LLM, so the headline is
reproduced exactly rather than resampled.

### 6.1 Restore performed — 2026-07-26

Only `extractions` and `theme_evidence` were loaded (both were empty; nothing else was touched).
A safety dump of the pre-restore state was taken first to
`~/blinkit_db_backups/db_dump_2026-07-26T1036Z_pre_restore.sql`.

Method: the two `COPY` blocks were extracted from the 07-24 dump and applied in a single
transaction, followed by `setval` on both sequences. The full dump was deliberately **not** replayed,
to avoid touching intact tables. The dump's `COPY` carries an explicit 9-column list, so the five
columns added to `extractions` since (`habit_signal`, `discovery_channel`, `info_needed`,
`explorer_signal`, `unmet_need`) restored as NULL — they were unused at the time of the run.

Post-restore verification:

| Check | Result |
|---|---|
| `extractions` | **4,740** ✓ |
| gate-passing | **1,094** ✓ |
| `theme_evidence` | 75 ✓ |
| Orphaned `extractions` → `filtered_reviews` FKs | 0 ✓ |
| Orphaned `theme_evidence` → `extractions` FKs | 0 ✓ |
| Sequences | restored to their original 5,260 / 387 ✓ |
| Behaviour distribution vs `results.json` | **exact match** (1,093 across 5 types) ✓ |
| Category distribution vs `results.json` | **exact match** on all 8 exported categories ✓ |

The published headline is now reproducible from rows again. The two apparent gaps against
`results.json` are the export's own filters, not restore defects:
[`export_results.py:67`](../discovery/export_results.py#L67) applies `limit 8` to categories, and
line 61 excludes `behavior_type = ''` — which is why the DB shows 1,094 categorised rows across 52
values while the export shows 1,020 across 8, and 1,093 behaviour rows rather than 1,094.

**Incidental data-quality note (pre-existing, not caused by the incident):** 44 of the 52 category
values are free text the model emitted outside the enum — `dairy`, `vegetables`, `GNC protein`,
`delivery boy taking extra money` — covering 74 gate-passing rows. The enum in the Step 2 schema is
not enforced post-hoc. Harmless today because the export takes only the top 8, but worth constraining
if the prompt is ever revised.

---

## 7. Recommended hardening

1. **Keep a real backup.** The only surviving copy was an incidental artifact in a temp directory
   that macOS could have deleted at any time. Add a periodic `pg_dump` to `~/blinkit_db_backups/`.
2. **Fix `SANDBOX_README.md` step 2** so the destructive command cannot be mis-aimed — e.g. resolve
   the container into a variable with a guard that refuses the production name:
   ```bash
   EXP=blinkit_exp_postgres
   [ "$EXP" = blinkit_postgres ] && { echo "REFUSING: that is production"; exit 1; }
   docker exec "$EXP" psql -U blinkit_user -d blinkit_discovery -c "TRUNCATE …"
   ```
3. **Make the two databases visually distinct** — rename the sandbox DB to `blinkit_sandbox` so the
   `psql` prompt and every connection string differ, removing the four-character ambiguity.
4. **Revoke destructive rights on prod for day-to-day use** — connect as a role without `TRUNCATE`
   on `extractions`, reserving the owner role for deliberate maintenance.

---

## 8. Sandbox environment — state and a still-live hazard

The sandbox was **not** damaged by the incident; it was the intended target and behaved correctly
(truncated 11:57:34, re-extracted 2026-07-26). Restoring production from the dump cannot affect it —
separate container, volume and port. Three separate issues were found while checking it.

### 8.1 LIVE HAZARD — `prefilter.py` writes to PRODUCTION

`~/Blinkit_experiment/analysis/prefilter.py` is the **only** pipeline script that never calls
`load_dotenv`:

```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://…@localhost:5432/blinkit_discovery")
```

With no `.env` loaded, the fallback applies and it connects to **5432 — production**. The sandbox
`.env` (5433) is never read.

| Sandbox script | Reads `.env`? | Effective target |
|---|---|---|
| `extract_themes.py`, `cluster_themes.py`, `validate_themes.py`, `export_results.py` | yes | 5433 sandbox ✓ |
| **`prefilter.py`** | **no** | **5432 production ✗** |

`SANDBOX_README.md` advertises the sandbox for *"different extraction/**filtering** prompts"*, so
running a modified prefilter is an intended workflow. It dedups, so it will not duplicate existing
rows, but a changed heuristic would silently **add** rows to production's 4,740 `filtered_reviews`,
corrupting the funnel cited in `results.json`, the docs and the deck. The setup-time isolation proof
did not catch this because it exercised only `.env`-loading scripts.

**Fix:** add `from dotenv import load_dotenv; load_dotenv()` to `prefilter.py`, and prefer failing
loudly over defaulting — drop the hardcoded fallback so a missing `DATABASE_URL` raises instead of
silently selecting production.

### 8.2 The experiment run is incomplete

3,938 of 4,740 extractions (802 short), last write 2026-07-26 09:37 UTC. Gate-pass is
**212 / 3,938 ≈ 5.4%** against the 23% baseline (1,094 / 4,740) — a prompt-calibration signal to be
tuned, not a finding to report.

### 8.3 The sandbox still holds the REAL themes

Because the truncate was `extractions CASCADE`, the sandbox `themes` table was untouched and still
contains the seeded production baseline — `Poor Quality…` 770, `Convenience…` 114,
`Discovery Friction…` 78 — while its `extractions` are experimental. `cluster_themes.py` has not run
there (`theme_evidence` = 0). Anyone reading the sandbox DB could mistake the real headline for
experiment output. Re-cluster before interpreting, or clear `themes` so the sandbox never displays
baseline numbers it did not produce.

### 8.4 Shared resources (by design, from setup)

- `~/Blinkit_experiment/venv` is a **symlink** to `Blinkit_PRD/venv` — a `pip install` in the sandbox
  changes this project's packages.
- The **same `GROQ_API_KEY`** is used, so large experiment batches consume the same free-tier quota
  as the two live Spaces.
