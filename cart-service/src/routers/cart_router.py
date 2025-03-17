from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from ..schemas.cart_response_schema import AddProductToCartResponse, GetProductsInCartResponse
from ..schemas.cart_request_schema import AddProductToCartRequest, RemoveProductFromCartRequest
from sqlalchemy.ext.asyncio import AsyncSession
from ..configs.database import get_db
from ..tasks.cart_tasks import CartTasks

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post(path="/product", status_code=status.HTTP_200_OK, response_model=AddProductToCartResponse)
async def add_product_to_cart(async_session: Annotated[AsyncSession, Depends(get_db)], request: AddProductToCartRequest):
    return await CartTasks.add_product_to_cart_task(async_session=async_session, user_id=request.user_id, product_id=request.product_id, quantity=request.quantity)

@router.delete(path="/product", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(async_session: Annotated[AsyncSession, Depends(get_db)], request: RemoveProductFromCartRequest):
    await CartTasks.remove_product_from_cart(async_session=async_session, user_id=request.user_id, product_id=request.product_id)
    
@router.get(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=GetProductsInCartResponse)
async def get_products_in_cart(async_session: Annotated[AsyncSession, Depends(get_db)], user_id: int):
    return await CartTasks.get_products_in_cart(async_session=async_session, user_id=user_id)