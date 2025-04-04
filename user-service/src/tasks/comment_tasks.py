from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from ..models.comment_model import Comment
from ..models.user_model import User
from ..schemas.comment_response_schema import CommentResponse
from starlette import status
from typing import cast
from datetime import datetime
from sqlalchemy import select

class CommentTasks:

    @classmethod
    async def comment_on_product_task(cls, async_session: AsyncSession, user_id: int, product_id: str, content: str) -> CommentResponse:
        existedUser = await async_session.get(User, user_id)
        if not existedUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
        new_comment = Comment(
            content=content,
            user_id=user_id,
            product_id=product_id
        )
        async_session.add(new_comment)
        try:
            await async_session.commit()
            await async_session.refresh(new_comment)
        except Exception:
            await async_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra khi tạo bình luận")

        return CommentResponse(
            id=cast(int, new_comment.id),
            user_id=cast(int, new_comment.user_id),
            product_id=cast(str, new_comment.product_id),
            created_at=cast(datetime, new_comment.created_at),
            updated_at=cast(datetime, new_comment.updated_at),
            content=cast(str, new_comment.content),
        )

    @classmethod
    async def update_comment_task(cls, async_session: AsyncSession, id: int, content: str) -> CommentResponse:
        existedComment = await async_session.get(Comment, id)
        if not existedComment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bình luận không tồn tại")
        existedComment.content = content # type: ignore
        async_session.add(existedComment)
        try:
            await async_session.commit()
            await async_session.refresh(existedComment)
        except Exception:
            await async_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra khi cập nhật bình luận")

        return CommentResponse(
            id=cast(int, existedComment.id),
            user_id=cast(int, existedComment.user_id),
            product_id=cast(str, existedComment.product_id),
            created_at=cast(datetime, existedComment.created_at),
            updated_at=cast(datetime, existedComment.updated_at),
            content=cast(str, existedComment.content),
        )

    @classmethod
    async def delete_comment_task(cls, async_session: AsyncSession, id: int) -> None:
        existedComment = await async_session.get(Comment, id)
        if not existedComment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bình luận không tồn tại")
        await async_session.delete(existedComment)
        try:
            await async_session.commit()
        except Exception:
            await async_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra khi xóa bình luận")

        return None

    @classmethod
    async def get_comments_by_user_task(cls, async_session: AsyncSession, user_id: int) -> list[CommentResponse]:
        comments = await async_session.execute(select(Comment).where(Comment.user_id == user_id))
        return [CommentResponse(
            id=cast(int, comment.id),
            user_id=cast(int, comment.user_id),
            product_id=cast(str, comment.product_id),
            created_at=cast(datetime, comment.created_at),
            updated_at=cast(datetime, comment.updated_at),
            content=cast(str, comment.content),
        ) for comment in comments.scalars()]

    @classmethod
    async def get_comments_by_product_task(cls, async_session: AsyncSession, product_id: str) -> list[CommentResponse]:
        comments = await async_session.execute(select(Comment).where(Comment.product_id == product_id))
        return [CommentResponse(
            id=cast(int, comment.id),
            user_id=cast(int, comment.user_id),
            product_id=cast(str, comment.product_id),
            created_at=cast(datetime, comment.created_at),
            updated_at=cast(datetime, comment.updated_at),
            content=cast(str, comment.content),
        ) for comment in comments.scalars()]
