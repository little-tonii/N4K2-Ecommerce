from pydantic import BaseModel
from typing import Optional
from pydantic import field_validator

class UpdateProductRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    category_id: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]):
        if value and not value.strip():
            raise ValueError("Tên không được để trống")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Optional[int]):
        if value and value <= 0:
            raise ValueError("Giá sản phẩm phải lớn hơn 0")
        return value

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: Optional[str]):
        if value and not value.strip():
            raise ValueError("ID danh mục không được để trống")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]):
        if value and not value.strip():
            raise ValueError("Mô tả sản phẩm không được để trống")
        return value
