from pydantic import BaseModel


class UpdateOrderStatusRequest(BaseModel):
    status: str