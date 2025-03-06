from datetime import datetime
from pydantic import BaseModel


class CustomerRegisterResposne(BaseModel):
    id: int
    email: str
    phone_number: str
    address: str
    created_at: datetime
    updated_at: datetime
    account_type: str