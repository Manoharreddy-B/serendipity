from kafka import KafkaConsumer, KafkaProducer
import json
import time
from generate_pdf import generate_pdf
from decimal import Decimal

def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return json.dumps(obj)

def consume_messages():
    
    consumer = KafkaConsumer(
        "pdf_gen",
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', 
        enable_auto_commit=False,
        group_id='your_consumer_group'
    )

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x, default=custom_serializer).encode('utf-8'))


    try:
        for message in consumer:
            try:
                message_data = json.loads(message.value.decode('utf-8'))
                print(f"Received Message:{message_data}")
                generate_pdf(message_data)

                ## commiting kafka message after pdf genertion
                consumer.commit()
            except Exception as e:
                print(f"Error while generating the pdf for user{message_data['name']}")
                print("Error message:", e)

                producer.send("dlq", message)
            except KeyboardInterrupt:
                pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()