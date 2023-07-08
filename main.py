from datetime import datetime
from bson import ObjectId
from fastapi import Body, FastAPI, status, Query, HTTPException
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


@app.get("/", response_description="Home")
async def home():
    return {"status": "ok"}


@app.get("/get-products/", response_description="List all products", response_model=List[Product])
async def list_products(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400, detail="Invalid limit. Limit must be between 1 and 1000.")
    if offset < 0:
        raise HTTPException(
            status_code=400, detail="Invalid offset. Offset must be greater than or equal to 0.")

    products = await db["products"].find().skip(offset).limit(limit).to_list(limit)
    return products


@app.post("/post-products/", response_description="Add new product", response_model=Product)
async def create_product(product: Product = Body(...)):
    product = jsonable_encoder(product)
    new_product = await db["products"].insert_one(product)
    created_student = await db["products"].find_one({"_id": new_product.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@app.put("/edit-products/{product_id}", response_description="Update product")
async def update_product(product_id: str, product: Product = Body(...)):
    existing_product = await db["products"].find_one({"_id": product_id})
    if not existing_product:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found.")

    # Update the product
    updated_product = product.dict(exclude_unset=True)  # Exclude unset fields
    await db["products"].update_one({"_id": product_id}, {"$set": updated_product})

    new_product = await db["products"].find_one({"_id": product_id})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Product updated succesfully", "product": new_product})


@app.get("/get-orders/", response_description="List all orders", response_model=List[Order])
async def list_orders(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400, detail="Invalid limit. Limit must be between 1 and 1000.")
    if offset < 0:
        raise HTTPException(
            status_code=400, detail="Invalid offset. Offset must be greater than or equal to 0.")

    orders = await db["orders"].find().skip(offset).limit(limit).to_list(limit)
    return orders


@app.post("/post-orders/", response_description="Add new order")
async def create_order(order: CreateOrder):
    total_amount = 0.0
    created_order = Order(items=[], timestamp=datetime.now(
    ), total_amount=0.0, user_address=order.user_address)

    if not order.items:
        raise HTTPException(
            status_code=400, detail="No items provided in the order.")

    for item in order.items:
        product = await db["products"].find_one({"_id": item.product_id})
        current_product: Product = Product(**product)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product with name {current_product.name} not found.")

        if item.bought_quantity > current_product.quantity:
            raise HTTPException(
                status_code=400, detail=f"Insufficient quantity for product with ID {current_product.name}.")

        created_order.items.append(item)
        total_amount += current_product.price * item.bought_quantity

        # Update product quantity
        new_quantity = current_product.quantity - item.bought_quantity
        await db["products"].update_one({"_id": item.product_id}, {"$set": {"quantity": new_quantity}})

    # Create the order
    created_order.total_amount = total_amount

    await db["orders"].insert_one(created_order.dict())
    new_order = await db["orders"].find_one({"_id": ObjectId(created_order.id)})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "new_order": new_order
    })


@app.get("/orders/{order_id}", response_description="Get a single order", response_model=Order)
async def get_order(order_id: str):
    order = await db["orders"].find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found.")

    return Order(**order)
