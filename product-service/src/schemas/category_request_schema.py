from pydantic import BaseModel


class CreateCategoryRequest(BaseModel):
    name: str
    
class UpdateCategoryRequest(BaseModel):
    name: str