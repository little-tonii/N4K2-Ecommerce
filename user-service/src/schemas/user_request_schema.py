from typing import Optional
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    hashed_password: str
    
class UpdateUserRequest(BaseModel):
    hashed_password: Optional[str] = None
    refresh_token: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None