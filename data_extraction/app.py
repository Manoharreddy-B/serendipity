from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
from database import main
from decimal import Decimal
from dotenv import load_dotenv
from typing import List
import jsonpickle
import os
import time
import json

load_dotenv()

kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC")
app = FastAPI()

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return str(float(obj))
    return json.dumps(obj).encode('utf-8')

def json_serializer(data):
    # Serialize with jsonpickle to handle Decimals and other custom types.
    return json.dumps(data, default=str).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=kafka_host,
    value_serializer=json_serializer)


@app.post("/transactions/")
def getAllTransactions(uid: List[int]):
    transactions = main.get_transaction(uid)
    for transaction in transactions:
        producer.send(kafka_topic, transaction)
    


