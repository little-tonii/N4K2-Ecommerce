from fastapi import APIRouter, HTTPException
from ..schemas.user_response_schema import UserResponse
from ..tasks.user_tasks import UserTasks
from ..schemas.user_request_schema import CreateUserRequest, UpdateUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..configs.database import get_db
from starlette import status

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(id: int = None, email: str = None, async_session: AsyncSession = Depends(get_db)) -> UserResponse:
    if id is not None:
        return await UserTasks.get_user_by_id_task(async_session=async_session, id=id)
    elif email is not None:
        return await UserTasks.get_user_by_email_task(async_session=async_session, email=email)
    else:
        raise HTTPException(status_code=400, detail="Vui lòng nhập id hoặc email")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, async_session: AsyncSession = Depends(get_db)):
    return await UserTasks.create_user_task(
        async_session=async_session, 
        email=request.email,
        hashed_password=request.hashed_password
    )

@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(request: UpdateUserRequest, id: int, async_session: AsyncSession = Depends(get_db)):
    return await UserTasks.update_user_task(
        async_session=async_session, 
        id=id,
        hashed_password=request.hashed_password,
        refresh_token=request.refresh_token,
        phone_number=request.phone_number,
        address=request.address
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id: int, async_session: AsyncSession = Depends(get_db)):
    return await UserTasks.delete_user_by_id_task(
        async_session=async_session, 
        id=id
    )