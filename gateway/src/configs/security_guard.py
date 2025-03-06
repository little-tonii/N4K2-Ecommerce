from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException
from starlette import status
from ..configs.variables import HASH_ALGORITHM, SECRET_KEY
from ..utils.token_util import TokenClaims, TokenKey
from ..services.user_service import UserService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')        

async def verify_access_token(token: Annotated[OAuth2PasswordBearer, Depends(oauth2_bearer)]) -> TokenClaims:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int = payload.get(TokenKey.ID)
        expires: int = payload.get(TokenKey.EXPIRES)
        account_type: str = payload.get(TokenKey.ACCOUNT_TYPE)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if expires and datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if await UserService.get_user_by_id(user_id=user_id) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        return TokenClaims(id=user_id, account_type=account_type)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')