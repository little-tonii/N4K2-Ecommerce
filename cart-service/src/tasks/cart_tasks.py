from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.cart_model import CartModel
from ..models.product_cart_model import ProductCartModel
from ..schemas.cart_response_schema import AddProductToCartResponse, GetProductsInCartResponse, ProductInCart
from starlette import status

class CartTasks:
    
    @classmethod
    async def add_product_to_cart_task(cls, async_session: AsyncSession, user_id: int, product_id: str, quantity: int) -> AddProductToCartResponse:
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
            quantity=product.quantity
        )
        
            
    @classmethod 
    async def remove_product_from_cart(cls, async_session: AsyncSession, user_id: int, product_id: str) -> None:
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
    async def get_products_in_cart(cls, async_session: AsyncSession, user_id: int) -> GetProductsInCartResponse:
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
                ProductInCart(product_id=product.product_id, quantity=product.quantity) 
                for product in products
            ]
        )