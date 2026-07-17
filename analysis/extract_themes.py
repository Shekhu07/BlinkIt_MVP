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
    mentions_category_behavior = Column(Boolean)
    behavior_type = Column(String(100))
    category = Column(String(100))
    reason = Column(Text)
    sentiment = Column(String(100))
    confidence = Column(Float)

class SingleExtraction(typing.TypedDict):
    filtered_review_id: int
    mentions_category_behavior: bool
    behavior_type: str
    category_mentioned: str
    underlying_reason: str
    sentiment: str
    confidence: float

def extract_insights():
    print("Connecting to DB...")
    session = SessionLocal()
    print("Session created.")
    try:
        batch_count = 0
        while True:
            if batch_count >= 3:
                print("Reached batch limit. Done for now.")
                break
            batch_count += 1
            print("Querying extracted_ids...")
            extracted_ids = [e.filtered_review_id for e in session.query(Extraction.filtered_review_id).all()]
            print(f"Found {len(extracted_ids)} extracted_ids.")
            print("Querying reviews_to_process...")
            reviews_to_process = session.query(FilteredReview).filter(~FilteredReview.id.in_(extracted_ids)).order_by(FilteredReview.id.desc()).limit(50).all()
            
            if not reviews_to_process:
                print("No new reviews to process. Done!")
                break

            print(f"Found {len(reviews_to_process)} reviews to extract from. Sending to Gemini...")
            
            batch_text = "Here are the reviews to analyze:\n\n"
            for r in reviews_to_process:
                batch_text += f"Review ID: {r.id}\nContent: {r.filtered_content}\n---\n"
                
            prompt = (
                "You are an AI extracting specific user behavior from reviews. "
                "Step 1 - Relevance Gate: Check if the text relates to: why a user keeps buying the same category, "
                "why a user has not tried an unfamiliar category, how users discover new products/categories, "
                "a specific moment of considering/trying/rejecting a category, trust or risk about trying something unfamiliar, "
                "or habitual/repeat-purchase patterns. If it is primarily about refunds, support, delivery timing/conduct, "
                "pricing, payments, or general app bugs with no explicit tie to category trial/avoidance, set mentions_category_behavior to false.\n"
                "Step 2 - Extraction: If mentions_category_behavior is true, fill in behavior_type (repeat_purchase | category_avoidance | discovery_friction | new_category_trial), "
                "category_mentioned (groceries | personal_care | pet_supplies | baby_products | electronics | household_essentials | snacks_beverages | other | unspecified), "
                "underlying_reason (one sentence, paraphrased), and sentiment (frustration | neutral_observation | satisfaction | curiosity). "
                "If mentions_category_behavior is false, leave other fields blank or default. "
                "Maintain the Review ID provided."
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
                    extractions_data = json.loads(response.text)
                    break
                except Exception as e:
                    import time
                    if "429" in str(e) or "quota" in str(e).lower():
                        print(f"Rate limited (attempt {attempt+1}/5). Waiting 35 seconds...")
                        time.sleep(35)
                    elif isinstance(e, json.JSONDecodeError):
                        print(f"Bad JSON (attempt {attempt+1}/5). Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        raise e
            
            print(f"Gemini processed {len(extractions_data)} reviews in batch!")
            
            inserted = 0
            rejected = 0
            for data in extractions_data:
                # We save all of them so we don't process them again, but we track the gate
                mentions = data.get('mentions_category_behavior', False)
                if not mentions:
                    rejected += 1
                
                ext = Extraction(
                    filtered_review_id=data.get('filtered_review_id'),
                    mentions_category_behavior=mentions,
                    behavior_type=data.get('behavior_type', 'unknown')[:100],
                    category=data.get('category_mentioned', 'unknown')[:100],
                    reason=data.get('underlying_reason', ''),
                    sentiment=data.get('sentiment', 'unknown')[:100],
                    confidence=float(data.get('confidence', 0.8))
                )
                session.add(ext)
                if mentions:
                    inserted += 1
                
            session.commit()
            print(f"Batch complete. Valid signal extracted: {inserted}. Rejected as noise: {rejected}.")

    except Exception as e:
        session.rollback()
        print(f"Error during extraction: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    extract_insights()
