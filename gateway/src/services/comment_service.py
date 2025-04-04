from ..configs.variables import PRODUCT_SERVICE_URL, USER_SERVICE_URL
from ..schemas.responses.comment_response_schema import CommentOnProductResponse, UpdateCommentResponse, GetCommentsResponse
from fastapi import HTTPException
import httpx
from starlette import status
from datetime import datetime
import pendulum
from typing import cast


class CommentService:

    @classmethod
    async def create_comment(cls, user_id: int, content: str, product_id: str) -> CommentOnProductResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{PRODUCT_SERVICE_URL}/product/{id}")
                response.raise_for_status()

            async with httpx.AsyncClient() as client:
                response = await client.post(f"{USER_SERVICE_URL}/comment/", json={
                    "user_id": user_id,
                    "content": content,
                    "product_id": product_id
                })
                response.raise_for_status()
                return CommentOnProductResponse(
                    id=response.json()["id"],
                    user_id=response.json()["user_id"],
                    content=response.json()["content"],
                    product_id=response.json()["product_id"],
                    created_at=cast(datetime, pendulum.parse(response.json()["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(response.json()["updated_at"]))
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ người dùng không khả dụng")

    @classmethod
    async def update_comment(cls, comment_id: int, content: str) -> UpdateCommentResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(f"{USER_SERVICE_URL}/comment/{comment_id}", json={"content": content})
                response.raise_for_status()
                return UpdateCommentResponse(
                    id=response.json()["id"],
                    user_id=response.json()["user_id"],
                    content=response.json()["content"],
                    product_id=response.json()["product_id"],
                    created_at=cast(datetime, pendulum.parse(response.json()["created_at"])),
                    updated_at=cast(datetime, pendulum.parse(response.json()["updated_at"]))
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bình luận")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ người dùng không khả dụng")

    @classmethod
    async def delete_comment(cls, comment_id: int) -> None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{USER_SERVICE_URL}/comment/{comment_id}")
                response.raise_for_status()
                return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bình luận")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ người dùng không khả dụng")

    @classmethod
    async def get_all_comments_by_user_id(cls, user_id: int) -> GetCommentsResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/comment/user/{user_id}")
                response.raise_for_status()
                return GetCommentsResponse(
                    comments=[
                        CommentOnProductResponse(
                            id=comment["id"],
                            user_id=comment["user_id"],
                            content=comment["content"],
                            product_id=comment["product_id"],
                            created_at=cast(datetime, pendulum.parse(comment["created_at"])),
                            updated_at=cast(datetime, pendulum.parse(comment["updated_at"]))
                        )
                        for comment in response.json()
                    ]
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ người dùng không khả dụng")

    @classmethod
    async def get_all_comments_by_product_id(cls, product_id: str) -> GetCommentsResponse:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{USER_SERVICE_URL}/comment/product/{product_id}")
                response.raise_for_status()
                return GetCommentsResponse(
                    comments=[
                        CommentOnProductResponse(
                            id=comment["id"],
                            user_id=comment["user_id"],
                            content=comment["content"],
                            product_id=comment["product_id"],
                            created_at=cast(datetime, pendulum.parse(comment["created_at"])),
                            updated_at=cast(datetime, pendulum.parse(comment["updated_at"]))
                        )
                        for comment in response.json()
                    ]
                )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra phía dịch vụ người dùng")
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ người dùng không khả dụng")
