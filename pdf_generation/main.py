from kafka import KafkaConsumer
import json
import time

def consume_messages():
    
    consumer = KafkaConsumer(
        "pdf_gen",
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', 
        enable_auto_commit=True,
        group_id='your_consumer_group'
    )

    try:
        for message in consumer:
            message_data = message.value.decode('utf-8')
            print(f"Received Message:{message_data}")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()