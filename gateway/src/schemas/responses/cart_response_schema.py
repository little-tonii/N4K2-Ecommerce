from pydantic import BaseModel

class AddProductToCartResponse(BaseModel):
    product_id: str
    quantity: int
    price: int

class ProductInCart(BaseModel):
    product_id: str
    quantity: int
    price: int

class CartResponse(BaseModel):
    products: list[ProductInCart]

class CartCheckoutResponse(BaseModel):
    id: int
    total_price: int
    phone_number: str
    address: str
    status: str
    full_name: str
    products: list[ProductInCart]
