from typing import Optional
from fastapi import HTTPException
import httpx
import pendulum
from starlette import status
from datetime import datetime
from ..models.user_model import AccountType
from ..configs.variables import USER_SERVICE_URL
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne, CustomerUpdateInfoResponse
from ..services.user_service import bcrypt_context
from typing import cast
from ..schemas.responses.cart_response_schema import ProductInCart, CartResponse, AddProductToCartResponse
from ..configs.variables import PRODUCT_SERVICE_URL, CART_SERVICE_URL

class CustomerService:

    @classmethod
    async def update_customer_info(cls, customer_id: int, phone_number: Optional[str], address: Optional[str], account_type: str) -> CustomerUpdateInfoResponse:
        try:
            async with httpx.AsyncClient() as client:
                if account_type != AccountType.CUSTOMER:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
                request_data = {}
                if phone_number:
                    request_data['phone_number'] = phone_number
                if address:
                    request_data['address'] = address
                if not request_data:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng gửi thông tin cần cập nhật")
                response = await client.patch(f"{USER_SERVICE_URL}/user/{customer_id}", json=request_data)
                response.raise_for_status()
                return CustomerUpdateInfoResponse(
                        id=int(response.json().get('id')),
                        email=response.json().get('email'),
                        phone_number=response.json().get('phone_number'),
                        address=response.json().get('address'),
                        created_at=cast(datetime, pendulum.parse(response.json()["created_at"])),
                        updated_at=cast(datetime, pendulum.parse(response.json()["updated_at"])),
                        account_type=response.json().get('account_type')
                    )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ người dùng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

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
                        created_at=cast(datetime, pendulum.parse(response.json()["created_at"])),
                        updated_at=cast(datetime, pendulum.parse(response.json()["updated_at"])),
                        account_type=response.json().get('account_type')
                    )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã được sử dụng")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ người dùng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Dịch vụ người dùng không khả dụng')

    @classmethod
    async def add_product_to_cart(cls, user_id: int, account_type: str, product_id: str, quantity: int) -> AddProductToCartResponse:
        if account_type != AccountType.CUSTOMER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không phải là khách hàng")
        try:
            async with httpx.AsyncClient() as client:
                product_response = await client.get(f"{PRODUCT_SERVICE_URL}/product/{product_id}")
                product_response.raise_for_status()
                product = product_response.json()
                product_price = product.get("price")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ sản phẩm')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ sản phẩm không khả dụng")
        try:
            async with httpx.AsyncClient() as client:
                cart_response = await client.post(f"{CART_SERVICE_URL}/cart/product", json={
                    "user_id": user_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": product_price
                })
                cart_response.raise_for_status()
                added_item = cart_response.json()
                return AddProductToCartResponse(
                    product_id=added_item["product_id"],
                    quantity=added_item["quantity"],
                    price=added_item["price"]
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ giỏ hàng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ giỏ hàng không khả dụng")

    @classmethod
    async def get_cart(cls, user_id: int, account_type: str) -> CartResponse:
        if account_type != AccountType.CUSTOMER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không phải là khách hàng")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{CART_SERVICE_URL}/cart/{user_id}")
                response.raise_for_status()
                products = response.json()["products"]
                return CartResponse(
                    products=[
                        ProductInCart(
                            product_id=product["product_id"],
                            quantity=product["quantity"],
                            price=product["price"]
                        )
                        for product in products
                    ]
                )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ giỏ hàng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ giỏ hàng không khả dụng")

    @classmethod
    async def remove_product_from_cart(cls, account_type: str, user_id: int, product_id: str) -> None:
        if account_type != AccountType.CUSTOMER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Bạn không phải là khách hàng')
        try:
            async with httpx.AsyncClient() as client:
                await client.delete(f"{CART_SERVICE_URL}/cart/product/{user_id}&{product_id}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Sản phẩm không tồn tại trong giỏ hàng')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Có lỗi xảy ra phía dịch vụ giỏ hàng')
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            raise HTTPException(status_code=500, detail="Dịch vụ giỏ hàng không khả dụng")
