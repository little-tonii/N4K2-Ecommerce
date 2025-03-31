import httpx
from ..configs.variables import PRODUCT_SERVICE_URL
from fastapi import HTTPException, UploadFile
from ..schemas.responses.product_response_schema import UpdateProductResponse, GetProductResponse, GetProductsResponse, CreateProductResponse, UpdateProductImageResponse
from typing import cast
from datetime import datetime
import pendulum
from starlette import status
from ..models.user_model import AccountType
from pathlib import Path
import uuid
import shutil
from typing import Optional

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

    @classmethod
    async def get_product(cls, id: str) -> GetProductResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{PRODUCT_SERVICE_URL}/product/{id}")
                response.raise_for_status()
                product = response.json()
                return GetProductResponse(
                    id=product["id"],
                    name=product["name"],
                    price=product["price"],
                    description=product["description"],
                    category_id=product["category_id"],
                    image_url=product["image_url"],
                    created_at=cast(datetime, pendulum.parse(product["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(product["updated_at"]))
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ sản phẩm")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")

    @classmethod
    async def create_product(cls, account_type: str, name: str, price: int, description: str, category_id: str, picture: UploadFile) -> CreateProductResponse:
        if account_type != AccountType.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        try:
            async with httpx.AsyncClient() as client:
                category_response = await client.get(f"{PRODUCT_SERVICE_URL}/category/{category_id}")
                category_response.raise_for_status()
                file_extension = Path(picture.filename or "").suffix
                new_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = Path("public/images") / new_filename
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(picture.file, buffer)
                image_url = f"/public/images/{new_filename}"
                product_response = await client.post(f"{PRODUCT_SERVICE_URL}/product/", json={
                    "name": name,
                    "price": price,
                    "description": description,
                    "category_id": category_id,
                    "image_url": image_url
                })
                product_response.raise_for_status()
                product = product_response.json()
                return CreateProductResponse(
                    id=product["id"],
                    name=product["name"],
                    price=product["price"],
                    description=product["description"],
                    category_id=product["category_id"],
                    image_url=product["image_url"],
                    created_at=cast(datetime, pendulum.parse(product["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(product["updated_at"]))
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Danh mục không tồn tại")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ sản phẩm')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")

    @classmethod
    async def update_product(cls, account_type: str, id: str, name: Optional[str], price: Optional[int], description: Optional[str], category_id: Optional[str]) -> UpdateProductResponse:
        if account_type != AccountType.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        prepare_update_data = {}
        if name:
            prepare_update_data["name"] = name
        if price:
            prepare_update_data["price"] = price
        if description:
            prepare_update_data["description"] = description
        if category_id:
            prepare_update_data["category_id"] = category_id
        if not prepare_update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Vui lòng nhập dữ liệu cần cập nhật')
        try:
            async with httpx.AsyncClient() as client:
                product_response = await client.patch(f"{PRODUCT_SERVICE_URL}/product/{id}", json=prepare_update_data)
                product_response.raise_for_status()
                product = product_response.json()
                return UpdateProductResponse(
                    id=product["id"],
                    name=product["name"],
                    price=product["price"],
                    description=product["description"],
                    category_id=product["category_id"],
                    image_url=product["image_url"],
                    created_at=cast(datetime, pendulum.parse(product["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(product["updated_at"]))
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ sản phẩm')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")

    @classmethod
    async def update_product_image(cls, id: str, account_type: str, picture: UploadFile) -> UpdateProductImageResponse:
        if account_type != AccountType.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        image_dir = Path("public/images")
        try:
            async with httpx.AsyncClient() as client:
                product_response = await client.get(f"{PRODUCT_SERVICE_URL}/product/{id}")
                product_response.raise_for_status()
                product = product_response.json()
                old_image_url = product.get("image_url")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ sản phẩm')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")
        if old_image_url:
            old_image_path = Path("") / old_image_url.lstrip("/")
            if old_image_path.exists():
                old_image_path.unlink()
        file_extension = Path(picture.filename or "").suffix
        new_filename = f"{uuid.uuid4()}{file_extension}"
        new_image_path = image_dir / new_filename
        with new_image_path.open("wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
        new_image_url = f"/public/images/{new_filename}"
        try:
            async with httpx.AsyncClient() as client:
                update_response = await client.patch(f"{PRODUCT_SERVICE_URL}/product/{id}", json={"image_url": new_image_url})
                update_response.raise_for_status()
                updated_product = update_response.json()
                return UpdateProductImageResponse(
                    id=updated_product["id"],
                    image_url=updated_product["image_url"],
                    created_at=cast(datetime, pendulum.parse(updated_product["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(updated_product["updated_at"]))
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ sản phẩm')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")
