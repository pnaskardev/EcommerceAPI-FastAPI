from fastapi import Body, FastAPI, Response, status
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.product import Product
from config.config import settings

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db = client.ecommerce


@app.get("/")
async def read_root():
    # list1=await client.list_database_names()
    # list2=await db.list_collection_names()
    # return {"list1": list1,"list2":list2}
    
    return {"Hello": "World"}

@app.post("/products/",response_description="Add new product", response_model=Product)
async def create_product(product: Product=Body(...)):
    product = jsonable_encoder(product)
    new_product = await db["products"].insert_one(product)
    created_student = await db["products"].find_one({"_id": new_product.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
