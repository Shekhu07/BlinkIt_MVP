import os
import json
import google.generativeai as genai
import typing_extensions as typing
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class MacroTheme(typing.TypedDict):
    theme_name: str
    description: str
    user_segment: str
    evidence_count: int

def run_fast_extract():
    session = SessionLocal()
    try:
        # Get 30 recent App Store reviews
        res = session.execute(text("SELECT content FROM raw_reviews WHERE source = 'app_store' ORDER BY id DESC LIMIT 30"))
        reviews = [row[0] for row in res]
        
        if not reviews:
            print("No reviews found.")
            return

        reviews_text = "\n".join([f"- {r}" for r in reviews])
        
        prompt = (
            "You are a Lead PM. I am giving you 30 specific user reviews (from MouthShut and ConsumerComplaints) "
            "about Blinkit. Your job is to extract and cluster the primary friction points into the Top 3 macro-themes "
            "explaining why users have bad experiences or don't adopt new categories.\n"
            "For each theme, provide:\n"
            "1. theme_name\n"
            "2. description\n"
            "3. user_segment\n"
            "4. evidence_count (estimated number of reviews matching this)\n\n"
            f"Here are the reviews:\n{reviews_text}"
        )

        import time
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
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"Rate limited (attempt {attempt+1}/5). Waiting 35 seconds...")
                    time.sleep(35)
                else:
                    raise e

        themes_data = json.loads(response.text)
        
        # Insert into themes table directly
        session.execute(text("DELETE FROM themes"))
        for t in themes_data:
            session.execute(
                text("INSERT INTO themes (theme_name, description, user_segment, evidence_count) VALUES (:tn, :d, :us, :ec)"),
                {"tn": t['theme_name'][:255], "d": t['description'], "us": t['user_segment'][:255], "ec": t['evidence_count']}
            )
        session.commit()
        print("Successfully generated and saved themes based on new data!")
        for t in themes_data:
            print(f"- {t['theme_name']}")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_fast_extract()
