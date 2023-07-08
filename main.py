from datetime import datetime
from fastapi import Body, FastAPI, Response, status, Query, HTTPException
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List


from models.product import Product
from models.order import Order, CreateOrder
from config.config import settings

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db = client.ecommerce


@app.get("/",response_description="Home")
async def home():
    return {"status": "ok"}


@app.get("/products/", response_description="List all products", response_model=List[Product])
async def list_products(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400, detail="Invalid limit. Limit must be between 1 and 1000.")
    if offset < 0:
        raise HTTPException(
            status_code=400, detail="Invalid offset. Offset must be greater than or equal to 0.")

    products = await db["products"].find().skip(offset).limit(limit).to_list(limit)
    return products



@app.post("/products/", response_description="Add new product", response_model=Product)
async def create_product(product: Product = Body(...)):
    product = jsonable_encoder(product)
    new_product = await db["products"].insert_one(product)
    created_student = await db["products"].find_one({"_id": new_product.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@app.get("/orders/", response_description="List all orders", response_model=List[Order])
async def list_orders(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="Invalid limit. Limit must be between 1 and 1000.")
    if offset < 0:
        raise HTTPException(status_code=400, detail="Invalid offset. Offset must be greater than or equal to 0.")

    orders = await db["orders"].find().skip(offset).limit(limit).to_list(limit)
    return orders




@app.post("/orders/", response_description="Add new order")
async def create_order(order: CreateOrder):
    total_amount = 0.0
    created_order = Order(items=[], timestamp=datetime.now(),total_amount=0.0,user_address=order.user_address)

    if not order.items:
        raise HTTPException(status_code=400, detail="No items provided in the order.")

    for item in order.items:
        product = await db["products"].find_one({"_id": item.product_id})
        current_product: Product = Product(**product)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with name {current_product.name} not found.")

        if item.bought_quantity > current_product.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity for product with ID {current_product.name}.")

        created_order.items.append(item)
        total_amount += current_product.price * item.bought_quantity

        # Update product quantity
        new_quantity = current_product.quantity - item.bought_quantity
        await db["products"].update_one({"_id": item.product_id}, {"$set": {"quantity": new_quantity}})

    # Create the order
    created_order.total_amount = total_amount

    new_order = await db["orders"].insert_one(created_order.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "total_amount": total_amount
    })