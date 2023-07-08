import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=dotenv_path)
class Settings(BaseSettings):
    mongo_url: str = os.getenv("MONGODB_URL")


settings = Settings()
