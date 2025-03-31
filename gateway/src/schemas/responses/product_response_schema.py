from pydantic import BaseModel
from datetime import datetime
from typing import List
from pydoc import cli

class GetProductResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str
    category_id: str
    image_url: str
    created_at: datetime
    updated_at: datetime

class GetProductsResponse(BaseModel):
    products: List[GetProductResponse]

class CreateProductResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str
    category_id: str
    image_url: str
    created_at: datetime
    updated_at: datetime

class UpdateProductResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str
    category_id: str
    image_url: str
    created_at: datetime
    updated_at: datetime

class UpdateProductImageResponse(BaseModel):
    id: str
    image_url: str
    created_at: datetime
    updated_at: datetime
