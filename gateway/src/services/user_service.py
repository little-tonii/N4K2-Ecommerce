from datetime import datetime

from fastapi import HTTPException
import pendulum

from ..schemas.responses.user_response_schema import UserAccessTokenResponse, UserInfoResponse, UserLoginResponse
from ..utils.token_util import create_access_token, create_refresh_token, verify_refresh_token
from ..models.user_model import UserModel
from ..configs.variables import USER_SERVICE_URL
import httpx
from starlette import status
from passlib.context import CryptContext
from typing import cast

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService:

    @classmethod
    async def get_user_info(cls, user_id: int) -> UserInfoResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/user/?id={user_id}")
                response.raise_for_status()
                return UserInfoResponse(
                    id=response.json().get("id"),
                    email=response.json().get("email"),
                    phone_number=response.json().get("phone_number"),
                    address=response.json().get("address"),
                    created_at=cast(datetime, pendulum.parse(response.json().get("created_at"))),
                    updated_at=cast(datetime, pendulum.parse(response.json().get("created_at"))),
                    account_type=response.json().get("account_type")
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

    @classmethod
    async def change_user_password(cls, user_id: int, new_password: str, old_password: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                get_response = await client.get(f"{USER_SERVICE_URL}/user/?id={user_id}")
                get_response.raise_for_status()
                old_hashed_password = get_response.json().get("hashed_password")
                if not bcrypt_context.verify(old_password, old_hashed_password):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu cũ không chính xác")
                new_hashed_password = bcrypt_context.hash(new_password)
                patch_response = await client.patch(f"{USER_SERVICE_URL}/user/{user_id}", json={"hashed_password": new_hashed_password})
                patch_response.raise_for_status()
                return "Đổi mật khẩu thành công"
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

    @classmethod
    async def get_access_token(cls, refresh_token: str) -> UserAccessTokenResponse:
        try:
            claims = verify_refresh_token(refresh_token)
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/user/?id={claims.id}")
                response.raise_for_status()
                refresh_token_saved = response.json()["refresh_token"]
                if refresh_token_saved != refresh_token:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")
                access_token = create_access_token(user_id=claims.id, account_type=claims.account_type)
                return UserAccessTokenResponse(access_token=access_token, token_type="bearer")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserModel | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/user/?id={user_id}")
                response.raise_for_status()
                return UserModel(
                    id=response.json().get("id"),
                    email=response.json().get("email"),
                    hashed_password=response.json().get("hashed_password"),
                    refresh_token=response.json().get("refresh_token"),
                    phone_number=response.json().get("phone_number"),
                    address=response.json().get("address"),
                    created_at=cast(datetime, pendulum.parse(response.json().get("created_at"))),
                    updated_at=cast(datetime, pendulum.parse(response.json().get("updated_at"))),
                    account_type=response.json().get("account_type")
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

    @classmethod
    async def login_user(cls, email: str, password: str) -> UserLoginResponse:
        try:
            async with httpx.AsyncClient() as client:
                get_response = await client.get(f"{USER_SERVICE_URL}/user/?email={email}")
                get_response.raise_for_status()
                id = get_response.json()["id"]
                hashed_password = get_response.json()["hashed_password"]
                account_type = get_response.json()["account_type"]
                if not bcrypt_context.verify(password, hashed_password):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email hoặc mật khẩu không chính xác")
                refresh_token = create_refresh_token(user_id=id, account_type=account_type)
                access_token = create_access_token(user_id=id, account_type=account_type)
                patch_response = await client.patch(f"{USER_SERVICE_URL}/user/{id}", json={"refresh_token": refresh_token})
                patch_response.raise_for_status()
                return UserLoginResponse(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type="bearer"
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email hoặc mật khẩu không chính xác")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')
