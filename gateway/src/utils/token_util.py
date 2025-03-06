from datetime import datetime, timedelta, timezone

from jose import jwt
from starlette import status
from fastapi import HTTPException
from jose.exceptions import JWTError

from ..configs.variables import ACCESS_TOKEN_EXPIRES, HASH_ALGORITHM, REFRESH_TOKEN_EXPIRES, SECRET_KEY

class TokenKey:
    ID: str = "id"
    EXPIRES: str = "exp"
    ACCOUNT_TYPE: str = "account_type"
    
class TokenClaims:
    id: int
    account_type: str
    
    def __init__(self, id: str, account_type: str):
        self.account_type = account_type
        self.id = id

def create_access_token(user_id: int, account_type: str) -> str:
    encode = { TokenKey.ID: user_id, TokenKey.ACCOUNT_TYPE: account_type }
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    encode.update({ TokenKey.EXPIRES: expires })
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

def create_refresh_token(user_id: int, account_type: str) -> str:
    encode = { TokenKey.ID: user_id, TokenKey.ACCOUNT_TYPE: account_type }
    expires = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES)
    encode.update({ TokenKey.EXPIRES: expires })
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

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