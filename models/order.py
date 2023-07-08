from typing import List
from datetime import datetime
from pydantic import BaseModel


class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str


class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int

class CreateOrder(BaseModel):
    timestamp: datetime = datetime.now()
    items: List[OrderItem]
    user_address: UserAddress

class Order(BaseModel):
    timestamp: datetime = datetime.now()
    items: List[OrderItem]
    total_amount: float
    user_address: UserAddress
