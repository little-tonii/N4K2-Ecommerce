from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class UserAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str