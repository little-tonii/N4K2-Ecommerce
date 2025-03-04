from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    hashed_password: str
    refresh_token: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime
    account_type: str