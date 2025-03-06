from datetime import datetime

from fastapi import HTTPException
from ..models.user_model import UserModel
from ..models.user_model import AccountType
from ..configs.variables import USER_SERVICE_URL
import httpx
from starlette import status

class UserService:
    
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
                    created_at=datetime.fromisoformat(response.json()["created_at"]),
                    updated_at=datetime.fromisoformat(response.json()["updated_at"]),
                    account_type=response.json()["account_type"]
                )
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Có lỗi xảy ra")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dịch vụ người dùng không khả dụng")