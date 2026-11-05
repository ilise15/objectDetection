import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Load the hidden URL from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires a slightly modified prefix for SQLAlchemy to use psycopg2
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Establish the connection to the Neon Cloud Database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 3. Create the Base class for your ORM models
Base = declarative_base()

# 4. Define your Table Architecture
class DetectionEvent(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    detected_at = Column(String, nullable=False) # e.g., "2026-11-03_14-30-45"
    video_filepath = Column(String, nullable=False) # e.g., "event_2026-11-03.mp4"

# 5. Build the tables in the cloud and create a Session factory
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    print("Database connected and 'detections' table successfully created in Neon!")