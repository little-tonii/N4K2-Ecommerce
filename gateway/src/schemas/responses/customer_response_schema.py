from datetime import datetime
from pydantic import BaseModel


class CustomerRegisterResposne(BaseModel):
    id: int
    email: str
    phone_number: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime
    account_type: str