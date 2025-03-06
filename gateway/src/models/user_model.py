from datetime import datetime

from pydantic import BaseModel

class AccountType:
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class UserModel(BaseModel):
    id: int
    email: str
    hashed_password: str
    refresh_token: str
    phone_number: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime
    account_type: str