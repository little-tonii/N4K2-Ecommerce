from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.order_response_schema import GetOrdersByUserIdResponse, OrderResponse
from ..models.order_model import OrderModel, OrderStatus
from ..models.product_order_model import ProductOrderModel
from starlette import status

class OrderTasks:
    
    @classmethod
    async def get_orders_by_user_id_task(cls, async_session: AsyncSession, user_id: int) -> GetOrdersByUserIdResponse:
        order_query = select(OrderModel).where(OrderModel.user_id == user_id)
        order_query_result = await async_session.execute(order_query)
        orders = order_query_result.scalars().all()
        if not orders:
            return GetOrdersByUserIdResponse(orders=[])
        response_orders = []
        for order in orders:
            product_query = select(ProductOrderModel.product_id).where(ProductOrderModel.order_id == order.id)
            product_query_result = await async_session.execute(product_query)
            product_ids = [row[0] for row in product_query_result.fetchall()]
            order_response = OrderResponse(
                id=order.id,
                total_price=order.total_price,
                phone_number=order.phone_number,
                address=order.address,
                full_name=order.full_name,
                status=order.status,
                products=product_ids
            )
            response_orders.append(order_response)
        return GetOrdersByUserIdResponse(orders=response_orders)
    
    @classmethod
    async def update_order_status_task(cls, async_session: AsyncSession, order_id: int, order_status: str) -> OrderResponse:
        match order_status:
            case "pending":
                new_status = OrderStatus.PENDING
            case "shipped":
                new_status = OrderStatus.SHIPPED
            case "delivered":
                new_status = OrderStatus.DELIVERED
            case "canceled":
                new_status = OrderStatus.CANCELED
            case _:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Trạng thái đơn hàng không hợp lệ"
                )
        order_query = select(OrderModel).where(OrderModel.id == order_id)
        order_query_result = await async_session.execute(order_query)
        order = order_query_result.scalar()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Đơn hàng không tồn tại"
            )
        order.status = new_status
        await async_session.commit()
        await async_session.refresh(order)
        product_query = select(ProductOrderModel).where(ProductOrderModel.order_id == order_id)
        product_query_result = await async_session.execute(product_query)
        products = product_query_result.scalars().all()
        product_list = [item.product_id for item in products]
        return OrderResponse(
            id=order.id,
            total_price=order.total_price,
            phone_number=order.phone_number,
            address=order.address,
            full_name=order.full_name,
            status=order.status,
            products=product_list
        )