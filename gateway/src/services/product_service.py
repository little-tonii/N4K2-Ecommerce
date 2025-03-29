import httpx
from ..configs.variables import PRODUCT_SERVICE_URL
from fastapi import HTTPException
from ..schemas.responses.product_response_schema import GetProductResponse, GetProductsResponse
from typing import cast
from datetime import datetime
import pendulum
from starlette import status

class ProductService:

    @classmethod
    async def get_products(cls) -> GetProductsResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{PRODUCT_SERVICE_URL}/product/")
                response.raise_for_status()
                return GetProductsResponse(
                    products=[
                        GetProductResponse(
                            id=product["id"],
                            name=product["name"],
                            price=product["price"],
                            description=product["description"],
                            category_id=product["category_id"],
                            image_url=product["image_url"],
                            created_at=cast(datetime, pendulum.parse(product["created_at"])),
                            updated_at=cast(datetime, pendulum.parse(product["updated_at"]))
                        )
                        for product in response.json()
                    ]
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ sản phẩm")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")
