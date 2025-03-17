from pydantic import BaseModel


class AddProductToCartResponse(BaseModel):
    user_id: int
    product_id: str
    quantity: int
    price: int
    
class ProductInCart(BaseModel):
    product_id: str
    quantity: int
    price: int

class GetProductsInCartResponse(BaseModel):
    products: list[ProductInCart]
    
class CheckOutCartResponse(BaseModel):
    id: int
    total_price: int
    phone_number: int
    address: str
    full_name: str
    status: str
    products: list[str]