from typing import Optional
from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError

class CustomerRegisterRequest(BaseModel):
    email: str
    password: str
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        if not value.strip():
            raise ValueError("Email không được để trống")
        try:
            email_infor = validate_email(value, check_deliverability=True)
            return email_infor.normalized
        except EmailNotValidError:
            raise ValueError(f"Email {value} không hợp lệ")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not value.strip():
            raise ValueError("Mật khẩu không được để trống")
        if len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value
    
class CustomerUpdateInfoRequest(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None):
        if value is None:
            return None
        if not value.strip():
            raise ValueError("Số điện thoại không được để trống")
        return value
    
    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str | None):
        if value is None:
            return None
        if not value.strip():
            raise ValueError("Địa chỉ không được để trống")
        return value