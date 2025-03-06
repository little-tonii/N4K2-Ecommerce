from datetime import datetime, timedelta, timezone

from jose import jwt

from ..configs.variables import ACCESS_TOKEN_EXPIRES, HASH_ALGORITHM, REFRESH_TOKEN_EXPIRES, SECRET_KEY

class TokenKey:
    ID: str = "id"
    EXPIRES: str = "exp"
    ACCOUNT_TYPE: str = "account_type"

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