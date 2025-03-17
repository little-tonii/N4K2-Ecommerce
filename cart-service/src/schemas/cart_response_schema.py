from pydantic import BaseModel


class AddProductToCartResponse(BaseModel):
    user_id: int
    product_id: str
    quantity: int
    
class ProductInCart(BaseModel):
    product_id: str
    quantity: int

class GetProductsInCartResponse(BaseModel):
    products: list[ProductInCart]