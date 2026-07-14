"""
Scraper for Trustpilot Blinkit reviews.
Uses the __NEXT_DATA__ JSON blob embedded in Trustpilot pages for stable extraction.
"""
import os
import json
import time
import hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def scrape_trustpilot(max_pages=10):
    """
    Scrape Blinkit reviews from Trustpilot.
    Trustpilot embeds review data in a __NEXT_DATA__ script tag as JSON.
    """
    base_url = "https://www.trustpilot.com/review/blinkit.com"
    all_reviews = []

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        print(f"  Trustpilot page {page}: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 403:
                print(f"    HTTP 403 Forbidden — Trustpilot is blocking. Stopping.")
                break
            if response.status_code != 200:
                print(f"    HTTP {response.status_code}, stopping.")
                break

            soup = BeautifulSoup(response.text, "html.parser")

            # Method 1: Try __NEXT_DATA__ JSON extraction (most reliable)
            next_data = soup.find("script", {"id": "__NEXT_DATA__"})
            if next_data:
                try:
                    data = json.loads(next_data.string)
                    # Navigate the JSON structure to find reviews
                    page_props = data.get("props", {}).get("pageProps", {})
                    reviews_data = page_props.get("reviews", [])

                    if not reviews_data:
                        print(f"    No reviews in __NEXT_DATA__, stopping.")
                        break

                    for review in reviews_data:
                        title = review.get("title", "")
                        text = review.get("text", "")
                        rating = review.get("rating", 0)
                        review_id = review.get("id", "")
                        date_str = review.get("dates", {}).get("publishedDate", "")

                        content = f"{title}. {text}" if title else text
                        if not content or len(content) < 5:
                            continue

                        created_at = None
                        if date_str:
                            try:
                                created_at = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                            except:
                                created_at = datetime.utcnow()

                        source_id = f"trustpilot_{review_id}" if review_id else f"trustpilot_{hashlib.md5(content[:100].encode()).hexdigest()}"

                        all_reviews.append({
                            "source": "trustpilot",
                            "source_id": source_id,
                            "content": content,
                            "rating": rating,
                            "created_at": created_at or datetime.utcnow()
                        })

                    print(f"    Found {len(reviews_data)} reviews via __NEXT_DATA__.")
                except json.JSONDecodeError:
                    print(f"    Failed to parse __NEXT_DATA__ JSON.")
            else:
                # Method 2: Fallback to HTML parsing
                review_cards = soup.find_all("article", {"class": lambda x: x and "paper_paper" in str(x)})
                if not review_cards:
                    review_cards = soup.find_all("div", {"data-review-count": True})

                if not review_cards:
                    print(f"    No reviews found via HTML parsing either, stopping.")
                    break

                for card in review_cards:
                    title_el = card.find("h2")
                    text_el = card.find("p", {"class": lambda x: x and "typography" in str(x)})

                    title = title_el.get_text(strip=True) if title_el else ""
                    text = text_el.get_text(strip=True) if text_el else ""
                    content = f"{title}. {text}" if title else text

                    if not content or len(content) < 5:
                        continue

                    # Try to get rating from star image
                    rating = 0
                    star_el = card.find("img", {"alt": lambda x: x and "star" in str(x).lower()})
                    if star_el:
                        alt = star_el.get("alt", "")
                        for i in range(5, 0, -1):
                            if str(i) in alt:
                                rating = i
                                break

                    source_id = f"trustpilot_{hashlib.md5(content[:100].encode()).hexdigest()}"
                    all_reviews.append({
                        "source": "trustpilot",
                        "source_id": source_id,
                        "content": content,
                        "rating": rating,
                        "created_at": datetime.utcnow()
                    })

                print(f"    Found {len(review_cards)} reviews via HTML fallback.")

            time.sleep(3)  # Trustpilot is strict about rate limiting

        except Exception as e:
            print(f"    Error on page {page}: {e}")
            break

    print(f"Total Trustpilot reviews scraped: {len(all_reviews)}")
    return all_reviews


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
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            result = session.execute(stmt)
            if result.rowcount > 0:
                inserted_count += 1
        session.commit()
        print(f"Successfully inserted {inserted_count} new Trustpilot reviews into the database.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    reviews = scrape_trustpilot(max_pages=10)
    if reviews:
        save_reviews_to_db(reviews)
    else:
        print("No reviews scraped from Trustpilot.")
    print("Trustpilot ingestion complete!")
