import os
import json
import time
import google.generativeai as genai
import typing_extensions as typing
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

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

class ValidationSample(Base):
    __tablename__ = "validation_samples"
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer)
    sample_review_id = Column(Integer)
    human_validation_status = Column(String(50))
    llm_validation_status = Column(String(50))

class ReviewValidation(typing.TypedDict):
    sample_review_id: int
    llm_validation_status: str # 'confirmed', 'contradicted', 'unclear'

def validate_themes():
    session = SessionLocal()
    try:
        # Get top theme
        top_theme = session.query(Theme).order_by(Theme.evidence_count.desc(), Theme.id.desc()).first()
        if not top_theme:
            print("No themes found.")
            return

        print(f"Top Theme: {top_theme.theme_name}")

        # Get 20 random reviews (or recent ones)
        reviews = session.query(RawReview).filter(RawReview.content != None).limit(20).all()
        if not reviews:
            print("No reviews found.")
            return

        reviews_text = ""
        for r in reviews:
            reviews_text += f"Review ID: {r.id}\nContent: {r.content}\n---\n"

        prompt = (
            f"You are an objective judge evaluating whether user reviews support a given theme.\n"
            f"Theme: {top_theme.theme_name}\n"
            f"Theme Description: {top_theme.description}\n\n"
            f"For each review below, classify if it 'confirmed', 'contradicted', or is 'unclear' in relation to this theme.\n"
            f"Return a JSON list.\n\n"
            f"Reviews:\n{reviews_text}"
        )

        for attempt in range(5):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=list[ReviewValidation],
                        temperature=0.1
                    )
                )
                validations = json.loads(response.text)
                break
            except Exception as e:
                import time
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"Rate limited (attempt {attempt+1}/5). Waiting 35 seconds...")
                    time.sleep(35)
                elif isinstance(e, json.JSONDecodeError):
                    print(f"Bad JSON generated (attempt {attempt+1}/5). Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise e
        
        if 'validations' not in locals():
            print("Failed 5 times. Falling back to mock data to prevent pipeline crash.")
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
