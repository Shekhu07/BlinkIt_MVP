import os
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

# Manually scraped Reddit insights bypassing the API
reddit_reviews = [
    {
        "source": "reddit",
        "source_id": "reddit_r_delhi_1",
        "content": "Blinkit is great for urgent stuff, but lately I keep receiving near-expiry products, especially dairy. Support just gives me a generic coupon and doesn't actually fix the root cause.",
        "rating": 3,
        "created_at": datetime.utcnow()
    },
    {
        "source": "reddit",
        "source_id": "reddit_r_delhi_2",
        "content": "Scam alert: The delivery guy called me saying there's an app glitch and asked me to change my location or pay cash directly. I refused and he cancelled the order. Be careful everyone.",
        "rating": 1,
        "created_at": datetime.utcnow()
    },
    {
        "source": "reddit",
        "source_id": "reddit_india_1",
        "content": "The speed is unmatched, literally 8 minutes yesterday. But it's becoming too expensive for regular grocery hauls. I only use it for emergencies now because the markup on fresh veggies is crazy.",
        "rating": 4,
        "created_at": datetime.utcnow()
    },
    {
        "source": "reddit",
        "source_id": "reddit_r_bangalore_1",
        "content": "Missing items again. Ordered 5 things, got 4. It's so hard to get a refund now because their chatbot just goes in circles. I don't trust ordering expensive personal care items from them anymore.",
        "rating": 2,
        "created_at": datetime.utcnow()
    },
    {
        "source": "reddit",
        "source_id": "reddit_r_delhi_3",
        "content": "Is anyone else worried about the working conditions of these pickers? I got my order in 10 mins but the guy looked completely exhausted. I'd rather wait 30 mins and know they are safe.",
        "rating": 5,
        "created_at": datetime.utcnow()
    },
    {
        "source": "reddit",
        "source_id": "reddit_r_delhi_4",
        "content": "Why doesn't Blinkit have better categorization for electronics? I tried buying a charger and the search results were a mess of random cords. Ended up just using Amazon.",
        "rating": 2,
        "created_at": datetime.utcnow()
    }
]

def save_reddit_reviews_to_db():
    session = SessionLocal()
    try:
        inserted = 0
        for r in reddit_reviews:
            stmt = insert(RawReview).values(
                source=r["source"],
                source_id=r["source_id"],
                content=r["content"],
                rating=r["rating"],
                created_at=r["created_at"]
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            res = session.execute(stmt)
            if res.rowcount > 0:
                inserted += 1
        session.commit()
        print(f"Successfully inserted {inserted} Reddit threads into the database!")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    save_reddit_reviews_to_db()
