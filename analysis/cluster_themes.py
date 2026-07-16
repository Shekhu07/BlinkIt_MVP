import os
import json
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

class Extraction(Base):
    __tablename__ = "extractions"
    id = Column(Integer, primary_key=True)
    reason = Column(Text)

class Theme(Base):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    theme_name = Column(String(255))
    description = Column(Text)
    user_segment = Column(String(255))
    evidence_count = Column(Integer)

class MacroTheme(typing.TypedDict):
    theme_name: str
    description: str
    user_segment: str
    evidence_count: int

def cluster_themes():
    session = SessionLocal()
    try:
        # Grab all extracted reasons
        extractions = session.query(Extraction).all()
        if not extractions:
            print("No extractions found to cluster.")
            return

        reasons = [e.reason for e in extractions if e.reason]
        print(f"Found {len(reasons)} extracted reasons. Sending to Gemini for clustering...")

        reasons_text = "\n".join([f"- {r}" for r in reasons])
        prompt = (
            "You are a Lead Product Manager. I am giving you a list of specific reasons and frictions extracted "
            "from user reviews about Blinkit. Your job is to cluster these into the Top 3 to 5 macro-themes.\n"
            "For each theme, provide:\n"
            "1. A clear theme_name (e.g. 'Trust Deficit in Personal Care')\n"
            "2. A description of the problem\n"
            "3. The target user_segment (e.g. 'Grocery-only repeat buyers')\n"
            "4. An estimated evidence_count (how many of the bullet points seem to map to this theme)\n\n"
            f"Here are the reasons:\n{reasons_text}"
        )

        for attempt in range(5):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=list[MacroTheme],
                        temperature=0.2
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

        themes_data = json.loads(response.text)
        
        # Clear old themes for idempotency during dev
        session.query(Theme).delete()
        
        for t in themes_data:
            theme = Theme(
                theme_name=t.get('theme_name')[:255],
                description=t.get('description'),
                user_segment=t.get('user_segment')[:255],
                evidence_count=t.get('evidence_count', 0)
            )
            session.add(theme)
            
        session.commit()
        print(f"Successfully clustered and saved {len(themes_data)} macro-themes!")

    except Exception as e:
        session.rollback()
        print(f"Error during clustering: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    cluster_themes()
