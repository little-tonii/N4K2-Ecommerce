from pydantic.main import BaseModel


class CreateCommentRequest(BaseModel):
    user_id: int
    product_id: str
    content: str

class UpdateCommentRequest(BaseModel):
    content: str
