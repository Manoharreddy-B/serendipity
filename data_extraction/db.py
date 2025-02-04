import asyncpg
import os

DATABASE_URL = "postgresql://serenbhai:serenbro@localhost:5432/serendipitydb"

async def connect_to_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False