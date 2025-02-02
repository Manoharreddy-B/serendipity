from fastapi import FastAPI, HTTPException
import asyncpg
from db import connect_to_db
from kafka import KafkaProducer
import time
import json
from database import main
from decimal import Decimal

app = FastAPI()

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

@app.get("/transactions/{uid}")
def getAllTransactions(uid: int):
    transaction = main.get_transaction(uid)
    print('hello!',transaction)
    producer.send("pdf_gen", transaction)
    


