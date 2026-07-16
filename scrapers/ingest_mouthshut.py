"""
Ingest MouthShut reviews that were scraped via browser automation.
Since MouthShut renders reviews via JavaScript, we extracted them manually
and now inject them into the database.
"""
import os
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

# Reviews scraped from MouthShut.com via browser automation
MOUTHSHUT_REVIEWS = [
    {"title": "No return or refund policy", "content": "Don't buy anything from blinkit. They will not return your money nor replacement. I ordered a hair dryer, got a used and dirty one. When I raised request for replacement, they decline my request. Customer support is worst. They don't listen to you. Fraud application.", "rating": 1},
    {"title": "Horrible - will never use blinkit", "content": "Horrible - will never use blinkit - they do not refund if they deliver bad/wrong products - customer support is non existent. We ordered whole wheat pav and got normal pav - they did not return or replace.", "rating": 1},
    {"title": "GREAT SERVICE", "content": "Excellent app. I got my delivery within 10 mins. Very fast service. Highly recommended.", "rating": 5},
    {"title": "Having a great experience", "content": "I am using this app since 6 months. It is very fast and reliable. I get all my groceries within 10-15 mins. The quality of products is also very good.", "rating": 5},
    {"title": "Highly unsatisfactory replies for duplicate product", "content": "Highly unsatisfactory replies for duplicate product received. The customer support is worst. They don't help you at all. Don't buy from them.", "rating": 1},
    {"title": "Poor reliability", "content": "Please check weight of your orders. I order 1 kg onion and get only 300gms. and tomato 900 gm instead of 1 kg.", "rating": 1},
    {"title": "Timely Delivery but insecure Pack", "content": "Delivers on time but the packaging is not. Torn Packets, in fact ice cream always comes melted, no proper delivery bags provided to the delivery person for Ice creams and Kulfi.", "rating": 4},
    {"title": "Well enough but more to be added", "content": "The products are timely delivered with good quality and wrong ones are replaced asap. But I wanna request to add medicines also as no such app offers free delivery of medicines even after a total cost of Rs. 500.", "rating": 4},
    {"title": "Sanyam customer service", "content": "Driver refused to deliver, marked as delivered and Sanyam service agent was extremely unhelpful. Awful service.", "rating": 1},
    {"title": "Fault Item from Blinkit", "content": "I purchased an Omron HEM-7090-L blood pressure monitor from Blinkit. Unfortunately, I found the cuff design to be uncomfortable and difficult to use correctly. I contacted Blinkit within 72 hours of receiving the product and explained that the monitor was not suitable for me because of the cuff design. However, I was informed that the item was replacement-only and my request for a return was declined. I also requested a one-time exception, but this was not considered. I hope Blinkit considers handling such situations with greater customer empathy in the future, especially when the request is made promptly after delivery.", "rating": 1},
    {"title": "Worst customer support", "content": "Neither received the ordered items nor the refund. They only resolve issues within a 24-hour window, what if the person who ordered is not available to reconfirm the order and another person receives it? At least they should be honest if the ordered product is not available they should raise the refund but they wait for the complaint to be registered.", "rating": 1},
    {"title": "Refund Promo instead of refund - Absolute cheating", "content": "We have received the broken package. Instead of crediting the refund in source account, they have given the refund promo which we need to use for future purchase. It is their fault and not customers. Even handling charge they should refund. Their support executive Abhijeet was very rude. Also delivery charges, small cart charges, handling charges, surge chg are different source of their income.", "rating": 1},
    {"title": "Worst Customer Service & Replacement Experience", "content": "I had a very disappointing experience with Blinkit. The product I received was defective, and even though I reported the issue within the eligible replacement period, my replacement request was not handled properly. Instead of resolving the issue, I was asked to contact the brand directly. Customer support kept giving repetitive responses without providing a real solution. Customers buy from Blinkit, so they naturally expect Blinkit to handle such issues.", "rating": 1},
    {"title": "Disappointed", "content": "They judge you for last cancelled orders and don't want customer to reorder. They remove the option for cash on delivery which was always easy for us to pay.", "rating": 1},
    {"title": "Delivered expired product", "content": "Had a very bad experience. I ordered a sun cream and they delivered one which was already expired. I requested a replacement and they delivered the same expired product again. I tried to contact customer care but they didn't give any option to address the issue.", "rating": 1},
    {"title": "Non friendly customer service, no trust", "content": "Blinkit has been on my radar for a while now. Tried them today for a change for veggies. Apples were rotten from inside, cauliflower was brown n stems broken, peeled small onions were the size of regular medium sized onions. When I wrote to them with photos they just said we cannot do anything about it as they cannot see the issues on the photos. Swiggy does all this over the chat inside the app and mostly gives refunds, as they trust their customers.", "rating": 1},
    {"title": "Fraud", "content": "Blinkit delivered half of my ordered product and not even refunded my money back. This is very unjust and a case of fraudulent racket going on by the delivery guy and the company. Eating up customer's product and money both. I highly request everyone to stay alert and not order from blinkit anymore.", "rating": 1},
    {"title": "Item not return", "content": "I ordered raaga tan removal which cost 430/-. It showed a big box, but I got 30 sachets in a box. I called customer care to discuss this issue, and they said they are trying to solve it, but unfortunately it was not returned. In the Blinkit app, whenever we want to return an item, they don't accept returns on our orders. It's very unfair and cheating the customers.", "rating": 1},
    {"title": "Worst customer support", "content": "If you have any items missing or damaged, then forget about getting a replacement or refund. The customer support will just waste your time and ask you to come back tomorrow and keep doing this till the complaint window closes. They will just harass and make it impossible to get a resolution. We should stop buying from these platforms so that they run out of business!", "rating": 1},
    {"title": "Think twice before ordering again", "content": "Very disappointing experience. The product quality was far below expectations, and the size was much smaller than what was shown in the description. What is even more disappointing is the lack of a satisfactory resolution from customer support. I raised a genuine concern, but instead of receiving meaningful assistance, I was given a generic response. This has significantly reduced my confidence in the service and the accuracy of the product listings.", "rating": 1},
]


def inject_mouthshut_reviews():
    session = SessionLocal()
    try:
        inserted_count = 0
        for review in MOUTHSHUT_REVIEWS:
            content = f"{review['title']}. {review['content']}"
            source_id = f"mouthshut_{hashlib.md5(content[:100].encode()).hexdigest()}"

            stmt = insert(RawReview).values(
                source="mouthshut",
                source_id=source_id,
                content=content,
                rating=review["rating"],
                created_at=datetime.utcnow()
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
            result = session.execute(stmt)
            if result.rowcount > 0:
                inserted_count += 1

        session.commit()
        print(f"Successfully inserted {inserted_count} MouthShut reviews into the database.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    inject_mouthshut_reviews()
    print("MouthShut ingestion complete!")
