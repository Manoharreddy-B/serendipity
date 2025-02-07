from decimal import Decimal
from kafka import KafkaConsumer, KafkaProducer
import json
import time
from generate_pdf import generate_pdf
from concurrent.futures import ThreadPoolExecutor
import threading

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

    reference_time = time.time()
    def process_message(message):
        try:
            message_data = json.loads(message.value.decode('utf-8'))
            thread_id = threading.get_ident()
            print(f"Thread ID: {thread_id}, Received Message: {message_data}",time.time()-reference_time)
            generate_pdf(message_data)

            ## commiting kafka message after pdf generation
            consumer.commit()
        except Exception as e:
            print(f"Error while generating the pdf for user {message_data['name']}")
            print("Error message:", e)

            producer.send("dlq", message) 
            
    with ThreadPoolExecutor(max_workers=10) as executor:
        try:
            for message in consumer:
                executor.submit(process_message, message)
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

if __name__ == "__main__":
    consume_messages()