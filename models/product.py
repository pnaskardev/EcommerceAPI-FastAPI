from bson import ObjectId
from pydantic import BaseModel, Field
import json

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class Product(BaseModel):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Product",
                "price": 10.99,
                "quantity": 5,
            }
        }
        populate_by_name = True
        arbitrary_types_allowed = True
        exclude = {"id"}

    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str = Field(...)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    quantity: int = Field(..., gt=0, description="The quantity must be greater than zero")

    def json(self, *args, **kwargs):
        kwargs["default"] = lambda o: str(o) if isinstance(o, ObjectId) else o
        return json.dumps(self.dict(), *args, **kwargs)
