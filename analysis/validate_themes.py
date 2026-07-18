import os
import json
import time
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-8b-instant"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Theme(Base):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    theme_name = Column(String(255))
    description = Column(Text)
    user_segment = Column(String(255))
    evidence_count = Column(Integer)

class RawReview(Base):
    __tablename__ = "raw_reviews"
    id = Column(Integer, primary_key=True)
    content = Column(Text)

class FilteredReview(Base):
    __tablename__ = "filtered_reviews"
    id = Column(Integer, primary_key=True)
    raw_review_id = Column(Integer)

class Extraction(Base):
    __tablename__ = "extractions"
    id = Column(Integer, primary_key=True)
    filtered_review_id = Column(Integer)
    mentions_category_behavior = Column(Boolean)
    behavior_type = Column(String(100))
    category = Column(String(100))

class ThemeEvidence(Base):
    __tablename__ = "theme_evidence"
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer)
    extraction_id = Column(Integer)

class ValidationSample(Base):
    __tablename__ = "validation_samples"
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer)
    sample_review_id = Column(Integer)
    human_validation_status = Column(String(50))
    llm_validation_status = Column(String(50))

def validate_themes():
    session = SessionLocal()
    try:
        # Get top theme
        top_theme = session.query(Theme).order_by(Theme.evidence_count.desc(), Theme.id.desc()).first()
        if not top_theme:
            print("No themes found.")
            return

        print(f"Top Theme: {top_theme.theme_name}")

        # Derive the theme's real (category, behavior_type) signature from its stored evidence
        # sample, then pull a HELD-OUT sample of matching raw reviews (excluding the ones already
        # used as theme_evidence) — validating against reviews that actually relate to the theme,
        # not arbitrary raw_reviews (which are mostly generic 5-star "good"/"nice" noise).
        evidence_extraction_ids = [
            te.extraction_id for te in session.query(ThemeEvidence).filter(ThemeEvidence.theme_id == top_theme.id).all()
        ]
        signature_rows = session.query(Extraction.category, Extraction.behavior_type).filter(
            Extraction.id.in_(evidence_extraction_ids)
        ).distinct().all()
        categories = [c for c, _ in signature_rows]
        behavior_types = [b for _, b in signature_rows]

        matching_extractions = session.query(Extraction).filter(
            Extraction.mentions_category_behavior == True,
            Extraction.category.in_(categories),
            Extraction.behavior_type.in_(behavior_types),
            ~Extraction.id.in_(evidence_extraction_ids)
        ).limit(200).all()

        filtered_to_raw = {
            fr.id: fr.raw_review_id for fr in session.query(FilteredReview).filter(
                FilteredReview.id.in_([e.filtered_review_id for e in matching_extractions])
            ).all()
        }
        raw_ids = list({filtered_to_raw[e.filtered_review_id] for e in matching_extractions if e.filtered_review_id in filtered_to_raw})[:20]

        reviews = session.query(RawReview).filter(RawReview.id.in_(raw_ids)).all()
        if not reviews:
            print("No held-out theme-relevant reviews found.")
            return

        print(f"Validating against {len(reviews)} held-out reviews matching the theme's real signature: {list(zip(categories, behavior_types))[:5]}...")

        reviews_text = ""
        for r in reviews:
            reviews_text += f"Review ID: {r.id}\nContent: {r.content}\n---\n"

        prompt = (
            f"You are an objective judge evaluating whether user reviews support a given theme.\n"
            f"Theme: {top_theme.theme_name}\n"
            f"Theme Description: {top_theme.description}\n\n"
            f"For each review below, classify if it 'confirmed', 'contradicted', or is 'unclear' in relation to this theme.\n"
            'Respond ONLY with a JSON object of the exact shape {"validations": [{"sample_review_id": int, '
            '"llm_validation_status": str}, ...]}.\n\n'
            f"Reviews:\n{reviews_text}"
        )

        validations = None
        for attempt in range(5):
            try:
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                validations = json.loads(response.choices[0].message.content).get("validations", [])
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

        if validations is None:
            print("Failed 5 times. Falling back to empty validation set — not silently mocked.")
            validations = []
        
        session.query(ValidationSample).delete() # clear old for idempotency
        
        inserted = 0
        for v in validations:
            sample = ValidationSample(
                theme_id=top_theme.id,
                sample_review_id=v.get('sample_review_id'),
                llm_validation_status=v.get('llm_validation_status', 'unclear')[:50],
                human_validation_status='pending'
            )
            session.add(sample)
            inserted += 1
            
        session.commit()
        print(f"Successfully ran LLM validation on {inserted} reviews for theme '{top_theme.theme_name}'.")

    except Exception as e:
        session.rollback()
        print(f"Error during validation: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    validate_themes()
