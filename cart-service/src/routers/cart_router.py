from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from ..schemas.cart_response_schema import AddProductToCartResponse, CheckOutCartResponse, GetProductsInCartResponse
from ..schemas.cart_request_schema import AddProductToCartRequest, CheckoutCartRequest, RemoveProductFromCartRequest
from sqlalchemy.ext.asyncio import AsyncSession
from ..configs.database import get_db
from ..tasks.cart_tasks import CartTasks

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post(path="/product", status_code=status.HTTP_200_OK, response_model=AddProductToCartResponse)
async def add_product_to_cart(async_session: Annotated[AsyncSession, Depends(get_db)], request: AddProductToCartRequest):
    return await CartTasks.add_product_to_cart_task(async_session=async_session, user_id=request.user_id, product_id=request.product_id, quantity=request.quantity, price=request.price)

@router.delete(path="/product/{user_id}&{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(async_session: Annotated[AsyncSession, Depends(get_db)], user_id: int, product_id: str):
    await CartTasks.remove_product_from_cart_task(async_session=async_session, user_id=user_id, product_id=product_id)

@router.get(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=GetProductsInCartResponse)
async def get_products_in_cart(async_session: Annotated[AsyncSession, Depends(get_db)], user_id: int):
    return await CartTasks.get_products_in_cart_task(async_session=async_session, user_id=user_id)

@router.post(path="/checkout", status_code=status.HTTP_201_CREATED, response_model=CheckOutCartResponse)
async def checkout(async_session: Annotated[AsyncSession, Depends(get_db)], request: CheckoutCartRequest):
    return await CartTasks.checkout_cart_task(async_session=async_session, user_id=request.user_id, phone_number=request.phone_number, address=request.address, full_name=request.full_name)
