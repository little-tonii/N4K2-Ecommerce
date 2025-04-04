from pydantic.functional_validators import field_validator
from pydantic.main import BaseModel


class CommentOnProductRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError("Bình luận không được để trống")
        return value.strip()

class UpdateCommentRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError("Bình luận không được để trống")
        return value.strip()
