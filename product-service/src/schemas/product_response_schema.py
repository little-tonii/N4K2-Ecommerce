from datetime import datetime
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str
    category_id: str
    image_url: str
    created_at: datetime
    updated_at: datetime

class RecommendationProductResponse(ProductResponse):
    id: str
    name: str
    price: int
    description: str
    category_id: str
    image_url: str
    created_at: datetime
    updated_at: datetime
    rate: float