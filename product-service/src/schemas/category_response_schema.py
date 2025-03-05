from datetime import datetime
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime