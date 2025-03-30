from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


# 1. Load the database URL from environment & Create the SQLAlchemy engine
engine = create_engine(settings.database_url, echo=True)  # echo=True will log SQL queries

# 2. Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # # 3. Create a base class for our models
# Base = declarative_base()
