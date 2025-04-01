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

class RemoveProductFromCartRequest(BaseModel):
    product_id: str

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, value: str):
        if not value.strip():
            raise ValueError("ID sản phẩm không được để trống")
        return value

class CheckoutCartRequest(BaseModel):
    full_name: str
    phone_number: str
    address: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        if not value.strip():
            raise ValueError("Tên khách hàng không được để trống")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        if not value.strip():
            raise ValueError("Số điện thoại không được để trống")
        return value

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str):
        if not value.strip():
            raise ValueError("Địa chỉ không được để trống")
        return value
