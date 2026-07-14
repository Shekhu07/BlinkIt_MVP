import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://blinkit_user:blinkit_password@localhost:5432/blinkit_discovery")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RawReview(Base):
    __tablename__ = "raw_reviews"
    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    content = Column(Text)
    rating = Column(Integer)

class FilteredReview(Base):
    __tablename__ = "filtered_reviews"
    id = Column(Integer, primary_key=True)
    raw_review_id = Column(Integer)
    filtered_content = Column(Text)
    tf_idf_score = Column(Float, default=1.0)
    is_relevant = Column(Boolean, default=True)

def prefilter_reviews():
    session = SessionLocal()
    try:
        # Fetch all raw reviews
        raw_reviews = session.query(RawReview).all()
        print(f"Found {len(raw_reviews)} raw reviews.")
        
        filtered_count = 0
        for review in raw_reviews:
            content = review.content
            if not content:
                continue
                
            words = content.split()
            # Heuristic 1: Skip very short reviews (e.g. "nice app", "good")
            if len(words) < 5 and review.source != "reddit":
                continue
                
            # Heuristic 2: Skip purely positive reviews (rating 5) unless it's reddit
            if review.rating == 5 and review.source != "reddit":
                continue
                
            # Check if it already exists to avoid duplicates during dev
            exists = session.query(FilteredReview).filter_by(raw_review_id=review.id).first()
            if not exists:
                filtered_review = FilteredReview(
                    raw_review_id=review.id,
                    filtered_content=content,
                    is_relevant=True
                )
                session.add(filtered_review)
                filtered_count += 1
                
        session.commit()
        print(f"Successfully pre-filtered and saved {filtered_count} high-signal reviews for LLM extraction.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    prefilter_reviews()
