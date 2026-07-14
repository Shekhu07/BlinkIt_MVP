import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from google_play_scraper import reviews, Sort
from app_store_scraper import AppStore

# Load environment variables
load_dotenv()

# Database setup
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

def fetch_play_store_reviews(app_id="com.grofers.customerapp", count=1000):
    print(f"Fetching up to {count} Play Store reviews for {app_id}...")
    result, continuation_token = reviews(
        app_id,
        lang='en', 
        country='in',
        sort=Sort.NEWEST,
        count=count
    )
    
    parsed_reviews = []
    for r in result:
        parsed_reviews.append({
            "source": "play_store",
            "source_id": f"play_{r['reviewId']}",
            "content": r['content'],
            "rating": r['score'],
            "created_at": r['at']
        })
    print(f"Fetched {len(parsed_reviews)} Play Store reviews.")
    return parsed_reviews

def fetch_app_store_reviews(app_name="blinkit", app_id="1001550974", count=1000):
    print(f"Fetching up to {count} App Store reviews for {app_name} ({app_id})...")
    app = AppStore(country='in', app_name=app_name, app_id=app_id)
    app.review(how_many=count)
    
    parsed_reviews = []
    for r in app.reviews:
        
        # Ensure we have a string source_id
        source_id = r.get('id')
        if not source_id:
            # Hash the review content + date if no ID
            content = r.get('review', '')
            date = str(r.get('date', ''))
            source_id = str(hash(content + date))

        parsed_reviews.append({
            "source": "app_store",
            "source_id": f"app_{source_id}",
            "content": r.get('review', ''),
            "rating": r.get('rating', 0),
            "created_at": r.get('date')
        })
    print(f"Fetched {len(parsed_reviews)} App Store reviews.")
    return parsed_reviews

def save_reviews_to_db(reviews_data):
    session = SessionLocal()
    try:
        inserted_count = 0
        for review_dict in reviews_data:
            stmt = insert(RawReview).values(
                source=review_dict["source"],
                source_id=review_dict["source_id"],
                content=review_dict["content"],
                rating=review_dict["rating"],
                created_at=review_dict["created_at"]
            )
            # On conflict (duplicate source_id), do nothing
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            result = session.execute(stmt)
            if result.rowcount > 0:
                inserted_count += 1
        session.commit()
        print(f"Successfully inserted {inserted_count} new reviews into the database.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    play_store_id = os.getenv("BLINKIT_PLAY_STORE_ID", "com.grofers.customerapp")
    app_store_id = os.getenv("BLINKIT_APP_STORE_ID", "1001550974")
    
    play_reviews = fetch_play_store_reviews(app_id=play_store_id, count=1000)
    app_reviews = fetch_app_store_reviews(app_id=app_store_id, count=1000)
    
    all_reviews = play_reviews + app_reviews
    save_reviews_to_db(all_reviews)
    print("Ingestion complete!")
