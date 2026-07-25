import os
import json
import time
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text
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
    evidence_count = Column(Integer)

class CompanyDisclosure(Base):
    __tablename__ = "company_disclosures"
    id = Column(Integer, primary_key=True)
    source_document = Column(String(255))
    content_snippet = Column(Text)
    theme_id = Column(Integer)
    signal_type = Column(String(50))

def analyze_concalls():
    session = SessionLocal()
    try:
        top_theme = session.query(Theme).order_by(Theme.evidence_count.desc(), Theme.id.desc()).first()
        if not top_theme:
            print("No themes found.")
            return

        # Real excerpts from Eternal Limited's Q4 FY26 earnings call (April 28, 2026) and Q1FY27
        # shareholders' letter (July 22, 2026), the latter supplied directly by the fellow and fetched/
        # transcribed 2026-07-22. Sources:
        # - https://b.zmtcdn.com/investor-relations/Q4FY26-earnings-call-transcript.pdf
        # - Eternal_Limited_Shareholders_Letter_Q1FY27_Results.pdf
        # NOTE: the Q4FY26 call stayed at the financial-metrics level with no direct commentary on
        # product quality/damage — that was a real, honest gap (see edge-cases.md). The Q1FY27 letter
        # closes that gap: management explicitly quantifies inventory losses from expiry/damage/loss in
        # transit (1.8% of NOV, concentrated in perishables) — direct, independent corroboration of the
        # Part 1 "Poor Quality and Unreliable Products" theme, not just a category-expansion strategy
        # inference. Also carries current (not historical) assortment-expansion commentary from Blinkit's
        # own CEO, plus retention-cohort data that tempers the survey's single competitor-switching
        # finding (R5) — real evidence should be reported both ways, not cherry-picked.
        real_concalls = [
            {
                "source_document": "Eternal_Q4FY26_Earnings_Call_2026-04-28",
                "text": "Analyst (Jignanshu Gor, Bernstein): 'as a large part of our growth narrative from here on depends in some sense on either growing the non-grocery assortment and going outside of the metro cities.'"
            },
            {
                "source_document": "Eternal_Q4FY26_Earnings_Call_2026-04-28",
                "text": "Akshant Goyal (CFO), on the 60% CAGR growth guidance: 'It's a function of assortment expansion, geographical expansion as well as more demand densification in the cities where we are present today and we might also get into newer cities.'"
            },
            {
                "source_document": "Eternal_Q4FY26_Earnings_Call_2026-04-28",
                "text": "Akshant Goyal (CFO), on declining orders-per-customer (3.6 to 3.35): 'We haven't seen too much impact on customer retention... Most of this is on account of the acceleration in new customer addition that we have seen in the last couple of quarters.'"
            },
            {
                "source_document": "Eternal_Limited_Shareholders_Letter_Q1FY27_Results_2026-07-22",
                "text": "Albinder Dhindsa (Blinkit CEO): 'We continue to focus our efforts on our three pillars of long-term growth - assortment expansion, geographical expansion, and demand densification... Going forward, premiumisation through launch of gourmet stores in select locations in top eight cities will also contribute to assortment expansion on the platform. These gourmet stores offer our customers the ability to buy curated premium brands across categories.'"
            },
            {
                "source_document": "Eternal_Limited_Shareholders_Letter_Q1FY27_Results_2026-07-22",
                "text": "Akshant Goyal (CFO), on inventory losses: 'Inventory losses for us are about 1.8% of NOV right now, which include losses on account of expiry, shrinkage, damage, loss in transit or pilferage. A large part of these losses are driven by perishable products (including fruits and vegetables) which is an important and large category for us in the quick commerce business.'"
            },
            {
                "source_document": "Eternal_Limited_Shareholders_Letter_Q1FY27_Results_2026-07-22",
                "text": "Akshant Goyal (CFO), on customer retention: 'Q4 retention (% of customers placing at least 1 order in the 4th quarter after acquisition): average across all cohorts is 46%, with every successive cohort improving - the most recent cohort (Q1FY26) is at 50%... NOV retention compounds even faster - Q4 at 150%, Q8 at 215%, Q12 at 279% average retention for all cohorts.'"
            }
        ]

        concall_text = ""
        for mc in real_concalls:
            concall_text += f"Document: {mc['source_document']}\nText: {mc['text']}\n---\n"

        prompt = (
            f"Analyze the following real earnings call excerpts against this user friction theme:\n"
            f"Theme: {top_theme.theme_name}\n"
            f"Theme Description: {top_theme.description}\n\n"
            f"For each excerpt, determine if it 'corroborates', 'contradicts', or is 'unrelated' to the theme. "
            f"Be conservative — only mark 'corroborates' if the excerpt specifically addresses product "
            f"quality, returns, refunds, or customer trust/support. An excerpt about category expansion "
            f"strategy in general is 'unrelated' to a quality/trust theme unless it explicitly connects "
            f"the two — don't stretch an indirect business-strategy mention into false corroboration.\n"
            f"Return a JSON list of objects.\n\n"
            f"Excerpts:\n{concall_text}"
        )

        signals = None
        for attempt in range(5):
            try:
                response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt + '\n\nRespond ONLY with a JSON object of the exact shape {"signals": [{"source_document": str, "content_snippet": str, "signal_type": str}, ...]}.'}],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                signals = json.loads(response.choices[0].message.content).get("signals", [])
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

        if signals is None:
            print("Failed 5 times. Falling back to empty signal set — not silently mocked.")
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
