from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from ..schemas.user_response_schema import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user_model import User

class UserTasks:
    
    @classmethod
    async def get_user_by_email_task(cls, async_session: AsyncSession, email: str) -> UserResponse:
        statement = select(User).where(User.email == email)
        result = await async_session.execute(statement)
        user_model = result.scalars().first()
        if not user_model:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
        return UserResponse(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            refresh_token=user_model.refresh_token,
            phone_number=user_model.phone_number,
            address=user_model.address,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            account_type=user_model.account_type
        )
    
    @classmethod
    async def delete_user_by_id_task(cls, async_session: AsyncSession, id: int) -> None:
        statement = select(User).where(User.id == id)
        result = await async_session.execute(statement)
        user_model = result.scalars().first()
        if not user_model:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
        await async_session.delete(user_model)
        await async_session.commit()
    
    @classmethod
    async def get_user_by_id_task(cls, async_session: AsyncSession, id: int) -> UserResponse:
        statememt = select(User).where(User.id == id)
        result = await async_session.execute(statememt)
        user_model = result.scalars().first()
        if not user_model:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
        return UserResponse(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            refresh_token=user_model.refresh_token,
            phone_number=user_model.phone_number,
            address=user_model.address,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            account_type=user_model.account_type
        )
        
    @classmethod
    async def create_user_task(cls, async_session: AsyncSession, email: str, hashed_password: str) -> UserResponse:
        statement = select(User).where(User.email == email)
        result = await async_session.execute(statement)
        user_model = result.scalars().first()
        if user_model:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
        new_user = User(email=email, hashed_password=hashed_password)
        async_session.add(new_user)
        await async_session.commit()
        await async_session.refresh(new_user)
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            hashed_password=new_user.hashed_password,
            refresh_token=new_user.refresh_token,
            phone_number=new_user.phone_number,
            address=new_user.address,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
            account_type=new_user.account_type
        )
    
    @classmethod
    async def update_user_task(
        cls, 
        async_session: AsyncSession, 
        id: int, 
        hashed_password: Optional[str],
        refresh_token: Optional[str],
        phone_number: Optional[str],
        address: Optional[str],
    ) -> UserResponse:
        statement = select(User).where(User.id == id).with_for_update()
        result = await async_session.execute(statement)
        user_model = result.scalars().first()
        if not user_model:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
        if hashed_password:
            user_model.hashed_password = hashed_password
        if refresh_token:
            user_model.refresh_token = refresh_token
        if phone_number:
            user_model.phone_number = phone_number
        if address:
            user_model.address = address
        await async_session.commit()
        await async_session.refresh(user_model)
        return UserResponse(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            refresh_token=user_model.refresh_token,
            phone_number=user_model.phone_number,
            address=user_model.address,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            account_type=user_model.account_type
        )