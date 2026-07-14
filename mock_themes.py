import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

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

def inject_mock_themes():
    session = SessionLocal()
    try:
        session.query(Theme).delete()
        themes = [
            Theme(
                theme_name="Trust Deficit in High-Value/Fresh Categories",
                description="Users hesitate to buy electronics, personal care, or fresh meat/dairy on Blinkit because they fear receiving expired, damaged, or counterfeit goods. They prefer established niche platforms (like Licious or Amazon) for these items due to better return policies and perceived authenticity.",
                user_segment="High-Income Millennials & Gen Z (Core Quick Commerce Users)",
                evidence_count=87
            ),
            Theme(
                theme_name="Premium/Handling Fees on Small Baskets",
                description="Users strongly object to high cumulative fees (delivery + handling + small cart fee). For non-grocery items, this removes the convenience premium, causing them to abandon carts or just walk to a local store.",
                user_segment="Price-Sensitive Students & Young Professionals",
                evidence_count=52
            ),
            Theme(
                theme_name="Poor Customer Support for Electronics/Apparel",
                description="Unlike standard grocery replacements which are quick, users report that returning electronics or apparel is extremely difficult. The lack of a clear return policy for high-ticket items prevents category adoption.",
                user_segment="Urban Families & Professionals",
                evidence_count=39
            )
        ]
        session.add_all(themes)
        session.commit()
        print("Successfully injected 3 macro-themes into the database!")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    inject_mock_themes()
