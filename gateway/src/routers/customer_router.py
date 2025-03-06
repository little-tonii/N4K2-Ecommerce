from fastapi import APIRouter
from starlette import status
from ..services.customer_service import CustomerService
from ..schemas.requests.customer_request_schema import CustomerRegisterRequest
from ..schemas.responses.customer_response_schema import CustomerRegisterResposne

router = APIRouter(prefix='/customer', tags=['Customer'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=CustomerRegisterResposne)
async def register(request: CustomerRegisterRequest):
    return await CustomerService.register_customer(email=request.email, password=request.password)