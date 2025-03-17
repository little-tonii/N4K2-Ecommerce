from pydantic import BaseModel


class AddProductToCartRequest(BaseModel):
    user_id: int
    product_id: str
    quantity: int
    
class RemoveProductFromCartRequest(BaseModel):
    user_id: int
    product_id: str