from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    kafka_host: str
    kafka_topic: str
    database_url: str
    kafka_consumer_group: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    auth_enabled: bool = False
    jwt_secret: str = "supersecret"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')  # Automatically load environment variables from .env

# Create a global instance that you can import elsewhere
settings = Settings()
