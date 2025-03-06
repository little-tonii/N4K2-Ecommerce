from fastapi import HTTPException
import httpx
import pendulum
from starlette import status
from ..configs.variables import USER_SERVICE_URL
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne
from ..services.user_service import bcrypt_context

class CustomerService:
    
    @classmethod
    async def register_customer(cls, email: str, password: str) -> CustomerRegisterResposne:
        try:
            async with httpx.AsyncClient() as client:
                hashed_password = bcrypt_context.hash(password)
                response = await client.post(f"{USER_SERVICE_URL}/user/", json={'email': email, 'hashed_password': hashed_password})
                response.raise_for_status()
                return CustomerRegisterResposne(
                        id=int(response.json().get('id')),
                        email=response.json().get('email'),
                        phone_number=response.json().get('phone_number'),
                        address=response.json().get('address'),
                        created_at=pendulum.parse(response.json()["created_at"]),
                        updated_at=pendulum.parse(response.json()["updated_at"]),
                        account_type=response.json().get('account_type')
                    )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã được sử dụng")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ người dùng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')