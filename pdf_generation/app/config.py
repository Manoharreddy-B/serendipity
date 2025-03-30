# app/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    kafka_host: str
    kafka_topic: str
    database_url: str
    kafka_consumer_group: str
    pdf_storage_path: str
    pdf_app_host: str
    pdf_app_port: int

    class Config:
        # Adjust to your own .env path or remove if you plan to
        # pass environment variables some other way (like Docker ENV)
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')

settings = Settings()
