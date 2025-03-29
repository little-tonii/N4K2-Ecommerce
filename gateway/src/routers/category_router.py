from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ..schemas.requests.category_request_schema import CreateCategoryRequest, UpdateCategoryRequest
from ..configs.security_guard import verify_access_token
from ..utils.token_util import TokenClaims
from ..schemas.responses.category_response_schema import CreateCategoryResponse, GetAllCategoryResponse, UpdateCategoryResponse
from ..services.category_service import CategoryService

router = APIRouter(prefix="/category", tags=["Category"])

@router.get(path="/", response_model=GetAllCategoryResponse, status_code=status.HTTP_200_OK)
async def all_categories():
    return await CategoryService.get_all_categories()

@router.post(path="/", response_model=CreateCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: CreateCategoryRequest):
    return await CategoryService.create_category(account_type=claims.account_type, name=request.name)

@router.put(path="/{id}", response_model=UpdateCategoryResponse, status_code=status.HTTP_200_OK)
async def update(claims: Annotated[TokenClaims, Depends(verify_access_token)], id: str, request: UpdateCategoryRequest):
    return await CategoryService.update_category(id=id, name=request.name, account_type=claims.account_type)
