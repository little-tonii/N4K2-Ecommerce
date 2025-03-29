from pydantic import BaseModel, field_validator


class CreateCategoryRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError("Tên danh mục không được để trống")
        return value

class UpdateCategoryRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError("Tên danh mục không được để trống")
        return value
