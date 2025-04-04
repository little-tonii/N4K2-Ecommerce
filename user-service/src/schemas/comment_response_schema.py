from datetime import datetime
from pydantic.main import BaseModel


class CommentResponse(BaseModel):
    id: int
    user_id: int
    product_id: str
    content: str
    created_at: datetime
    updated_at: datetime
