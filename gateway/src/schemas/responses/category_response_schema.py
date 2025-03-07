from datetime import datetime

from pydantic import BaseModel


class GetCategoryResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

class GetAllCategoryResponse(BaseModel):
    categories: list[GetCategoryResponse]
    
class CreateCategoryResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime