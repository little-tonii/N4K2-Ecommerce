from pydantic import BaseModel


class AddProductToCartRequest(BaseModel):
    user_id: int
    product_id: str
    quantity: int
    price: int
    
class RemoveProductFromCartRequest(BaseModel):
    user_id: int
    product_id: str
    
class CheckoutCartRequest(BaseModel):
    user_id: int
    full_name: str
    phone_number: str
    address: str