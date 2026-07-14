import os
import json
import time
import google.generativeai as genai
import typing_extensions as typing
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert

load_dotenv()

# Setup Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    print("ERROR: GEMINI_API_KEY is not set correctly in .env file.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
# Use Gemini 1.5 Flash for high throughput
model = genai.GenerativeModel('gemini-flash-latest')

# DB Setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FilteredReview(Base):
    __tablename__ = "filtered_reviews"
    id = Column(Integer, primary_key=True)
    raw_review_id = Column(Integer)
    filtered_content = Column(Text)

class Extraction(Base):
    __tablename__ = "extractions"
    id = Column(Integer, primary_key=True)
    filtered_review_id = Column(Integer)
    behavior_type = Column(String(100))
    category = Column(String(100))
    reason = Column(Text)
    confidence = Column(Float)

class SingleExtraction(typing.TypedDict):
    filtered_review_id: int
    behavior_type: str
    category: str
    reason: str
    confidence: float

def extract_insights():
    print("Connecting to DB...")
    session = SessionLocal()
    print("Session created.")
    try:
        while True:
            print("Querying extracted_ids...")
            extracted_ids = [e.filtered_review_id for e in session.query(Extraction.filtered_review_id).all()]
            print(f"Found {len(extracted_ids)} extracted_ids.")
            print("Querying reviews_to_process...")
            reviews_to_process = session.query(FilteredReview).filter(~FilteredReview.id.in_(extracted_ids)).limit(50).all()
            
            if not reviews_to_process:
                print("No new reviews to process. Done!")
                break

            print(f"Found {len(reviews_to_process)} reviews to extract from. Sending to Gemini...")
            
            batch_text = "Here are the reviews to analyze:\n\n"
            for r in reviews_to_process:
                batch_text += f"Review ID: {r.id}\nContent: {r.filtered_content}\n---\n"
                
            prompt = (
                "You are a Product Manager at Blinkit analyzing user reviews. "
                "For each review provided, extract any friction or reason why a user might not adopt "
                "new categories (like electronics, personal care, etc) or why they have a bad experience. "
                "If a review doesn't contain a clear reason or friction, ignore it. "
                "Return a JSON array of extractions, maintaining the Review ID provided."
            )

            for attempt in range(5):
                try:
                    response = model.generate_content(
                        f"{prompt}\n\n{batch_text}",
                        generation_config=genai.GenerationConfig(
                            response_mime_type="application/json",
                            response_schema=list[SingleExtraction],
                            temperature=0.1
                        )
                    )
                    break
                except Exception as e:
                    import time
                    if "429" in str(e) or "quota" in str(e).lower():
                        print(f"Rate limited (attempt {attempt+1}/5). Waiting 35 seconds...")
                        time.sleep(35)
                    else:
                        raise e
            
            extractions_data = json.loads(response.text)
            print(f"Gemini extracted {len(extractions_data)} insights!")
            
            inserted = 0
            for data in extractions_data:
                ext = Extraction(
                    filtered_review_id=data.get('filtered_review_id'),
                    behavior_type=data.get('behavior_type', 'unknown')[:100],
                    category=data.get('category', 'unknown')[:100],
                    reason=data.get('reason', ''),
                    confidence=float(data.get('confidence', 0.8))
                )
                session.add(ext)
                inserted += 1
                
            session.commit()
            print(f"Saved {inserted} extractions to the database.")

    except Exception as e:
        session.rollback()
        print(f"Error during extraction: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    extract_insights()
