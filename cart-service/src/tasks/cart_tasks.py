from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product_cart_model import ProductCartModel
from ..models.cart_model import CartModel
from ..models.product_cart_model import ProductCartModel
from ..schemas.cart_response_schema import AddProductToCartResponse, CheckOutCartResponse, GetProductsInCartResponse, ProductInCart
from starlette import status
from ..models.order_model import OrderModel, OrderStatus
from ..models.product_order_model import ProductOrderModel

class CartTasks:
    
    @classmethod
    async def add_product_to_cart_task(cls, async_session: AsyncSession, user_id: int, product_id: str, quantity: int, price) -> AddProductToCartResponse:
        cart_query = select(CartModel).where(CartModel.user_id == user_id)
        cart_query_result = await async_session.execute(cart_query)
        cart = cart_query_result.scalar()
        if not cart:
            cart = CartModel(user_id=user_id)
            async_session.add(cart)
            await async_session.commit()
            await async_session.refresh(cart)
        product_query = select(ProductCartModel).where(ProductCartModel.cart_id == cart.id, ProductCartModel.product_id == product_id)
        product_query_result = await async_session.execute(product_query)
        product = product_query_result.scalar()
        if product:
            product.quantity += quantity
        else:
            product = ProductCartModel(cart_id=cart.id, product_id=product_id, quantity=quantity)
            async_session.add(product)
        await async_session.commit()
        await async_session.refresh(product)
        return AddProductToCartResponse(
            user_id=cart.user_id,
            product_id=product.product_id,
            quantity=product.quantity,
            price=product.price
        )
        
            
    @classmethod 
    async def remove_product_from_cart_task(cls, async_session: AsyncSession, user_id: int, product_id: str) -> None:
        cart_query = select(CartModel).where(CartModel.user_id == user_id)
        cart_query_result = await async_session.execute(cart_query)
        cart = cart_query_result.scalar()
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có sản phẩm trong giỏ hàng")
        product_query = select(ProductCartModel).where(ProductCartModel.cart_id == cart.id, ProductCartModel.product_id == product_id)
        product_query_result = await async_session.execute(product_query)
        product = product_query_result.scalar()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có sản phẩm trong giỏ hàng")
        await async_session.delete(product)
        await async_session.commit()
        
    @classmethod
    async def get_products_in_cart_task(cls, async_session: AsyncSession, user_id: int) -> GetProductsInCartResponse:
        cart_query = select(CartModel).where(CartModel.user_id == user_id)
        cart_query_result = await async_session.execute(cart_query)
        cart = cart_query_result.scalar()
        if not cart:
            return GetProductsInCartResponse(products=[])
        product_query = select(ProductCartModel).where(ProductCartModel.cart_id == cart.id)
        product_query_result = await async_session.execute(product_query)
        products = product_query_result.scalars().all()
        return GetProductsInCartResponse(
            products=[
                ProductInCart(product_id=product.product_id, quantity=product.quantity, price=product.price) 
                for product in products
            ]
        )
        
    @classmethod
    async def checkout_cart_task(cls, async_session: AsyncSession, user_id: int, phone_number: str, address: str, full_name: str) -> CheckOutCartResponse:
        cart_query = select(CartModel).where(CartModel.user_id == user_id)
        cart_query_result = await async_session.execute(cart_query)
        cart = cart_query_result.scalar()
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Giỏ hàng không có sản phẩm nào")
        product_query = select(ProductCartModel).where(ProductCartModel.cart_id == cart.id)
        product_query_result = await async_session.execute(product_query)
        products_in_cart = product_query_result.scalars().all()
        if not products_in_cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Giỏ hàng không có sản phẩm nào")
        total_price = 0
        product_list = []
        for item in products_in_cart:
            total_price += item.price * item.quantity
            product_list.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price
            })
        new_order = OrderModel(
            user_id=user_id,
            total_price=total_price,
            phone_number=phone_number, 
            address=address,
            full_name=full_name,
            status=OrderStatus.PENDING
        )
        async_session.add(new_order)
        await async_session.commit()
        await async_session.refresh(new_order)
        for item in products_in_cart:
            new_product_order = ProductOrderModel(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            async_session.add(new_product_order)
        for item in products_in_cart:
            await async_session.delete(item)
        await async_session.commit()
        return CheckOutCartResponse(
            id=new_order.id,
            total_price=new_order.total_price,
            phone_number=new_order.phone_number,
            address=new_order.address,
            full_name=new_order.full_name,
            status=new_order.status,
            products=[p["product_id"] for p in product_list]
        )