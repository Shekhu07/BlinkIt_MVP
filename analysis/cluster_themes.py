import os
import json
import time
from collections import defaultdict
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-8b-instant"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Extraction(Base):
    __tablename__ = "extractions"
    id = Column(Integer, primary_key=True)
    filtered_review_id = Column(Integer)
    mentions_category_behavior = Column(Boolean)
    behavior_type = Column(String(100))
    category = Column(String(100))
    reason = Column(Text)
    sentiment = Column(String(100))
    confidence = Column(Float)

class Theme(Base):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    theme_name = Column(String(255))
    description = Column(Text)
    user_segment = Column(String(255))
    evidence_count = Column(Integer)

class ThemeEvidence(Base):
    __tablename__ = "theme_evidence"
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer)
    extraction_id = Column(Integer)

def cluster_themes():
    session = SessionLocal()
    try:
        extractions = session.query(Extraction).filter(Extraction.mentions_category_behavior == True).all()
        if not extractions:
            print("No gate-passing extractions found to cluster.")
            return

        # Group by (category, behavior_type) combo — real, DB-backed counts, not LLM guesses.
        # A single free-text clustering call over 1000+ reasons blows every free-tier token
        # budget; clustering the ~20 combo keys instead is small enough to fit and lets us
        # compute evidence_count deterministically afterward.
        combos = defaultdict(list)
        for e in extractions:
            combos[(e.category or "unspecified", e.behavior_type or "unknown")].append(e)

        # Keep only the top combos by volume — the long tail contributes negligible evidence
        # and blows the free-tier per-request token budget if included. Large combos are
        # internally heterogeneous (e.g. "groceries|category_avoidance" mixes quality, refund,
        # and competitor-comparison complaints), so a single example reason isn't enough signal
        # to name them accurately — sample more examples per combo, fewer combos, to compensate.
        top_combos = sorted(combos.items(), key=lambda kv: -len(kv[1]))[:12]

        combo_summaries = []
        for (category, behavior_type), items in top_combos:
            sample_size = min(6, len(items))
            step = max(1, len(items) // sample_size)
            examples = [i.reason[:100] for i in items[::step][:sample_size] if i.reason]
            combo_summaries.append({
                "key": f"{category}|{behavior_type}",
                "category": category,
                "behavior_type": behavior_type,
                "count": len(items),
                "examples": examples
            })

        print(f"Found {len(extractions)} gate-passing extractions across {len(combo_summaries)} category/behavior combos. Sending combos to Groq for clustering...")

        combos_text = json.dumps(combo_summaries, indent=1)
        prompt = (
            "You are a Lead Product Manager. Below is a JSON list of (category, behavior_type) combinations "
            "extracted from user reviews about a quick-commerce app, each with a real count of how many reviews "
            "matched it and 1-2 example reasons.\n"
            "Your job is to cluster these combos into the Top 3 to 5 macro-themes explaining why users don't "
            "explore new categories on the platform.\n"
            "For each theme, provide: theme_name, description, user_segment, and combo_keys "
            "(the exact 'key' strings from the input list that belong to this theme — every combo must be "
            "assigned to exactly one theme).\n\n"
            'Respond ONLY with a JSON object of the exact shape {"themes": [{"theme_name": str, "description": str, '
            '"user_segment": str, "combo_keys": [str, ...]}, ...]}.\n\n'
            f"Combos:\n{combos_text}"
        )

        themes_data = None
        for attempt in range(5):
            try:
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_completion_tokens=1500
                )
                themes_data = json.loads(response.choices[0].message.content).get("themes", [])
                break
            except json.JSONDecodeError:
                print(f"Bad JSON generated (attempt {attempt+1}/5). Retrying in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    print(f"Rate limited (attempt {attempt+1}/5). Waiting 20 seconds...")
                    time.sleep(20)
                else:
                    raise e

        if themes_data is None:
            print("All 5 attempts failed. Aborting without touching the themes table.")
            return

        key_to_items = {c["key"]: combos[(c["category"], c["behavior_type"])] for c in combo_summaries}

        # The model is asked to assign each combo to exactly one theme but isn't reliable about
        # it — enforce exclusivity in Python: first theme (in returned order) to claim a combo
        # key keeps it, later claims are dropped. Otherwise evidence_count can double-count.
        claimed_keys = set()
        for t in themes_data:
            deduped = []
            for key in t.get("combo_keys", []):
                if key not in claimed_keys:
                    deduped.append(key)
                    claimed_keys.add(key)
            t["combo_keys"] = deduped

        session.execute(text("TRUNCATE TABLE themes, theme_evidence CASCADE"))

        saved = 0
        for t in themes_data:
            matched_groups = [key_to_items.get(key, []) for key in t.get("combo_keys", [])]
            matched_groups = [g for g in matched_groups if g]
            if not matched_groups:
                print(f"Skipping theme '{t.get('theme_name')}' — no combo_keys matched any real data.")
                continue
            total_matched = sum(len(g) for g in matched_groups)

            theme = Theme(
                theme_name=t.get('theme_name', '')[:255],
                description=t.get('description', ''),
                user_segment=t.get('user_segment', '')[:255],
                evidence_count=total_matched
            )
            session.add(theme)
            session.flush()

            # Round-robin across combo groups so stored evidence represents every sub-category
            # in the theme, not just whichever combo happened to be largest/first.
            sample = []
            round_num = 0
            while len(sample) < min(25, total_matched):
                for group in matched_groups:
                    if round_num < len(group):
                        sample.append(group[round_num])
                round_num += 1
            for item in sample[:25]:
                session.add(ThemeEvidence(theme_id=theme.id, extraction_id=item.id))

            saved += 1

        session.commit()
        print(f"Successfully clustered and saved {saved} macro-themes with real evidence_count + linked theme_evidence rows.")

    except Exception as e:
        session.rollback()
        print(f"Error during clustering: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    cluster_themes()
