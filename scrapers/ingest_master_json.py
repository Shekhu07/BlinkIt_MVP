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

def parse_rating(rating_str):
    try:
        return int(float(rating_str))
    except:
        return 0

def ingest_master_json():
    session = SessionLocal()
    try:
        json_path = os.path.join(os.path.dirname(__file__), '../data/MASTER_Blinkit_Reviews.json')
        print(f"Loading {json_path}...")
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        print(f"Found {len(data)} reviews in JSON. Starting ingestion...")
        inserted_count = 0
        batch_size = 500
        batch_data = []

        for i, review in enumerate(data):
            source_raw = review.get('source') or 'unknown'
            # normalize source string
            if "google play store" in source_raw.lower():
                source = "play_store"
            elif "google maps" in source_raw.lower():
                source = "google_maps"
            elif "app store" in source_raw.lower():
                source = "app_store"
            elif "consumercomplaints" in source_raw.lower():
                source = "consumer_complaints"
            else:
                source = "unknown_master"

            title = review.get('title', '')
            text = review.get('content', '')
            content = f"{title}. {text}" if title else text
            
            # Ensure content is a string
            if content is None:
                content = ""
            
            rating = parse_rating(review.get('rating'))
            
            # Date can be complex "Jul 15, 2026", just using current time for simplicity or trying to parse
            created_at = datetime.utcnow()
            
            # Generate unique source_id to prevent duplicates
            hash_str = f"{source}_{review.get('author', 'user')}_{content[:100]}"
            source_id = f"master_{hashlib.md5(hash_str.encode('utf-8', errors='ignore')).hexdigest()}"
            
            # Truncate strings just in case
            stmt = insert(RawReview).values(
                source=source[:50],
                source_id=source_id[:255],
                content=content,
                rating=rating,
                created_at=created_at
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            
            result = session.execute(stmt)
            if result.rowcount > 0:
                inserted_count += 1
            
            if (i + 1) % batch_size == 0:
                session.commit()
                print(f"  Processed {i + 1}/{len(data)} reviews... (Inserted: {inserted_count})")
                
        session.commit()
        print(f"\nDone! Successfully inserted {inserted_count} new reviews from MASTER file.")
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    ingest_master_json()
