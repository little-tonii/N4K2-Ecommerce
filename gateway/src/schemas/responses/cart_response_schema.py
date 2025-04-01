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
