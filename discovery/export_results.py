"""One-time build tool: export the real Part 1 discovery-engine results from Postgres
to discovery/data/results.json, so the deployed Results Explorer needs no live DB.

Run once (with docker-compose up and the pipeline already populated):
    ./venv/bin/python discovery/export_results.py

Re-run only if the pipeline is re-run and the numbers change (keep docs in sync).
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

OUT = Path(__file__).parent / "data" / "results.json"
engine = create_engine(
    os.getenv("DATABASE_URL",
              "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
)


def rows(c, q, **p):
    return [dict(r._mapping) for r in c.execute(text(q), p)]


def main():
    with engine.connect() as c:
        funnel = {
            "raw_reviews": c.execute(text("select count(*) from raw_reviews")).scalar(),
            "filtered_reviews": c.execute(text("select count(*) from filtered_reviews")).scalar(),
            "extractions_total": c.execute(text("select count(*) from extractions")).scalar(),
            "gate_pass": c.execute(text(
                "select count(*) from extractions where mentions_category_behavior=true")).scalar(),
        }

        source_mix = rows(c, "select source, count(*) n from raw_reviews group by source order by n desc")

        themes = rows(c, """
            select id, theme_name, description, user_segment, evidence_count
            from themes order by evidence_count desc""")
        gate = funnel["gate_pass"]
        for t in themes:
            t["evidence_share"] = round(t["evidence_count"] / gate, 3) if gate else None
            # a few real evidence quotes per theme
            t["sample_evidence"] = rows(c, """
                select rr.content as review, rr.source, e.category, e.behavior_type, e.reason
                from theme_evidence te
                join extractions e on e.id = te.extraction_id
                join filtered_reviews fr on fr.id = e.filtered_review_id
                join raw_reviews rr on rr.id = fr.raw_review_id
                where te.theme_id = :tid
                  and rr.content is not null and length(rr.content) between 30 and 400
                order by length(rr.content)
                limit 4""", tid=t["id"])

        behavior_dist = rows(c, """
            select behavior_type, count(*) n from extractions
            where mentions_category_behavior=true and behavior_type <> ''
            group by behavior_type order by n desc""")

        category_dist = rows(c, """
            select category, count(*) n from extractions
            where mentions_category_behavior=true
            group by category order by n desc limit 8""")

        val = rows(c, """
            select llm_validation_status status, count(*) n
            from validation_samples group by llm_validation_status order by n desc""")
        validation = {"total": sum(v["n"] for v in val),
                      "breakdown": {v["status"]: v["n"] for v in val}}

        disclosures = rows(c, """
            select source_document, signal_type, content_snippet
            from company_disclosures order by id""")

    out = {
        "_meta": {
            "description": "Real Part 1 AI discovery-engine results, exported from Postgres. "
                           "NOT synthetic — these are the actual pipeline outputs cited across docs/.",
            "generated_by": "discovery/export_results.py",
        },
        "funnel": funnel,
        "source_mix": source_mix,
        "themes": themes,
        "behavior_distribution": behavior_dist,
        "category_distribution": category_dist,
        "validation": validation,
        "company_disclosures": disclosures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"Wrote {OUT}")
    print(f"  {funnel['raw_reviews']} raw -> {funnel['filtered_reviews']} filtered -> "
          f"{funnel['gate_pass']} gate-pass; {len(themes)} themes; "
          f"validation {validation['breakdown']}")


if __name__ == "__main__":
    main()
