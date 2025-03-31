from pydantic import BaseModel

class AddProductToCartResponse(BaseModel):
    product_id: str
    quantity: int
    price: int
