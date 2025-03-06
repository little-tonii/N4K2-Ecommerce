from datetime import datetime
from fastapi import HTTPException
import httpx
from starlette import status
from ..configs.variables import USER_SERVICE_URL
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CustomerService:
    
    @classmethod
    async def register_customer(email: str, password: str) -> CustomerRegisterResposne:
        async with httpx.AsyncClient() as client:
            hashed_password = bcrypt_context.hash(password)
            response = await client.post(f"{USER_SERVICE_URL}/user/", json={'email': email, 'hashed_password': hashed_password})
            if response.status_code == status.HTTP_201_CREATED:
                return CustomerRegisterResposne(
                    id=response.json().get('id'),
                    email=response.json().get('email'),
                    phone_number=response.json().get('phone_number'),
                    address=response.json().get('address'),
                    created_at=datetime.fromisoformat(response.json().get('created_at')),
                    updated_at=datetime.fromisoformat(response.json().get('updated_at')),
                    account_type=response.json().get('account_type')
                )
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.json().get('message'))
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')