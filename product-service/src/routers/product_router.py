from typing import List
from fastapi import APIRouter
from starlette import status
from ..schemas.product_response_schema import ProductResponse
from ..schemas.product_request_shema import CreateProductRequest, UpdateProductRequest
from ..tasks.product_tasks import ProductTasks

router = APIRouter(prefix="/product", tags=["Product"])

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(request: CreateProductRequest):
    return await ProductTasks.create_product_task(
        name=request.name,
        price=request.price,
        description=request.description,
        category_id=request.category_id,
        image_url=request.image_url
    )
    
@router.get(path="/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
async def get_products():
    return await ProductTasks.get_all_products_task()

@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_product_by_id(id: str):
    return await ProductTasks.get_product_by_id_task(id=id)

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(id: str):
    return await ProductTasks.delete_product_by_id_task(id=id)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product_by_id(id: str, request: UpdateProductRequest):
    return await ProductTasks.update_product_by_id_task(
        id=id,
        name=request.name,
        price=request.price,
        description=request.description,
        category_id=request.category_id,
        image_url=request.image_url
    )