import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load the database URL from environment (or default to a known string)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://serenbhai:serenbro@localhost:5432/serendipitydb")

# 2. Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True will log SQL queries

# 3. Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 4. Create a base class for our models
Base = declarative_base()
