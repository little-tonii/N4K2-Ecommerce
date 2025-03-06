from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ..utils.token_util import TokenClaims

from ..configs.security_guard import verify_access_token

from ..schemas.requests.user_request_schema import UserChangePasswordRequest, UserRefreshTokenRequest

from ..services.user_service import UserService

from ..schemas.responses.user_response_schema import UserAccessTokenResponse, UserLoginResponse, UserInfoResponse

router = APIRouter(prefix='/user', tags=['User'])

@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def login(login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await UserService.login_user(email=login_form.username, password=login_form.password)

@router.post(path="/refresh-token", status_code=status.HTTP_200_OK, response_model=UserAccessTokenResponse)
async def refresh_token(request: UserRefreshTokenRequest):
    return await UserService.get_access_token(refresh_token=request.refresh_token)

@router.post(path="/change-password", status_code=status.HTTP_200_OK)
async def change_password(claims: Annotated[TokenClaims, Depends(verify_access_token)], request: UserChangePasswordRequest):
    return await UserService.change_user_password(user_id=claims.id, new_password=request.new_password, old_password=request.old_password)

@router.get(path="/user-info", status_code=status.HTTP_200_OK, response_model=UserInfoResponse)
async def user_info(claims: Annotated[TokenClaims, Depends(verify_access_token)]):
    return await UserService.get_user_info(user_id=claims.id)