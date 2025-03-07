from typing import List
from fastapi import APIRouter
from ..schemas.category_response_schema import CategoryResponse
from starlette import status
from ..schemas.category_request_schema import CreateCategoryRequest, UpdateCategoryRequest
from ..tasks.category_tasks import CategoryTasks

router = APIRouter(prefix="/category", tags=["Category"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def create_category(request: CreateCategoryRequest):
    return await CategoryTasks.create_category_task(name=request.name)

@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories():
    return await CategoryTasks.get_all_categories_task()

@router.get("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category_by_id(id: str):
    return await CategoryTasks.get_category_by_id_task(id=id)

@router.put("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(id: str, request: UpdateCategoryRequest):
    return await CategoryTasks.update_category_task(id=id, name=request.name)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str):
    return await CategoryTasks.delete_category_task(id=id)