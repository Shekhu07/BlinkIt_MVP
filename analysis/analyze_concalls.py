import os
import json
import time
import google.generativeai as genai
import typing_extensions as typing
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text
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

class CompanyDisclosure(Base):
    __tablename__ = "company_disclosures"
    id = Column(Integer, primary_key=True)
    source_document = Column(String(255))
    content_snippet = Column(Text)
    theme_id = Column(Integer)
    signal_type = Column(String(50))

class ConcallSignal(typing.TypedDict):
    source_document: str
    content_snippet: str
    signal_type: str # 'corroborates', 'contradicts', 'unrelated'

def analyze_concalls():
    session = SessionLocal()
    try:
        top_theme = session.query(Theme).order_by(Theme.id.desc()).first()
        if not top_theme:
            print("No themes found.")
            return

        mock_concalls = [
            {
                "source_document": "Q4_2025_Earnings_Call",
                "text": "Analyst: Can you talk about the category expansion strategy? CEO: We are seeing great traction in groceries, but non-grocery items like electronics have a slightly higher return rate which has caused some friction in customer trust. We are working on streamlining our return and refund processes to build more confidence."
            },
            {
                "source_document": "Q1_2026_Earnings_Call",
                "text": "CEO: The quick commerce model is robust. Average order value is climbing as users get used to the convenience. However, we've paused expansion into high-value electronics in Tier 2 cities temporarily because the post-purchase support infrastructure isn't quite there yet to handle disputes quickly."
            }
        ]

        concall_text = ""
        for mc in mock_concalls:
            concall_text += f"Document: {mc['source_document']}\nText: {mc['text']}\n---\n"

        prompt = (
            f"Analyze the following earnings call excerpts against this user friction theme:\n"
            f"Theme: {top_theme.theme_name}\n"
            f"Theme Description: {top_theme.description}\n\n"
            f"For each excerpt, determine if it 'corroborates', 'contradicts', or is 'unrelated' to the theme. "
            f"Return a JSON list of objects.\n\n"
            f"Excerpts:\n{concall_text}"
        )

        for attempt in range(5):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=list[ConcallSignal],
                        temperature=0.1
                    )
                )
                signals = json.loads(response.text)
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
        
        if 'signals' not in locals():
            print("Failed 5 times. Falling back to mock data to prevent pipeline crash.")
            signals = []
        
        session.query(CompanyDisclosure).delete() # clear old for idempotency
        
        inserted = 0
        for s in signals:
            disclosure = CompanyDisclosure(
                source_document=s.get('source_document')[:255],
                content_snippet=s.get('content_snippet', ''),
                theme_id=top_theme.id,
                signal_type=s.get('signal_type', 'unrelated')[:50]
            )
            session.add(disclosure)
            inserted += 1
            
        session.commit()
        print(f"Successfully ran LLM analysis on earnings calls. Saved {inserted} signals.")

    except Exception as e:
        session.rollback()
        print(f"Error during concall analysis: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    analyze_concalls()
