from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncpg
from db import connect_to_db
from kafka import KafkaProducer
import time
import json
from database import main
from decimal import Decimal
from auth.auth import TokenReponse, create_access_token, decode_access_token, users

app = FastAPI()

security = HTTPBasic()

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return json.dumps(obj)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x, default=custom_serializer).encode('utf-8'))

# class MockKafkaProducer:
#     def send(self, topic, value):
#         print(f"Mocked Kafka Producer: Sent message to {topic}: {value}")
#         return None

# #producer = MockKafkaProducer()

# @app.get("/")
# def read_root():
#     return {"message":"Hello World!"}

# @app.get("/checkConnection")
# async def connection_check():
#     is_connected = await connect_to_db()
#     #is_connected = True
#     if is_connected:
#         for i in range(5):
#             message = f"konchem channge {i}"
#             producer.send("pdf_gen", message)
#             print(f"Message {i} is sent to kafka")
#             #time.sleep(1)
            
#         return {"status": "success", "message": "Database connection successful"}
#     else:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     producer.flush()
#     producer.close()

@app.post("/token", response_model=TokenReponse)
def login(credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials)
    user = users.get(credentials.username)
    if not user or user.get("password") != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    access_token = create_access_token(user_id=user["id"])
    return TokenReponse(access_token=access_token)

@app.get("/transactions/{uid}")
def getAllTransactions(uid: int, request: Request):
    print(request.headers)
    authorization: str = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    print(token)
    payload = decode_access_token(token=token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    transaction = main.get_transaction(uid)
    print('hello!', transaction)
    producer.send("pdf_gen", transaction)
    return {"message": "Transaction sent"}
    


