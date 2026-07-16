"""
Scraper for ConsumerComplaints.in Blinkit complaints.
Uses the search endpoint to find Blinkit-related complaints.
"""
import os
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
}

def scrape_consumer_complaints(max_pages=50):
    """
    Scrape Blinkit complaints from ConsumerComplaints.in via search.
    Step 1: Get complaint listing from search results
    Step 2: Visit each complaint page for the full text
    """
    all_reviews = []
    complaint_links = []

    # Step 1: Get complaint links from search results
    for page in range(1, max_pages + 1):
        url = f"https://www.consumercomplaints.in/?search=blinkit&page={page}"
        print(f"  Search page {page}: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"    HTTP {response.status_code}, stopping.")
                break

            soup = BeautifulSoup(response.text, "html.parser")

            # Find complaint links — they typically have titles with "Blinkit"
            links_found = 0
            for a_tag in soup.find_all("a"):
                href = a_tag.get("href", "")
                text = a_tag.get_text(strip=True)
                # Complaint pages use /blinkit-*-c{id} pattern
                if href and "blinkit" in href.lower() and href.startswith("/blinkit") and text and len(text) > 10:
                    full_url = f"https://www.consumercomplaints.in{href}"
                    if full_url not in [l[0] for l in complaint_links]:
                        complaint_links.append((full_url, text))
                        links_found += 1

            print(f"    Found {links_found} complaint links.")
            if links_found == 0:
                break
            time.sleep(2)

        except Exception as e:
            print(f"    Error: {e}")
            break

    print(f"\nTotal unique complaint links found: {len(complaint_links)}")

    # Step 2: Visit each complaint page for the full text
    for i, (link, title) in enumerate(complaint_links):
        try:
            response = requests.get(link, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Try different selectors for complaint body
            body_text = ""
            for selector in [
                ("div", {"class": "complaint-body"}),
                ("div", {"class": "complaint_description"}),
                ("article", {}),
                ("div", {"class": "card-body"}),
            ]:
                el = soup.find(selector[0], selector[1])
                if el:
                    body_text = el.get_text(strip=True)
                    break

            # Fallback: grab all paragraph text from main content
            if not body_text:
                paragraphs = soup.find_all("p")
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 50 and ("blinkit" in text.lower() or "order" in text.lower() or "delivery" in text.lower()):
                        body_text += text + " "

            content = f"{title}. {body_text}" if body_text else title
            content = content[:2000]  # Cap length

            if content and len(content) > 20:
                source_id = f"cc_{hashlib.md5(content[:100].encode()).hexdigest()}"
                all_reviews.append({
                    "source": "consumer_complaints",
                    "source_id": source_id,
                    "content": content,
                    "rating": 1,  # All complaints = low rating
                    "created_at": datetime.utcnow()
                })

            if (i + 1) % 5 == 0:
                print(f"    Processed {i + 1}/{len(complaint_links)} complaints...")
            time.sleep(2)

        except Exception as e:
            print(f"    Error on complaint {i + 1}: {e}")
            continue

    print(f"Total ConsumerComplaints reviews scraped: {len(all_reviews)}")
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
        print(f"Successfully inserted {inserted_count} new ConsumerComplaints reviews.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    reviews = scrape_consumer_complaints(max_pages=50)
    if reviews:
        save_reviews_to_db(reviews)
    else:
        print("No reviews scraped from ConsumerComplaints.in.")
    print("ConsumerComplaints ingestion complete!")
