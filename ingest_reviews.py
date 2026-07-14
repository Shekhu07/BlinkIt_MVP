import os
import json
import time
import requests as http_requests
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from google_play_scraper import reviews, Sort

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

def fetch_play_store_reviews(app_id="com.grofers.customerapp", count=5000):
    """Fetch Play Store reviews using google-play-scraper. Increased to 5000."""
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

def fetch_app_store_reviews_rss(app_id="1001550974", country="in", max_pages=10):
    """
    Fetch App Store reviews using Apple's official iTunes RSS feed.
    This is reliable and doesn't get blocked unlike the app-store-scraper library.
    Each page returns up to 50 reviews, max 10 pages = 500 reviews.
    """
    print(f"Fetching App Store reviews via iTunes RSS feed for app {app_id}...")
    parsed_reviews = []
    
    for page in range(1, max_pages + 1):
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/page={page}/json"
        
        try:
            response = http_requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }, timeout=15)
            
            if response.status_code != 200:
                print(f"  Page {page}: HTTP {response.status_code}, stopping.")
                break
                
            data = response.json()
            feed = data.get("feed", {})
            entries = feed.get("entry", [])
            
            if not entries:
                print(f"  Page {page}: No entries found, stopping.")
                break
            
            # The first entry is often the app metadata, skip it
            review_entries = []
            for entry in entries:
                # Real reviews have an 'im:rating' field; the app metadata entry does not
                if "im:rating" in entry:
                    review_entries.append(entry)
            
            for entry in review_entries:
                review_id = entry.get("id", {}).get("label", "")
                title = entry.get("title", {}).get("label", "")
                content = entry.get("content", {}).get("label", "")
                rating = int(entry.get("im:rating", {}).get("label", "0"))
                author = entry.get("author", {}).get("name", {}).get("label", "")
                updated = entry.get("updated", {}).get("label", "")
                
                # Combine title and content for richer text
                full_content = f"{title}. {content}" if title else content
                
                # Parse the date
                created_at = None
                if updated:
                    try:
                        created_at = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    except:
                        created_at = datetime.utcnow()
                
                parsed_reviews.append({
                    "source": "app_store",
                    "source_id": f"app_{review_id}" if review_id else f"app_{hash(full_content)}",
                    "content": full_content,
                    "rating": rating,
                    "created_at": created_at
                })
            
            print(f"  Page {page}: Fetched {len(review_entries)} reviews.")
            time.sleep(1)  # Be respectful to Apple's servers
            
        except Exception as e:
            print(f"  Page {page}: Error - {e}")
            break
    
    print(f"Total App Store reviews fetched: {len(parsed_reviews)}")
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
    
    play_reviews = fetch_play_store_reviews(app_id=play_store_id, count=5000)
    app_reviews = fetch_app_store_reviews_rss(app_id=app_store_id)
    
    all_reviews = play_reviews + app_reviews
    save_reviews_to_db(all_reviews)
    print(f"\nIngestion complete! Total reviews processed: {len(all_reviews)}")
