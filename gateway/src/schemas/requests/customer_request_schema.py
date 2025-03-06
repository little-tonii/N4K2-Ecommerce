from pydantic import BaseModel


class CustomerRegisterRequest(BaseModel):
    email: str
    password: str