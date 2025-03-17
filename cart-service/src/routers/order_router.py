from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from ..schemas.order_response_schema import GetOrdersByUserIdResponse, OrderResponse
from ..configs.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..tasks.order_tasks import OrderTasks
from ..schemas.order_request_shema import UpdateOrderStatusRequest

router = APIRouter(prefix="/order", tags=["Order"])

@router.get(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=GetOrdersByUserIdResponse)
async def get_orders_by_user_id(async_session: Annotated[AsyncSession, Depends(get_db)], user_id: int):
    return await OrderTasks.get_orders_by_user_id_task(async_session=async_session, user_id=user_id)

@router.patch(path="/status/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def update_order_status(async_session: Annotated[AsyncSession, Depends(get_db)], order_id: int, request: UpdateOrderStatusRequest):
    return await OrderTasks.update_order_status_task(async_session=async_session, order_id=order_id, order_status=request.status)