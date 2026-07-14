"""
Playwright scraper for MouthShut.com Blinkit reviews.
Bypasses JS requirements by using a real browser engine to render the pages.
"""
import os
import time
import hashlib
from datetime import datetime
from playwright.sync_api import sync_playwright
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

def scrape_mouthshut_playwright(max_pages=20):
    all_reviews = []
    base_url = "https://www.mouthshut.com/product-reviews/blinkit-reviews-925738270"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()

        for page_num in range(1, max_pages + 1):
            url = base_url if page_num == 1 else f"{base_url}-page-{page_num}"
            print(f"Scraping MouthShut page {page_num}...")
            
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(3)  # Wait for reviews to load
                
                # Close any popups if they exist
                try:
                    page.locator("a.close").click(timeout=1000)
                except:
                    pass

                reviews_locators = page.locator("div.review-article, div.review, div.col-10").all()
                if not reviews_locators:
                    reviews_locators = page.locator("div[id^='review-']").all()

                found_on_page = 0
                for locator in reviews_locators:
                    try:
                        content = locator.inner_text().strip()
                        if len(content) < 20 or "blinkit" not in content.lower():
                            continue
                        
                        # Very basic rating extraction if available, defaults to 1 for complaints
                        rating = 1
                        if "Star" in content or "rating" in content.lower():
                            for i in range(5, 0, -1):
                                if f"{i} Star" in content or f"{i} star" in content.lower():
                                    rating = i
                                    break
                                    
                        # Clean content
                        lines = content.split('\n')
                        clean_content = " ".join([l.strip() for l in lines if l.strip() and not l.strip().startswith('Vote') and not l.strip().startswith('Reply')])
                        clean_content = clean_content[:2000] # Cap length
                        
                        source_id = f"mouthshut_{hashlib.md5(clean_content[:100].encode()).hexdigest()}"
                        
                        # Deduplicate in current list
                        if not any(r['source_id'] == source_id for r in all_reviews):
                            all_reviews.append({
                                "source": "mouthshut",
                                "source_id": source_id,
                                "content": clean_content,
                                "rating": rating,
                                "created_at": datetime.utcnow()
                            })
                            found_on_page += 1
                    except Exception as inner_e:
                        continue
                        
                print(f"  Found {found_on_page} reviews on page {page_num}")
                if found_on_page == 0:
                    print("  No reviews found, stopping pagination.")
                    break
                    
            except Exception as e:
                print(f"  Error on page {page_num}: {e}")
                break

        browser.close()
        
    print(f"Total MouthShut reviews scraped via Playwright: {len(all_reviews)}")
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
        print(f"Successfully inserted {inserted_count} new MouthShut reviews.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    reviews = scrape_mouthshut_playwright(max_pages=20)
    if reviews:
        save_reviews_to_db(reviews)
