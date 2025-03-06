from datetime import datetime

from fastapi import HTTPException
import pendulum

from ..schemas.responses.user_response_schema import UserAccessTokenResponse, UserLoginResponse
from ..utils.token_util import create_access_token, create_refresh_token, verify_refresh_token
from ..models.user_model import UserModel
from ..configs.variables import USER_SERVICE_URL
import httpx
from starlette import status
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService:
    
    @classmethod
    async def change_user_password(cls, user_id: int, new_password: str, old_password: str) -> str:
        async with httpx.AsyncClient() as client:
            get_response = await client.get(f"{USER_SERVICE_URL}/user/?id={user_id}")
            if get_response.status_code == status.HTTP_200_OK:
                old_hashed_password = get_response.json().get("hashed_password")
                if not bcrypt_context.verify(old_password, old_hashed_password):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu cũ không chính xác")
                new_hashed_password = bcrypt_context.hash(new_password)
                patch_response = await client.patch(f"{USER_SERVICE_URL}/user/{user_id}", json={"hashed_password": new_hashed_password})
                if patch_response.status_code == status.HTTP_200_OK:
                    return "Đổi mật khẩu thành công"
                elif patch_response.status_code == status.HTTP_404_NOT_FOUND:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")
            elif get_response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
            elif get_response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")
    
    @classmethod
    async def get_access_token(cls, refresh_token: str) -> UserAccessTokenResponse:
        claims = verify_refresh_token(refresh_token)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/user/?id={claims.id}")
            if response.status_code == status.HTTP_200_OK:
                refresh_token_saved = response.json()["refresh_token"]
                if refresh_token_saved != refresh_token:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")
                access_token = create_access_token(user_id=claims.id, account_type=claims.account_type)
                return UserAccessTokenResponse(access_token=access_token, token_type="bearer")
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")
                
    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserModel | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/user/?id={user_id}")
            if response.status_code == status.HTTP_200_OK:
                return UserModel(
                    id=response.json()["id"],
                    email=response.json()["email"],
                    hashed_password=response.json()["hashed_password"],
                    refresh_token=response.json()["refresh_token"],
                    phone_number=response.json()["phone_number"],
                    address=response.json()["address"],
                    created_at=pendulum.parse(response.json()["created_at"]),
                    updated_at=pendulum.parse(response.json()["updated_at"]),
                    account_type=response.json()["account_type"]
                )
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Có lỗi xảy ra")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")
    
    @classmethod
    async def login_user(cls, email: str, password: str) -> UserLoginResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/user/?email={email}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email hoặc mật khẩu không chính xác")
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra")
            elif response.status_code == status.HTTP_200_OK:
                id = response.json()["id"]
                hashed_password = response.json()["hashed_password"]
                account_type = response.json()["account_type"]
                if not bcrypt_context.verify(password, hashed_password):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email hoặc mật khẩu không chính xác")
                refresh_token = create_refresh_token(user_id=id, account_type=account_type)
                access_token = create_access_token(user_id=id, account_type=account_type)
                response = await client.patch(f"{USER_SERVICE_URL}/user/{id}", json={"refresh_token": refresh_token})
                if response.status_code == status.HTTP_200_OK:
                    return UserLoginResponse(
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type="bearer"
                    )
                elif response.status_code == status.HTTP_404_NOT_FOUND:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email hoặc mật khẩu không chính xác")
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")