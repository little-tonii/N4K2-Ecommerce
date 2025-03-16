from datetime import datetime
from pydantic import BaseModel

class CreateProductRequest(BaseModel):
    name: str
    price: int
    description: str
    category_id: str
    image_url: str