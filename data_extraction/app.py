from fastapi import FastAPI, Depends, HTTPException
from kafka import KafkaProducer
from database import main
from decimal import Decimal
from dotenv import load_dotenv
from typing import List
import jsonpickle
import time
import json
from config import settings
from database.security import require_jwt 


app = FastAPI()

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return str(float(obj))
    return json.dumps(obj).encode('utf-8')

def json_serializer(data):
    # Serialize with jsonpickle to handle Decimals and other custom types.
    return json.dumps(data, default=str).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=[settings.kafka_host],
    value_serializer=json_serializer)



@app.post("/transactions/")
def get_all_transactions(uid: List[int], _=Depends(require_jwt)):
    """
    Endpoint to get all transactions for a list of user IDs.
    Now protected by JWT if AUTH_ENABLED=true.
    """
    transactions = main.get_transaction(uid)
    for transaction in transactions:
        producer.send(settings.kafka_topic, transaction)
    return {"status": "OK", "message": "Transactions published"}


