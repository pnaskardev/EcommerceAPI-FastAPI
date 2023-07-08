from fastapi import FastAPI
import motor.motor_asyncio

from config.config import settings

app = FastAPI()
client=motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)


@app.get("/")
def read_root():
    return {"Hello": "World"}