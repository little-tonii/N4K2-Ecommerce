from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..configs.database import get_db
from ..tasks.comment_tasks import CommentTasks

from ..schemas.comment_request_schema import CreateCommentRequest, UpdateCommentRequest

from ..schemas.comment_response_schema import CommentResponse

router = APIRouter(prefix="/comment", tags=["Comment"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def comment_on_product(request: CreateCommentRequest, async_session: AsyncSession = Depends(get_db)):
    return await CommentTasks.comment_on_product_task(
        user_id=request.user_id,
        product_id=request.product_id,
        content=request.content,
        async_session=async_session
    )

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def update_comment(id: int, request: UpdateCommentRequest, async_session: AsyncSession = Depends(get_db)):
    return await CommentTasks.update_comment_task(
        id=id,
        content=request.content,
        async_session=async_session
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int, async_session: AsyncSession = Depends(get_db)):
    await CommentTasks.delete_comment_task(
        id=id,
        async_session=async_session
    )

@router.get(path="/user/{user_id}", status_code=status.HTTP_200_OK, response_model=list[CommentResponse])
async def get_comments_by_user(user_id: int, async_session: AsyncSession = Depends(get_db)):
    return await CommentTasks.get_comments_by_user_task(
        user_id=user_id,
        async_session=async_session
    )

@router.get(path="/product/{product_id}", status_code=status.HTTP_200_OK, response_model=list[CommentResponse])
async def get_comments_by_product(product_id: str, async_session: AsyncSession = Depends(get_db)):
    return await CommentTasks.get_comments_by_product_task(
        product_id=product_id,
        async_session=async_session
    )