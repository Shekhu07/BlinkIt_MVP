import os
import json
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RawReview(Base):
    __tablename__ = "raw_reviews"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50))
    source_id = Column(String(255), unique=True)
    content = Column(Text)
    rating = Column(Integer)
    created_at = Column(DateTime)
    ingested_at = Column(DateTime, default=datetime.utcnow)

def ingest_json_reviews():
    session = SessionLocal()
    try:
        json_path = os.path.join(os.path.dirname(__file__), '../data/blinkit_reviews.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        inserted_count = 0
        for review in data:
            title = review.get('title', '')
            text = review.get('review', '')
            content = f"{title}. {text}" if title else text
            rating = review.get('rating', 0)
            
            date_str = review.get('date', '')
            created_at = datetime.utcnow()
            if date_str:
                try:
                    # Handles format like 2026-07-13T09:31:21-07:00
                    created_at = datetime.fromisoformat(date_str)
                except ValueError:
                    pass
            
            source_id = f"app_store_{review.get('userName', 'user')}_{hashlib.md5(content[:100].encode()).hexdigest()}"
            
            stmt = insert(RawReview).values(
                source="app_store",
                source_id=source_id,
                content=content,
                rating=rating,
                created_at=created_at.replace(tzinfo=None) # Strip tz for DB schema
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            result = session.execute(stmt)
            if result.rowcount > 0:
                inserted_count += 1
                
        session.commit()
        print(f"Successfully inserted {inserted_count} App Store reviews from JSON.")
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    ingest_json_reviews()
