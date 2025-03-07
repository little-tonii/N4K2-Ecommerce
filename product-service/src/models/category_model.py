from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .py_object_id import PyObjectId

class CategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {ObjectId: str}