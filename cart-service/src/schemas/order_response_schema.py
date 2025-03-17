from pydantic import BaseModel

class OrderResponse(BaseModel):
    id: int
    total_price: int
    phone_number: int
    address: str
    full_name: str
    status: str
    products: list[str]
    
class GetOrdersByUserIdResponse(BaseModel):
    orders: list[OrderResponse]