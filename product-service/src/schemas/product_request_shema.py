from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UpdateProductRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    image_url: Optional[str] = None
    
class CreateProductRequest(BaseModel):
    name: str
    price: int
    description: str
    category_id: str
    image_url: str