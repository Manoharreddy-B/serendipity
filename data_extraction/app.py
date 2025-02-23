from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
from database import main
from decimal import Decimal
from dotenv import load_dotenv
from typing import List
import os
import time
import json

load_dotenv()

kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC")
app = FastAPI()

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return json.dumps(obj)

producer = KafkaProducer(
    bootstrap_servers=kafka_host,
    value_serializer=lambda x: json.dumps(x, default=custom_serializer).encode('utf-8'))


@app.post("/transactions/")
def getAllTransactions(uid: List[int]):
    transaction = main.get_transaction(uid)
    producer.send(kafka_topic, transaction)
    


