from datetime import datetime
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class UserAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserInfoResponse(BaseModel):
    id: int
    email: str
    phone_number: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime
    account_type: str