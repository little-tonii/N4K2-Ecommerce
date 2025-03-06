from pydantic import BaseModel, field_validator


class UserRefreshTokenRequest(BaseModel):
    refresh_token: str
    
    @field_validator("refresh_token")
    @classmethod
    def validate_refresh_token(cls, value: str):
        if not value.strip():
            raise ValueError("Refresh token không được để trống")
        return value
    
class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    
    @field_validator("old_password")
    @classmethod
    def validate_old_password(cls, value: str):
        if not value.strip():
            raise ValueError("Mật khẩu cũ không được để trống")
        return value
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str):
        if not value.strip():
            raise ValueError("Mật khẩu mới không được để trống")
        if len(value) < 6:
            raise ValueError("Mật khẩu mới phải có ít nhất 6 ký tự")
        return value