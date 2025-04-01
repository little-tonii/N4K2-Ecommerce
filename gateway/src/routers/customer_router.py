from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ..utils.token_util import TokenClaims

from ..configs.security_guard import verify_access_token
from ..services.customer_service import CustomerService
from ..schemas.requests.customer_request_schema import CustomerRegisterRequest, CustomerUpdateInfoRequest
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne, CustomerUpdateInfoResponse
from ..schemas.requests.cart_request_schema import CheckoutCartRequest, AddProductToCartRequest, RemoveProductFromCartRequest
from ..schemas.responses.cart_response_schema import CartCheckoutResponse, AddProductToCartResponse, CartResponse

router = APIRouter(prefix='/customer', tags=['Customer'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=CustomerRegisterResposne)
async def register(request: CustomerRegisterRequest):
    return await CustomerService.register_customer(email=request.email, password=request.password)

@router.patch('/update-info', status_code=status.HTTP_200_OK, response_model=CustomerUpdateInfoResponse)
async def update_info(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: CustomerUpdateInfoRequest):
    return await CustomerService.update_customer_info(customer_id=claims.id, phone_number=request.phone_number, address=request.address, account_type=claims.account_type)

@router.post('/add-product-to-cart', status_code=status.HTTP_201_CREATED, response_model=AddProductToCartResponse)
async def add_product_to_cart(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: AddProductToCartRequest):
    return await CustomerService.add_product_to_cart(
        user_id=claims.id,
        account_type=claims.account_type,
        product_id=request.product_id,
        quantity=request.quantity
    )

@router.delete(path='/remove-product-from-cart', status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    request: RemoveProductFromCartRequest
):
    return await CustomerService.remove_product_from_cart(
        user_id=claims.id,
        product_id=request.product_id,
        account_type=claims.account_type
    )

@router.get(path='/get-cart', status_code=status.HTTP_200_OK, response_model=CartResponse)
async def get_cart(claims: Annotated[TokenClaims, Depends(verify_access_token)]):
    return await CustomerService.get_cart(user_id=claims.id, account_type=claims.account_type)

@router.post(path='/check-out-cart', status_code=status.HTTP_201_CREATED, response_model=CartCheckoutResponse)
async def check_out_cart(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: CheckoutCartRequest):
    return await CustomerService.check_out_cart(
        user_id=claims.id,
        account_type=claims.account_type,
        address=request.address,
        phone_number=request.phone_number,
        full_name=request.full_name,
    )
