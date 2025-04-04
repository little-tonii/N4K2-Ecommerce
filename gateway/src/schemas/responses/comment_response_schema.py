from datetime import datetime
from pydantic.main import BaseModel

class CommentOnProductResponse(BaseModel):
    id: int
    content: str
    user_id: int
    product_id: str
    created_at: datetime
    updated_at: datetime

class UpdateCommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    product_id: str
    created_at: datetime
    updated_at: datetime

class GetCommentsResponse(BaseModel):
    comments: list[CommentOnProductResponse]
