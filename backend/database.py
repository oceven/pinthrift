from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    platform = Column(String)
    link = Column(String)
    image_url = Column(String)
    embedding = Column(ARRAY(Float))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()