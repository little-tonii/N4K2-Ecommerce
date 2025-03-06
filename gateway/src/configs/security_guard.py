from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException
from starlette import status
from ..configs.variables import HASH_ALGORITHM, SECRET_KEY
from ..utils.token_util import TokenKey
from ..services.user_service import UserService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')        

class TokenClaims:
    id: int
    account_type: str
    
    def __init__(self, id: str, account_type: str):
        self.account_type = account_type
        self.id = id

async def verify_access_token(token: Annotated[OAuth2PasswordBearer, Depends(oauth2_bearer)]) -> TokenClaims:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int = payload.get(TokenKey.ID)
        expires: int = payload.get(TokenKey.EXPIRES)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if expires and datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        user_response = await UserService.get_user_by_id(user_id=user_id)
        if user_response is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')    
        return TokenClaims(id=user_id, account_type=user_response.account_type)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
    
def verify_refresh_token(refresh_token: str) -> TokenClaims:
    try:
        payload = jwt.decode(token=refresh_token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int = payload.get(TokenKey.ID)
        expires: int = payload.get(TokenKey.EXPIRES)
        account_type: str = payload.get(TokenKey.ACCOUNT_TYPE)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if expires and datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        return TokenClaims(id=user_id, account_type=account_type)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')