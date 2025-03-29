from fastapi import APIRouter, Form, UploadFile
from starlette import status

from ..utils.validator import validate_product_name, validate_product_description, validate_product_price, validate_picture

from ..services.product_service import ProductService
from ..schemas.responses.product_response_schema import GetProductsResponse, GetProductResponse, CreateProductResponse
from typing import Annotated
from ..utils.token_util import TokenClaims
from ..configs.security_guard import verify_access_token
from fastapi import Depends

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
