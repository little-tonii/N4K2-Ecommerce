from fastapi import HTTPException
import httpx
import pendulum
from starlette import status
from datetime import datetime
from ..models.user_model import AccountType

from ..configs.variables import PRODUCT_SERVICE_URL
from ..schemas.responses.category_response_schema import CreateCategoryResponse, GetAllCategoryResponse, GetCategoryResponse
from typing import cast

class CategoryService:

    @classmethod
    async def get_all_categories(cls) -> GetAllCategoryResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{PRODUCT_SERVICE_URL}/category/")
                response.raise_for_status()
                return GetAllCategoryResponse(
                    categories=[
                        GetCategoryResponse(
                            id=category["id"],
                            name=category["name"],
                            created_at=cast(datetime, pendulum.parse(category["created_at"])),
                            updated_at=cast(datetime, pendulum.parse(category["updated_at"]))
                        )
                        for category in response.json()
                    ]
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ sản phẩm")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ sản phẩm không khả dụng')

    @classmethod
    async def create_category(cls, account_type: str, name: str) -> CreateCategoryResponse:
        if account_type != AccountType.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{PRODUCT_SERVICE_URL}/category/", json={ "name": name })
                response.raise_for_status()
                created_at = cast(datetime, pendulum.parse(response.json()["created_at"]))
                updated_at = cast(datetime, pendulum.parse(response.json()["updated_at"]))
                return CreateCategoryResponse(
                    id=response.json()["id"],
                    name=response.json()["name"],
                    created_at=created_at,
                    updated_at=updated_at
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ sản phẩm")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ sản phẩm không khả dụng')
