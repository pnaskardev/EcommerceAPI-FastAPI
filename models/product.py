from typing import Union
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    quantity: int = 0