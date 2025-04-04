from fastapi import APIRouter, Form, UploadFile
from starlette import status

from ..services.comment_service import CommentService

from ..schemas.requests.comment_request_schema import CommentOnProductRequest

from ..utils.validator import validate_product_name, validate_product_description, validate_product_price, validate_picture

from ..services.product_service import ProductService
from ..schemas.responses.product_response_schema import GetProductsResponse, GetProductResponse, CreateProductResponse, UpdateProductResponse, UpdateProductImageResponse
from ..schemas.requests.product_request_schema import UpdateProductRequest
from typing import Annotated
from ..utils.token_util import TokenClaims
from ..configs.security_guard import verify_access_token
from fastapi import Depends
from ..schemas.responses.comment_response_schema import CommentOnProductResponse, GetCommentsResponse

router = APIRouter(prefix="/product", tags=["Product"])

@router.get(path="/", status_code=status.HTTP_200_OK, response_model=GetProductsResponse)
async def all_products():
    return await ProductService.get_products()

@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=GetProductResponse)
async def product_by_id(id: str):
    return await ProductService.get_product(id=id)

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=CreateProductResponse)
async def create_product(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    name: str = Depends(validate_product_name),
    price: int = Depends(validate_product_price),
    description: str = Depends(validate_product_description),
    category_id: str = Form(...),
    picture: UploadFile = Depends(validate_picture)
):
    return await ProductService.create_product(
        account_type=claims.account_type,
        name=name,
        price=price,
        description=description,
        category_id=category_id,
        picture=picture
    )

@router.put(path="/{id}", status_code=status.HTTP_200_OK, response_model=UpdateProductImageResponse)
async def update_product_image(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    id: str,
    picture: UploadFile = Depends(validate_picture)
):
    return await ProductService.update_product_image(
        account_type=claims.account_type,
        id=id,
        picture=picture
    )

@router.patch(path="/{id}", status_code=status.HTTP_200_OK, response_model=UpdateProductResponse)
async def update_product(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    id: str,
    request: UpdateProductRequest
):
    return await ProductService.update_product(
        account_type=claims.account_type,
        id=id,
        name=request.name,
        price=request.price,
        description=request.description,
        category_id=request.category_id
    )

@router.post(path="/{product_id}/comment", status_code=status.HTTP_201_CREATED, response_model=CommentOnProductResponse)
async def comment_on_product(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    product_id: str,
    request: CommentOnProductRequest
):
    return await CommentService.create_comment(
        user_id=claims.id,
        content=request.content,
        product_id=product_id
    )

@router.get(path="/{product_id}/comment", status_code=status.HTTP_200_OK, response_model=GetCommentsResponse)
async def get_comments(product_id: str):
    return await CommentService.get_all_comments_by_product_id(product_id=product_id)
