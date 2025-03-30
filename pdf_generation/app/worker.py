# app/worker.py

import json
import logging
from decimal import Decimal
from kafka import KafkaConsumer, KafkaProducer

from .config import settings
from .pdf_generator import generate_pdf
import os
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

def custom_serializer(obj):
    """
    Custom serializer for anything that isn't standard JSON-serializable.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)

def consume_messages() -> None:
    """
    Consumes Kafka messages from the specified topic,
    generates PDFs, and commits offsets on success.
    """
    logger.info("Starting Kafka consumer for topic '%s' at '%s' in group '%s'",
                settings.kafka_topic,
                settings.kafka_host,
                settings.kafka_consumer_group)

    # 1. Create Kafka consumer
    consumer = KafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=[settings.kafka_host],
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id=settings.kafka_consumer_group
    )

    # 2. Optional: create a producer for sending errors to a DLQ topic
    #    If you have no DLQ, you can omit this.
    dlq_topic = "dlq"  # or fetch from config
    producer = KafkaProducer(
        bootstrap_servers=[settings.kafka_host],
        value_serializer=lambda x: json.dumps(x, default=custom_serializer).encode('utf-8')
    )

    # 3. Create PDF storage folder if not exists
    os.makedirs(settings.pdf_storage_path, exist_ok=True)

    logger.info("Consumer is now polling messages...")

    try:
        for message in consumer:
            try:
                # 1) Decode message
                message_data = json.loads(message.value.decode('utf-8'))
                logger.info("Received message: %s", message_data)
                start_time_str = datetime.now()
                # 2) Generate PDF
                user_name = message_data.get('name', 'unknown')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = uuid.uuid4().hex[:8]  # Generate an 8-character unique id
                output_pdf_filename = f"{user_name}_{timestamp}_{unique_id}_report.pdf"
                output_pdf_path = os.path.join(settings.pdf_storage_path, output_pdf_filename)

                generate_pdf(
                    user_data=message_data,
                    template_path=os.path.join(os.path.dirname(__file__), "report.ttyp"),
                    output_pdf=output_pdf_path
                )
                if start_time_str:
                    # start_time = datetime.fromisoformat(start_time_str)
                    now = datetime.now()
                    duration = now - start_time_str
                    logger.info("Message processed in %s seconds", duration.total_seconds())

                # 3) Commit offset (ACK the message)
                consumer.commit()
            except Exception as e:
                logger.exception("Error generating PDF. Pushing to DLQ.")
                # If something goes wrong, send to DLQ topic
                producer.send(dlq_topic, message.value)
    except KeyboardInterrupt:
        logger.info("Shutting down consumer on KeyboardInterrupt...")
    finally:
        logger.info("Closing Kafka consumer...")
        consumer.close()

