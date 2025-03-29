from fastapi import APIRouter
from starlette import status

from ..services.product_service import ProductService
from ..schemas.responses.product_response_schema import GetProductsResponse

router = APIRouter(prefix="/product", tags=["Product"])

@router.get(path="/", status_code=status.HTTP_200_OK, response_model=GetProductsResponse)
async def all_products():
    return await ProductService.get_products()
