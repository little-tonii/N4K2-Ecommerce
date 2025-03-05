from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .py_object_id import PyObjectId

class CategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {ObjectId: str}