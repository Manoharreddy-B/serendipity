from fastapi import FastAPI, HTTPException
import asyncpg
from db import connect_to_db

app = FastAPI()


@app.get("/")
def read_root():
    return {"message":"Hello World!"}

@app.get("/checkConnection")
async def connection_check():
    is_connected = await connect_to_db()
    if is_connected:
        return {"status": "success", "message": "Database connection successful"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")

