from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ..utils.token_util import TokenClaims

from ..configs.security_guard import verify_access_token
from ..services.customer_service import CustomerService
from ..schemas.requests.customer_request_schema import CustomerRegisterRequest, CustomerUpdateInfoRequest
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne, CustomerUpdateInfoResponse

router = APIRouter(prefix='/customer', tags=['Customer'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=CustomerRegisterResposne)
async def register(request: CustomerRegisterRequest):
    return await CustomerService.register_customer(email=request.email, password=request.password)

@router.patch('/update-info', status_code=status.HTTP_200_OK, response_model=CustomerUpdateInfoResponse)
async def update_info(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: CustomerUpdateInfoRequest):
    return await CustomerService.update_customer_info(customer_id=claims.id, phone_number=request.phone_number, address=request.address, account_type=claims.account_type)