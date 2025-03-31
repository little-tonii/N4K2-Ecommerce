from pydantic import BaseModel
from pydantic import field_validator

class AddProductToCartRequest(BaseModel):
    product_id: str
    quantity: int

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, value: str):
        if not value.strip():
            raise ValueError("ID sản phẩm không được để trống")
        return value

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Số lượng sản phẩm phải lớn hơn 0")
        return value
