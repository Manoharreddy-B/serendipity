from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Load the database URL from environment (or default to a known string)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True will log SQL queries

# 3. Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 4. Create a base class for our models
Base = declarative_base()
